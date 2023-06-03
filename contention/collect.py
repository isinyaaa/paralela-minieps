import csv
import subprocess
from multiprocessing import cpu_count

MONTE_CARLO = 1000


def compile(if_count):
    subprocess.call(["make", f"IF={if_count}"])


def run(threads, array_size):
    contention = subprocess.run(["./contention", str(threads), str(array_size)],
                                text=True, capture_output=True)
    return contention.stdout.strip()[:-1]


def run_monte_carlo(max_size_exp=19, max_threads=cpu_count()):
    import math
    runs = []
    print(f"CPU count: {cpu_count()}")
    for if_count in range(2):
        compile(if_count)
        exp = int(math.log2(max_threads))
        # we need the workload to be about 20000 values/thread
        for array_exp in range(exp + 14, exp + max_size_exp):
            print(f"if_count: {if_count}, array_exp: {array_exp}")
            times = []
            for _ in range(MONTE_CARLO):
                time = run(max_threads, 2**array_exp)
                time = int(float(time))
                assert time > 0, f"{time=} is not positive"
                times.append(time)
            time = sum(times) / MONTE_CARLO
            stddev = sum((t - time)**2 for t in times) / MONTE_CARLO
            runs.append({"if_count": if_count, "array_exp": array_exp,
                         "time": time, "stddev": stddev})
            print(time)

    with open("runs.csv", "w") as f:
        writer = csv.DictWriter(f, ["if_count", "array_exp", "time", "stddev"])
        writer.writeheader()
        writer.writerows(runs)

    return runs


def main():
    import os.path
    from sys import argv

    from matplotlib import pyplot as plt

    if len(argv) > 1 and input("Run Monte Carlo? (y/n) ") == "y":
        print("Running Monte Carlo")
        try:
            size_exp = int(argv[1])
            if len(argv) > 2:
                max_threads = int(argv[2])
                runs = run_monte_carlo(size_exp, max_threads)
            else:
                runs = run_monte_carlo(size_exp)
        except ValueError:
            runs = run_monte_carlo()
    else:
        # see if file exists
        if not os.path.exists("runs.csv"):
            raise FileNotFoundError("runs.csv not found, please run simulation first")

        print("Loading from runs.csv")
        with open("runs.csv") as f:
            reader = csv.DictReader(f)
            runs = list(reader)

        for run in runs:
            for key in run:
                if key != "if_count":
                    run[key] = float(run[key])
                else:
                    run[key] = int(run[key])

    # plot time vs array exp with error bars as stddev for if=0 and if=1
    # (different lines)
    plt.errorbar([r["array_exp"] for r in runs if r["if_count"] == 0],
                 [r["time"] for r in runs if r["if_count"] == 0],
                 yerr=[r["stddev"] for r in runs if r["if_count"] == 0],
                 label="if=0", color="blue", linestyle="dashed")
    plt.errorbar([r["array_exp"] for r in runs if r["if_count"] == 1],
                 [r["time"] for r in runs if r["if_count"] == 1],
                 yerr=[r["stddev"] for r in runs if r["if_count"] == 1],
                 label="if=1", color="red")
    plt.xlabel("log2(array size)")
    plt.ylabel("time (ms)")
    plt.legend()
    plt.savefig("runs.png", dpi=300)


if __name__ == "__main__":
    main()

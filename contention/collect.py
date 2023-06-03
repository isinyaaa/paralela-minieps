import csv
import math
from multiprocessing import cpu_count
import subprocess


def compile(if_count):
    subprocess.call(["make", f"IF={if_count}"])


def run(threads, array_size):
    contention = subprocess.run(["./contention", str(threads), str(array_size)],
                                text=True, capture_output=True)
    return contention.stdout.strip()[:-1]


def main():
    runs = []
    print(f"CPU count: {cpu_count()}")
    for if_count in range(2):
        compile(if_count)
        exp = int(math.log2(cpu_count()))
        # we need the workload to be about 20000 values/thread
        for array_exp in range(exp + 14, exp + 19):
            print(f"if_count: {if_count}, array_exp: {array_exp}")
            time = run(cpu_count(), 2**array_exp)
            time = int(float(time))
            assert time > 0, f"{time=} is not positive"
            runs.append({"if_count": if_count, "array_exp": array_exp,
                         "time": time})

    with open("runs.csv", "w") as f:
        writer = csv.DictWriter(f, ["if_count", "threads", "array_exp", "time"])
        writer.writeheader()
        writer.writerows(runs)


if __name__ == "__main__":
    main()

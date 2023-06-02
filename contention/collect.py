import csv
import subprocess


def compile(if_count):
    subprocess.call(["make", f"IF={if_count}"])


def run(threads, array_size):
    contention = subprocess.run(["./contention", str(threads), str(array_size)],
                                text=True, capture_output=True)
    return contention.stdout.strip()[:-1]


def main():
    runs = []
    for if_count in range(4):
        compile(if_count)
        for thread_count in range(32, 257, 32):
            for array_exp in range(1, 21):
                print(f"if_count: {if_count}, threads: {thread_count}, array_exp: {array_exp}")
                time = run(thread_count, 2**array_exp)
                runs.append({"if_count": if_count,
                             "threads": thread_count, "array_exp": array_exp,
                             "time": time})

    with open("runs.csv", "w") as f:
        writer = csv.DictWriter(f, ["if_count", "threads", "array_exp", "time"])
        writer.writeheader()
        writer.writerows(runs)


if __name__ == "__main__":
    main()

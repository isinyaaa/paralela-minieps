import matplotlib.pyplot as plt
import pandas as pd
import subprocess

def main():
    results = []

    for i in range(8, 13):
        for a in range(1, 3):
            if a == 2:
                for bs in range(3, 9):

                    if bs > i:
                        break

                    print(f'Running GEMM {str(a)} with n={str(2**i)} and block size={str(2**bs)}')

                    t = subprocess.check_output(["./main",
                                                 "-n", str(2**i),
                                                 "-a", str(a),
                                                 "-b", str(2**bs)])
                    t = float(t.decode('utf-8'))
                    results.append({'algorithm': a,
                                    'n': 2**i,
                                    'bs': 2**bs,
                                    'time': t})

                    print(f'Finished in {str(t)} seconds')
                continue

            print(f'Running GEMM {str(a)} with n={str(2**i)}')

            t = subprocess.check_output(["./main",
                                         "-n", str(2**i),
                                         "-a", str(a),
                                         "-b", str(1)])

            t = float(t.decode('utf-8'))

            results.append({'algorithm': a,
                            'n': 2**i,
                            'bs': 0,
                            'time': t})

            print(f'Finished in {str(t)} seconds')

    results = pd.DataFrame(results)

    # first, we plot the times for the naive algorithm
    plt.plot(results[results['algorithm'] == 1]['n'],
             results[results['algorithm'] == 1]['time'],
             label='GEMM 1')

    # now, we plot the times for the blocked algorithm
    # each block size will be a different line on the same plot
    for bs in range(3, 9):
        plt.plot(results[(results['algorithm'] == 2) & (results['bs'] == 2**bs)]['n'],
                 results[(results['algorithm'] == 2) & (results['bs'] == 2**bs)]['time'],
                 label=f'GEMM 2 ({str(2**bs)})')

    plt.xlabel('Matrix Size')
    plt.ylabel('Time (s)')
    plt.title('GEMM Performance')
    plt.legend()
    # save this plot to a file
    plt.savefig('gemm.png', dpi=300)

main()

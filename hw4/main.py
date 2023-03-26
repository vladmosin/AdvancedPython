import multiprocessing as mp
import threading as td
from time import time


def fib_long():
    n1 = 0
    n2 = 1

    for _ in range(500000):
        n2, n1 = n1, n1 + n2

    return n1


def run_process():
    processes = []
    for _ in range(10):
        p = mp.Process(target=fib_long)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


def run_thread():
    threads = []
    for _ in range(10):
        p = td.Thread(target=fib_long)
        p.start()
        threads.append(p)

    for p in threads:
        p.join()


if __name__ == '__main__':
    t1 = time()
    run_process()
    t2 = time()
    run_thread()
    t3 = time()
    print(f'Processes: {round(t2 - t1, 3)} seconds')
    print(f'Threads: {round(t3 - t2, 3)} seconds')

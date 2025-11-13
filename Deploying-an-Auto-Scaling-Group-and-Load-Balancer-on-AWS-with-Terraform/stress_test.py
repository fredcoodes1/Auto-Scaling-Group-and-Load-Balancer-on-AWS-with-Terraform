import multiprocessing
import time


def cpu_stress():
    while True:
        pass  # Infinite loop to keep the CPU busy


if __name__ == "__main__":
    # Get the number of CPU cores
    num_cores = multiprocessing.cpu_count()

    # Create a list to hold the processes
    processes = []

    # Start a process for each CPU core
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)

    # Run the stress test for 3 minutes (180 seconds)
    time.sleep(180)

    # Terminate all processes
    for p in processes:
        p.terminate()
import heapq
from collections import Counter
from itertools import product, islice
from math import prod
import numpy as np
from dataclasses import dataclass
import multiprocessing as mp
from multiprocessing import Pool, Manager
from functools import partial
import time

#FILE = "example.txt"
FILE = "input.txt"

inputs = [line.rstrip("\n").split(" ") for line in open(FILE)]


def check_combinations_batch(chunk, wiring_bitmasks, target):
    """Optimized batch checking using pure numpy operations"""
    if not chunk:
        return False

    chunk_np = np.array(chunk, dtype=np.int32)

    mini_batch_size = 15000

    for i in range(0, len(chunk_np), mini_batch_size):
        batch = chunk_np[i : i + mini_batch_size]

        states = wiring_bitmasks[batch].sum(axis=1)
        matches = (states == target).all(axis=1)

        if matches.any():
            return True

    return False


class Machine:
    lights: str
    lights_bitmask: np.ndarray
    wiring: list[list[int]]
    wiring_bitmasks: np.ndarray
    joltages: list[int]
    joltages_np: np.ndarray
    required_permutations: int

    def __init__(self, lights: str, wiring: list[list[int]], joltages: list[int]):
        self.lights = lights
        self.lights_bitmask = np.array(
            [1 if i == "#" else 0 for i in lights], dtype=np.int32
        )
        self.wiring = wiring
        self.joltages = joltages
        self.joltages_np = np.array(joltages, dtype=np.int32)

        self.wiring_bitmasks = np.array(
            [[1 if i in j else 0 for i in range(len(lights))] for j in wiring],
            dtype=np.int32,
        )

        self.required_permutations = self.get_required_permutations()

    def get_required_permutations(self):
        n_switches = len(self.wiring)
        count = max(self.joltages) - 1
        num_cores = mp.cpu_count()
        total_time_start = time.perf_counter()

        while True:
            count += 1
            print(f"Testing count: {count}")

            total_expected = n_switches**count
            print(f"  Total combinations: {total_expected}")

            all_products = product(range(n_switches), repeat=count)

            chunk_size = 500000

            check_func = partial(
                check_combinations_batch,
                wiring_bitmasks=self.wiring_bitmasks,
                target=self.joltages_np,
            )

            iter_time_start = time.perf_counter()

            
            found = False
            with Pool(num_cores) as pool:
                while True:
                    chunks = []
                    for _ in range(num_cores * 2):
                        chunk = list(islice(all_products, chunk_size))
                        if not chunk:
                            break
                        chunks.append(chunk)

                    if not chunks:
                        break

                    for result in pool.imap_unordered(check_func, chunks):
                        if result:
                            pool.terminate()
                            found = True
                            break

                    if found:
                        break

            iter_time_end = time.perf_counter()
            print(f"  Time taken for count={count}: {iter_time_end - iter_time_start:.3f} seconds")

            if found:
                total_time_end = time.perf_counter()
                print(f"Total time to find count={count}: {total_time_end - total_time_start:.3f} seconds")
                return count

            # if count > 13:
            #     break

        return -1


if __name__ == "__main__":

    total_time_start = time.perf_counter()

    parsed_inputs = [
        Machine(
            lights=line[0].lstrip("[").rstrip("]"),
            wiring=[
                list(map(int, i.lstrip("(").rstrip(")").strip().split(",")))
                for i in line[1:-1]
            ],
            joltages=tuple(map(int, line[-1].strip("{").strip("}").split(","))),
        )
        for line in inputs
    ]

    required_permutations = sum(i.required_permutations for i in parsed_inputs)
    total_time_end = time.perf_counter()
    print(f"Total time: {total_time_end - total_time_start:.3f} seconds")
    print(f"Result: {required_permutations}")

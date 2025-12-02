from multiprocessing import Pool, cpu_count


def check_invalid(j: int) -> int:
    size = len(str(j))
    if size < 2:
        return 0
    if all([i == str(j)[0] for i in list(str(j))]):
        # print(f"{j} all equal")
        return j
    for k in range(2, (size // 2) + 1):
        if size % k != 0:
            continue
        pieces = [str(j)[i : i + k] for i in range(0, size, k)]
        if all([i == pieces[0] for i in pieces]):
            # print(f"{j} all equal in {k} pieces")
            return j
    return 0


def iter_jobs(inputs):
    """Yield all j values from the input ranges."""
    for r in inputs:
        start, end = r.split("-")
        start, end = int(start), int(end)
        for j in range(start, end + 1):
            yield j


# FILE = "example.txt"

if __name__ == "__main__":
    FILE = "input.txt"

    inputs = [(line.split(",")) for line in open(FILE)][0]
    inputs.sort(key=lambda x: int(x.split("-")[0]))

    # Build all jobs (or you could stream with imap if memory is tight)
    jobs = list(iter_jobs(inputs))

    with Pool(cpu_count()) as pool:
        results = pool.map(check_invalid, jobs, chunksize=1000)

    invalid_sum = sum(results)
    print(invalid_sum)

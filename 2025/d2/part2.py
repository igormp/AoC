from multiprocessing import Pool, cpu_count


def check_invalid(j: int) -> int:
    s = str(j)
    size = len(s)
    if size < 2:
        return 0
    if all([i == s[0] for i in s[1:]]):
        # print(f"{j} all equal")
        return j

    for k in range(2, (size // 2) + 1):
        if size % k != 0:
            continue
        piece = s[:k]
        if piece * (size // k) == s:
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


def get_ranges(inputs):
    for r in inputs:
        start, end = r.split("-")
        yield int(start), int(end)


def sum_invalids(start, end):
    total = 0
    for j in range(start, end + 1):
        total += check_invalid(j)
    return total


# FILE = "example.txt"

if __name__ == "__main__":
    FILE = "input.txt"

    inputs = [(line.split(",")) for line in open(FILE)][0]
    inputs.sort(key=lambda x: int(x.split("-")[0]))
    ranges = get_ranges(inputs)

    # Build all jobs (or you could stream with imap if memory is tight)
    jobs = list(iter_jobs(inputs))

    with Pool(cpu_count()) as pool:
        results = pool.starmap(sum_invalids, ranges)

    invalid_sum = sum(results)
    print(invalid_sum)

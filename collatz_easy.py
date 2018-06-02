
def collatz(limit):
    counts = [1]
    for n in range(1, limit + 1):
        c = 1
        while n > 1:
            n = n // 2 if n % 2 == 0 else (n * 3) + 1
            c += 1
        counts.append(c)
    print("With n = {}\nMax count = {}".format(counts.index(max(counts)), max(counts)))
collatz(10000)

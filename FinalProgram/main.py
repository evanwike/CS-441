from functools import reduce
import math
import timeit
from multiprocessing import Pool
import matplotlib.pyplot as plt

data = open('WarAndPeace.txt')

# Strip newlines and empty strings
data = [s.strip() for s in data if s != '']
data = [s for s in data if s != '']

# Convert back to string
data = ' '.join(data)

single = {}
double = {}
triple = {}

# These aren't really 'functional' as they're only used for their side-effects,
# but the PDF said to use reduce and map.  The more-FP functions can be found below.
def get_single_freq(d: dict, c: str):
    d[c] = d.get(c, 0) + 1
    return d


def get_double_freq(a: str, b: str) -> str:
    double[a + b] = double.get(a + b, 0) + 1
    return b


def get_triple_freq(a: str, b: str) -> str:
    triple[a + b] = double.get(a + b, 0) + 1
    return a[-1] + b

# Wasn't sure if we were supposed to include this in the timed execution or not
# Set up single, double, and third-order character count dictionaries
# reduce(get_single_freq, data, single)
# reduce(get_double_freq, data)
# reduce(get_triple_freq, data)

# Function Composition
# H(S) = Σ(Nc)(-Pc)lg2(Pc)
p = lambda c, d: d[c] / reduce(lambda a, b: a + b, d.values())
h = lambda e, d: d[e] * -p(e, d) * math.log2(p(e, d))
hS = lambda d: list(map(lambda e: h(e[0], d), d.items()))
entropies = map(hS, [single, double, triple])

# Single threaded
# Time how long it takes to get info for first, second, and third-order entropy of text file
avg_times = {1: 0, 2: 0, 4: 0, 8: 0, 16: 0, 32: 0, 64: 0}

total_time = 0

for i in range(3):
    start = timeit.default_timer()
    # Set up single, double, and third-order character count dictionaries
    reduce(get_single_freq, data, single)
    reduce(get_double_freq, data)
    reduce(get_triple_freq, data)
    # Calculate info for first, second, and third-order character streams
    info = list(map(sum, entropies))
    stop = timeit.default_timer()

    total_time += stop - start

avg_times[1] = total_time / 3

# Run the program with 2, 4, 8, 16, 32, and 64 threads
for i in range(6):
    threads = 2 ** (i + 1)

    # Take the average time of 3 executions
    total_time = 0

    for j in range(3):
        start = timeit.default_timer()
        with Pool(processes=threads) as pool:
            # Set up single, double, and third-order character count dictionaries
            reduce(get_single_freq, data, single)
            reduce(get_double_freq, data)
            reduce(get_triple_freq, data)
            # Calculate info for first, second, and third-order character streams
            info = list(map(sum, entropies))
        stop = timeit.default_timer()
        total_time += stop - start

    avg_times[threads] = total_time / 3

# Output how long it took to execute with each number of threads
print(avg_times)
plt.xlabel('Number of Threads')
plt.ylabel('Time to Execute (s)')
plt.plot(list(avg_times.keys()), list(avg_times.values()))
plt.show()

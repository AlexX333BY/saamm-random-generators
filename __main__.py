import argparse
from generators.LehmerSequence import LehmerSequence
from SequenceAnalyzer import SequenceAnalyzer
import matplotlib.pyplot as plt
from array import array


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', type=int, required=True, help='value of a', dest='a')
    parser.add_argument('-m', action='store', type=int, required=True, help='value of m', dest='m')
    parser.add_argument('-r0', action='store', type=int, required=True, help='value of R0', dest='r0')
    parser.add_argument('-l', '--length', action='store', type=int, required=True,
                        help='generated sequence length', dest='length')
    args = parser.parse_args()

    lehmer_generator = LehmerSequence(args.a, args.m, args.r0)
    sequence = lehmer_generator.provide_sequence(args.length)

    analyzer = SequenceAnalyzer(sequence)

    k = 20  # number of intervals
    reverse_sorted_sequence = sorted(sequence)
    reverse_sorted_sequence.reverse()
    sequence_length = len(sequence)
    x_min = reverse_sorted_sequence[sequence_length - 1]
    x_max = reverse_sorted_sequence[0]
    delta = (x_max - x_min) / k

    numbers_in_intervals = array('i')
    for i in range(k):
        cur_range_count = 0
        cur_range_max = x_min + (i + 1) * delta
        while len(reverse_sorted_sequence) > 0 \
                and reverse_sorted_sequence[len(reverse_sorted_sequence) - 1] <= cur_range_max:
            reverse_sorted_sequence.pop()
            cur_range_count += 1
        numbers_in_intervals.append(cur_range_count)

    numbers_in_intervals[k - 1] += len(reverse_sorted_sequence)

    plt.hist(numbers_in_intervals, normed=True, bins=k)
    plt.show()

if __name__ == "__main__":
    main()

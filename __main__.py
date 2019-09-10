import argparse
from generators.LehmerSequence import LehmerSequence
from SequenceAnalyzer import SequenceAnalyzer
import matplotlib.pyplot as plt
import matplotlib
from array import array


def draw_chart(sequence, intervals_count=20):
    reverse_sorted_sequence = sorted(sequence)
    reverse_sorted_sequence.reverse()
    sequence_length = len(sequence)

    x_min = reverse_sorted_sequence[sequence_length - 1]
    x_max = reverse_sorted_sequence[0]
    delta = (x_max - x_min) / intervals_count

    intervals_sizes = array('i')
    for i in range(intervals_count):
        cur_range_size = 0
        cur_range_max = x_min + (i + 1) * delta
        while len(reverse_sorted_sequence) > 0 \
                and reverse_sorted_sequence[len(reverse_sorted_sequence) - 1] <= cur_range_max:
            reverse_sorted_sequence.pop()
            cur_range_size += 1
        intervals_sizes.append(cur_range_size)

    intervals_sizes[intervals_count - 1] += len(reverse_sorted_sequence)

    labels = []
    for i in range(intervals_count):
        labels.append(str(x_min + i * delta)[:5])

    matplotlib.rcParams['toolbar'] = 'None'
    chart = plt.gca()
    chart.bar(range(intervals_count), intervals_sizes)
    chart.set_xticklabels(labels)
    plt.grid(True)
    plt.show()

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

    print("Оценки:")
    print("\tматематического ожидания: ", analyzer.get_expected_value_estimate())
    print("\tдисперсии: ", analyzer.get_variance_estimate())
    print("\tсреднего квадратичного отклонения: ", analyzer.get_standard_deviation_estimate())

    period_length = analyzer.get_period_length()
    aperiodicity_interval_length = analyzer.get_aperiodicity_interval_length()
    print("Длина периода: " + str(period_length) if period_length != 0 else "Периода нет")
    print("Длина отрезка апериодичности: ", aperiodicity_interval_length)

    print("Значение косвенного признака: ", analyzer.get_indirect_sign())

    draw_chart(sequence)

if __name__ == "__main__":
    main()

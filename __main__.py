import argparse
from RandomGenerators import LehmerUniformDistributionGenerator
from SequenceAnalyzer import SequenceAnalyzer
import matplotlib.pyplot as plt


def draw_chart(sequence, intervals_count=20):
    plt.rcParams['patch.force_edgecolor'] = True
    plt.rcParams['toolbar'] = 'None'
    plt.hist(sequence, bins=intervals_count)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', type=int, required=True, help='value of a', dest='a')
    parser.add_argument('-m', action='store', type=int, required=True, help='value of m', dest='m')
    parser.add_argument('-r0', action='store', type=int, required=True, help='value of R0', dest='r0')
    parser.add_argument('-l', '--length', action='store', type=int, required=True,
                        help='generated sequence length', dest='length')
    args = parser.parse_args()

    lehmer_generator = LehmerUniformDistributionGenerator(args.a, args.m, args.r0)
    sequence = lehmer_generator.get_sequence(args.length)

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

import argparse
from RandomGenerators import LehmersUniformDistributionGenerator
from RandomGenerators import UniformDistributionGenerator
from RandomGenerators import GaussianDistributionGenerator
from RandomGenerators import ExponentialDistributionGenerator
from RandomSequencesAnalyzers import LehmersUniformSequenceAnalyzer, RandomSequenceAnalyzer
import matplotlib.pyplot as plt


def get_lehmers_generator(arguments_parser):
    arguments_parser.add_argument('-a', action='store', type=int, required=True, help='value of a', dest='a')
    arguments_parser.add_argument('-m', action='store', type=int, required=True, help='value of m', dest='m')
    arguments_parser.add_argument('-r0', action='store', type=int, required=True, help='value of R0', dest='r0')
    args = arguments_parser.parse_args()
    return LehmersUniformDistributionGenerator(args.a, args.m, args.r0)


def get_uniform_generator(arguments_parser):
    arguments_parser.add_argument('--min', action='store', type=float, required=True, help='minimum value', dest='min')
    arguments_parser.add_argument('--max', action='store', type=float, required=True, help='maximum value', dest='max')
    lehmers_generator = get_lehmers_generator(arguments_parser)
    args = arguments_parser.parse_args()
    return UniformDistributionGenerator(args.min, args.max, lehmers_generator)


def get_gaussian_generator(arguments_parser):
    arguments_parser.add_argument('--expected-value', action='store', type=float, required=True, help='expected value',
                                  dest='expected_value')
    arguments_parser.add_argument('--standard-deviation', action='store', type=float, required=True,
                                  help='standard deviation', dest='standard_deviation')
    arguments_parser.add_argument('--uniform-per-generated', action='store', type=int, required=False, default=6,
                                  help='uniform distributed numbers count per generated one', dest='uniform_count')
    lehmers_generator = get_lehmers_generator(arguments_parser)
    args = arguments_parser.parse_args()
    return GaussianDistributionGenerator(args.expected_value, args.standard_deviation, lehmers_generator,
                                         args.uniform_count)


def get_exponential_generator(arguments_parser):
    arguments_parser.add_argument('--param', action='store', type=float, required=True,
                                  help='exponential distribution parameter', dest='param')
    lehmers_generator = get_lehmers_generator(arguments_parser)
    args = arguments_parser.parse_args()
    return ExponentialDistributionGenerator(args.param, lehmers_generator)


def get_gamma_generator(arguments_parser):
    arguments_parser.add_argument('--param_nu', action='store', type=float, required=True,
                                  help='gamma parameter nu', dest='param_nu')
    arguments_parser.add_argument('--param_lambda', action='store', type=float, required=True,
                                  help='gamma parameter lambda', dest='param_lambda')
    lehmers_generator = get_lehmers_generator(arguments_parser)
    args = arguments_parser.parse_args()
    return GammaDistributionGenerator(args.param, lehmers_generator)


def get_triangle_generator(arguments_parser):
    arguments_parser.add_argument('--param_a', action='store', type=float, required=True,
                                  help='triangle parameter a', dest='param_a')
    arguments_parser.add_argument('--param_b', action='store', type=float, required=True,
                                  help='triangle parameter b', dest='param_b')
    lehmers_generator = get_lehmers_generator(arguments_parser)
    args = arguments_parser.parse_args()
    return TriangleDistributionGenerator(args.param, lehmers_generator)


def get_simpsons_generator(arguments_parser):
    return SimpsonDistributionGenerator(get_uniform_generator(arguments_parser))

def draw_chart(sequence, intervals_count=20):
    plt.rcParams['patch.force_edgecolor'] = True
    plt.rcParams['toolbar'] = 'None'
    plt.hist(sequence, bins=intervals_count)
    plt.show()


def main():
    generator_providers = {'lehmers': get_lehmers_generator, 'uniform': get_uniform_generator,
                           'gaussian': get_gaussian_generator, 'exponential': get_exponential_generator,
                           'gamma': get_gamma_generator, 'triangle': get_triangle_generator,
                           'simpsons': get_simpsons_generator}

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distribution', action='store', required=True, help='distribution type',
                        choices=generator_providers.keys(), dest='distribution')
    args = parser.parse_known_args()[0]

    parser.add_argument('-l', '--length', action='store', type=int, required=True,
                        help='generated sequence length', dest='length')
    sequence_generator = generator_providers[args.distribution](parser)
    args = parser.parse_args()
    sequence = sequence_generator.get_sequence(args.length)

    is_lehmers = isinstance(sequence_generator, LehmersUniformDistributionGenerator)
    if is_lehmers:
        analyzer = LehmersUniformSequenceAnalyzer(sequence)
    else:
        analyzer = RandomSequenceAnalyzer(sequence)

    print("Оценки:")
    print("\tматематического ожидания: ", analyzer.get_expected_value_estimate())
    print("\tдисперсии: ", analyzer.get_variance_estimate())
    print("\tсреднего квадратичного отклонения: ", analyzer.get_standard_deviation_estimate())

    if is_lehmers:
        period_length = analyzer.get_period_length()
        aperiodicity_interval_length = analyzer.get_aperiodicity_interval_length()
        print("Длина периода: " + str(period_length) if period_length != 0 else "Периода нет")
        print("Длина отрезка апериодичности: ", aperiodicity_interval_length)

        print("Значение косвенного признака: ", analyzer.get_indirect_sign())

    draw_chart(sequence)


if __name__ == "__main__":
    main()

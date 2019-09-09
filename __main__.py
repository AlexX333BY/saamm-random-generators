import argparse
from generators.LehmerSequence import LehmerSequence
from SequenceAnalyzer import SequenceAnalyzer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', type=int, required=True, help='value of a')
    parser.add_argument('-m', action='store', type=int, required=True, help='value of m')
    parser.add_argument('-r0', action='store', type=int, required=True, help='value of R0')
    parser.add_argument('-l', '--length', action='store', type=int, required=True, \
        help='generated sequence length', dest='length')
    args = parser.parse_args()
    
    lehmer_generator = LehmerSequence(args.a, args.m, args.r0)
    sequence = lehmer_generator.provide_sequence(args.length)
    
    analyzer = SequenceAnalyzer(sequence)

if __name__ == "__main__":
    main()

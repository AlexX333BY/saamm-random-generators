import math


class RandomSequenceAnalyzer:
    def __init__(self, sequence):
        self.__sequence = sequence

    def get_expected_value_estimate(self):
        return sum(self.__sequence) / len(self.__sequence)

    def get_variance_estimate(self):
        sum = 0
        expected_value_estimate = self.get_expected_value_estimate()
        for value in self.__sequence:
            sum += (value - expected_value_estimate) ** 2
        return sum / (len(self.__sequence) - 1)

    def get_standard_deviation_estimate(self):
        return math.sqrt(self.get_variance_estimate())

    def get_sequence(self):
        return self.__sequence


class LehmersUniformSequenceAnalyzer(RandomSequenceAnalyzer):
    def __init__(self, sequence):
        RandomSequenceAnalyzer.__init__(self, sequence)

    def get_period_length(self):
        try:
            sequence = self.get_sequence()
            sequence_length = len(sequence)
            return sequence[(sequence_length - 2)::-1].index(sequence[sequence_length - 1]) + 1
        except ValueError:
            return 0

    def get_aperiodicity_interval_length(self):
        period_length = self.get_period_length()
        aperiodicity_interval = 0
        sequence = self.get_sequence()
        if period_length != 0:
            first_duplicate_index = 0
            while sequence[first_duplicate_index] != sequence[first_duplicate_index + period_length]:
                first_duplicate_index += 1
            aperiodicity_interval = first_duplicate_index + period_length
        else:
            aperiodicity_interval = len(sequence)
        return aperiodicity_interval

    def get_indirect_sign(self):
        points_in_circle_count = 0
        sequence = self.get_sequence()
        sequence_length = len(sequence)
        for pair_no in range(0, sequence_length // 2):
            if (sequence[2 * pair_no] ** 2 + sequence[2 * pair_no + 1] ** 2) < 1:
                points_in_circle_count += 1
        return 2 * points_in_circle_count / sequence_length

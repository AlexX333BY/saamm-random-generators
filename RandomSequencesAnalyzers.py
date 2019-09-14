import math


class IRandomSequenceAnalyzer:
    def get_expected_value_estimate(self): raise NotImplementedError
    def get_variance_estimate(self): raise NotImplementedError
    def get_standard_deviation_estimate(self): raise NotImplementedError


class SequenceAnalyzer:
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

    def get_period_length(self):
        try:
            sequence_length = len(self.__sequence)
            return self.__sequence[(sequence_length - 2)::-1].index(self.__sequence[sequence_length - 1]) + 1
        except ValueError:
            return 0

    def get_aperiodicity_interval_length(self):
        period_length = self.get_period_length()
        aperiodicity_interval = 0
        if period_length != 0:
            first_duplicate_index = 0
            while self.__sequence[first_duplicate_index] != self.__sequence[first_duplicate_index + period_length]:
                first_duplicate_index += 1
            aperiodicity_interval = first_duplicate_index + period_length
        else:
            aperiodicity_interval = len(self.__sequence)
        return aperiodicity_interval

    def get_indirect_sign(self):
        points_in_circle_count = 0
        for pair_no in range(0, len(self.__sequence) // 2):
            if (self.__sequence[2 * pair_no] ** 2 + self.__sequence[2 * pair_no + 1] ** 2) < 1:
                points_in_circle_count += 1
        return 2 * points_in_circle_count / len(self.__sequence)

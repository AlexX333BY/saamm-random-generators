import math


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

    def __get_first_duplicate_index(self):
        cur_index = 0
        sequence_length = len(self.__sequence)
        while (cur_index < sequence_length) and (self.__sequence.count(self.__sequence[cur_index]) < 2):
            cur_index += 1
        return cur_index if cur_index < sequence_length else -1

    def get_period_length(self):
        first_duplicate_index = self.__get_first_duplicate_index()
        if first_duplicate_index != -1:
            second_duplicate_index = self.__sequence[(first_duplicate_index + 1):] \
                .index(self.__sequence[first_duplicate_index]) + first_duplicate_index + 1
            return second_duplicate_index - first_duplicate_index
        else:
            return 0

    def get_aperiodicity_interval_length(self):
        first_duplicate_index = self.__get_first_duplicate_index()
        return first_duplicate_index if first_duplicate_index != -1 else len(self.__sequence)

    def get_indirect_sign(self):
        points_in_circle_count = 0
        for pairNo in range(0, len(self.__sequence) // 2):
            if (self.__sequence[2 * pairNo] ** 2 + self.__sequence[2 * pairNo + 1] ** 2) < 1:
                points_in_circle_count += 1
        return 2 * points_in_circle_count / len(self.__sequence)

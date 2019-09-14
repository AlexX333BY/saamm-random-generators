from array import array
import math


class RandomGeneratorBase:
    def get_next(self): raise NotImplementedError

    def get_sequence(self, sequence_length):
        random_sequence = array('f')
        for i in range(sequence_length):
            random_sequence.append(self.get_next())
        return random_sequence


class LehmersUniformDistributionGenerator(RandomGeneratorBase):
    def __init__(self, a, m, r0):
        self.__a = a
        self.__m = m
        self.__r0 = r0
        self.__r = r0

    def get_next(self):
        self.__r = self.__a * self.__r % self.__m
        return self.__r / self.__m

    def reset(self):
        self.__r = self.__r0


class UniformDistributionGenerator(RandomGeneratorBase):
    def __init__(self, min_value, max_value, zero_to_one_uniform_generator):
        self.__min = min_value
        self.__max = max_value
        self.__uniform_generator = zero_to_one_uniform_generator

    def get_next(self):
        return self.__min + (self.__max - self.__min) * self.__uniform_generator.get_next()


class GaussianDistributionGenerator(RandomGeneratorBase):
    def __init__(self, expected_value, standard_deviation, zero_to_one_uniform_generator,
                 uniform_per_generated_numbers_count):
        self.__expected_value = expected_value
        self.__standard_deviation = standard_deviation
        self.__uniform_generator = zero_to_one_uniform_generator
        self.__uniform_per_generated = uniform_per_generated_numbers_count

    def get_next(self):
        uniform_sum = 0.0
        for i in range(self.__uniform_per_generated):
            uniform_sum += self.__uniform_generator.get_next()
        return self.__expected_value + self.__standard_deviation * math.sqrt(12 / self.__uniform_per_generated) \
               * (uniform_sum - self.__uniform_per_generated / 2)

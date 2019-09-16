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


class ExponentialDistributionGenerator(RandomGeneratorBase):
    def __init__(self, exponential_parameter, zero_to_one_uniform_generator):
        self.__parameter = exponential_parameter
        self.__uniform_generator = zero_to_one_uniform_generator

    def get_next(self):
        return -1 / self.__parameter * math.log1p(self.__uniform_generator.get_next())


class GammaDistributionGenerator(RandomGeneratorBase):
    def __init__(self, parametr_nu, parametr_lambda, zero_to_one_uniform_generator):
        self.__parametr_nu = parametr_nu
        self.__parametr_lambda = parametr_lambda
        self.__uniform_generator = zero_to_one_uniform_generator

    def get_next(self):
        uniform_composition = 1.0
        for i in range(self.__parametr_nu):
            uniform_composition *= self.__uniform_generator.get_next()
        return -1 / self.__parametr_lambda * math.log1p(uniform_composition)


class TriangleDistributionGenerator(RandomGeneratorBase):
    def __init__(self, parametr_a, parametr_b, zero_to_one_uniform_generator):
        self.__parametr_a = parametr_a
        self.__parametr_b = parametr_b
        self.__uniform_generator = zero_to_one_uniform_generator

    def get_next(self):
        r_1 = self.__uniform_generator.get_next()
        r_2 = self.__uniform_generator.get_next()
        return self.__parametr_a + (self.__parametr_b - self.__parametr_a) * max(r_1, r_2)


class SimpsonDistributionGenerator(RandomGeneratorBase):
    def __init__(self, uniform_generator):
        self.__uniform_generator = uniform_generator

    def get_next(self):
        y = self.__uniform_generator.get_next()
        z = self.__uniform_generator.get_next()
        return y + z

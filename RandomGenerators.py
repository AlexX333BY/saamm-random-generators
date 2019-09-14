from array import array


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

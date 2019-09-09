from generators.SequenceInterface import ISequence


class LehmerSequence(ISequence):
    def __init__(self, a, m, r0):
        self.__a = a
        self.__m = m
        self.__r0 = r0
        self.__r = r0
        
    def provide_sequence(self, sequence_length):
        random_sequence = []
        for i in range(sequence_length):
            random_sequence.append(self.next_number())
        return random_sequence
        
    def next_number(self):
        self.__r = self.__a * self.__r % self.__m
        return self.__r / self.__m
    
    def reset(self):
        self.__r = self.__r0

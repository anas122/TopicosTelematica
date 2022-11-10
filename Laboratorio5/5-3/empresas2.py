from mrjob.job import MRJob
from sympy import true

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        cp, price, date = line.split(',')
        yield cp, float(price)

    def reducer(self, cp, values):
        l = list(values)
        est = true
        pastValue = l[0]
        for value in l[1:]:
            if value < pastValue:
                est = False
            pastValue = value
        if est:
            yield cp, 'Estable'
        

if __name__ == '__main__':
    MRWordFrequencyCount.run()
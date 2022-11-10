from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        cp, price, date = line.split(',')
        yield cp,(price, date)

    def reducer(self, cp, values):
        l = list(values)
        dMin= min(l)
        dMax= max(l)
        yield cp ,("Peor dia",dMin,"Mejor dia",dMax)

if __name__ == '__main__':
    MRWordFrequencyCount.run()
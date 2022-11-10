from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        idemp, sector,salary,year = line.split(',')
        yield (idemp, sector)

    def reducer(self, idemp, values):
        l = list(values)
        yield (idemp, len(l))

if __name__ == '__main__':
    MRWordFrequencyCount.run()
from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user, movie, cal, gender, date= line.split(',')
        
        yield date , 1

    def reducer(self,date, values):
        yield None, (sum(values), date)

    def reducer2(self, _, values):
        yield 'Dia que se vieron mas peliculas', max(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()
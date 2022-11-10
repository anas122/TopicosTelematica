from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user, movie, cal, gender, date= line.split(',')
        
        yield date , float(cal)

    def reducer(self,date, values):
        l = list(values)
        pro = sum(l)/len(l)
        yield None, (pro, date)

    def reducer2(self, _, values):
        yield 'Dia con peores calificaciones', min(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()
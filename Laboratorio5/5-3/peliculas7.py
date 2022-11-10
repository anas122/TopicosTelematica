from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user, movie, cal, gender, date = line.split(',')
       
        yield (movie, gender),float(cal)

    def reducer(self, genpel, values):
        l = list(values)
        yield genpel, sum(l)/len(l)

    def mapper2(self, genpel, value):
        yield genpel[1], (value, genpel[0])

    def reducer2(self, gender, values):
        l = list(values)
        yield gender, ("Peor pelicula: ", min(l), "mejor pelicula: ", max(l))

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(mapper=self.mapper2, reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()
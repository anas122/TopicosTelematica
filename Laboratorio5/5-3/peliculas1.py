from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user,movies,cal,gender,date = line.split(',')
        yield user, float(cal)

    def reducer(self, user, values):
        l = list(values)
        pro = sum(l) / len(l)
        yield user, ("calificacion promedio",pro,"peliculas vistas",len(l))

if __name__ == '__main__':
    MRWordFrequencyCount.run()
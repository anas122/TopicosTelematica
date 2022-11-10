from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user,movie,cal,gender,date = line.split(',')
        yield movie, (user ,float(cal))

    def reducer(self, movie, values):
        l = list(values)
        pro = sum([x[1] for x in l])/len(l)
        yield movie, ("calificacion promedio",pro,"numero de usuarios que vieron",len(l))

if __name__ == '__main__':
    MRWordFrequencyCount.run()
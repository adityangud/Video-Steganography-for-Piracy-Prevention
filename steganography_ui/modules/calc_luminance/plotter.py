from matplotlib import pyplot
import sys

def plotter(filename):
    fp = open(filename)
    values = eval(fp.read())
    lines = pyplot.plot(range(0, len(values)), values)
    pyplot.savefig(filename + '.png')

if __name__ == '__main__':
    filename = sys.argv[1]
    plotter(filename)

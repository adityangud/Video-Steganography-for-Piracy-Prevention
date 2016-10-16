from matplotlib import pyplot
import sys

def plotter(filename, save_name=None):
    print "plotting %s" % filename
    fp = open(filename)
    values = eval(fp.read())
    lines = pyplot.plot(range(0, len(values)), values)
    pyplot.title(filename)
    if save_name:
        pyplot.savefig(save_name)
    else:
        pyplot.show()
    pyplot.gcf().clear()

if __name__ == '__main__':
    filename = sys.argv[1]
    save_name = None
    if len(sys.argv) == 3:
        save_name = sys.argv[2]

    plotter(filename, save_name)

from os.path import splitext as _splitext

def _load_data(filename):
    fp = open(filename)
    data = fp.read()
    values = eval(data)
    fp.close()
    return values

def _store_data(values=[], filename="/tmp/filename"):
    fp = open(filename, "w")
    fp.write("%s" % repr(values))
    fp.close()

def differential(filename):
    '''
    computes x[i+1] - x[i]
    '''

    values = _load_data(filename)

    difference_list = []
    for i in xrange(1, len(values)):
        # x2 - x1
        difference_list.append(values[i] - values[i-1])

    filename, extension = _splitext(filename)
    filename = filename + "_d" + extension

    _store_data(difference_list, filename)
    return filename

def mean(filename):
    '''
    computes x[i] - mean(x)
    '''

    values = _load_data(filename)

    mean = sum(values) / len(values)

    mean_list = []
    for i in values:
        mean_list.append(i - mean)

    filename, extension = _splitext(filename)
    filename = filename + "_mean" + extension

    _store_data(mean_list, filename)
    return filename

def normalize(filename):
    '''
    normalizes the graph to a certain range
    TODO: make the normalization relative to two graphs
    '''
    values = _load_data(filename)
    max_val = max(values)
    min_val = min(values)

    normalized_list = []
    for i in values:
        normalized_list.append( (float(i - min_val) / (max_val - min_val)) * 100)

    filename, extension = _splitext(filename)
    filename = filename + "_normalized" + extension

    _store_data(normalized_list, filename)
    return filename

def std_dev(filename):
    '''
    computes x[i] - standard_deviation
    '''
    #TODO complete..


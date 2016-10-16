
def decoder_preprocessing_spidey(a, b):
    a = a[75:-75]

    avg_b_74 = float(sum(b[:74]))/len(b[:74])
    for i in xrange(len(b)):
        b[i] = b[i] - avg_b_74

    avg_a = float(sum(a))/len(a)
    avg_b = float(sum(b))/len(b)

    b = b[74:]

    new_avg_b = float(sum(b))/len(b)
    length = len(b)
    a = a[:length]

    for i in xrange(length):
        a[i] = a[i] - avg_a
        b[i] = b[i] - new_avg_b

    return (a, b)

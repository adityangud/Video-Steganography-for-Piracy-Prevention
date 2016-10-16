import Image
import sys

# luminance per pixel formula
luma = lambda r,g,b: long((0.2126 * r) + (0.7152 * g) + (0.0722 * b))

def get_filenames(filenames_file):
    '''
    returns the filenames from the file one by one
    '''
    fp = open(filenames_file)
    data = fp.read()
    fp.close()

    lines = [i.strip() for i in data.split('\n')]
    return [i for i in lines if i != '']

def calc_luma(filename):
    '''
    Reads filename as an image and calculates average luminance
    '''
    im = Image.open(filename)
    rows, cols = im.size
    pixels = im.load()

    luma_sum = 0
    for i in xrange(rows):
        for j in xrange(cols):
            luma_sum += luma(*pixels[i, j])

    # avg luminance is sum / number of pixels
    return luma_sum / (rows * cols)


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print "usage python calc_luma.py <filename_containing_image_paths_to_process>"
        sys.exit(0)

    filenames_file = sys.argv[1]

    filenames = get_filenames(filenames_file)
    total = len(filenames)

    luma_list = []
    sys.stderr.write('0');
    sys.stderr.flush();
    i = 1.0

    for filename in get_filenames(filenames_file):
        sys.stderr.write('\r%d%%' % ((i / total ) * 100))
        sys.stderr.flush()
        luma_list.append(calc_luma(filename))
        i = i + 1.0

    sys.stderr.write('\r')
    sys.stderr.flush()
    print repr(luma_list)

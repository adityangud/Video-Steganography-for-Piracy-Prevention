import pyopencl as cl
import numpy
import Image
import time
import os
from humanize import naturalsize, naturaltime
import sys

if len(sys.argv) >= 4:
    target_dir = sys.argv[2]
    target_name = sys.argv[3]
else:
    print "give a target_dir"
    sys.exit()


output_file = open('%s' % (os.path.join(target_dir, target_name)), 'w')
output_file.write('hello')

ACTUAL_START_TIME = time.time()

img_names_file = sys.argv[1]
img_names = open(img_names_file).read()
img_names_total = [i.strip() for i in img_names.split('\n') if i.strip() != '']

numpy.set_printoptions(threshold=numpy.nan)

while img_names_total:
    img_names = img_names_total[:20]
    img_names_total = img_names_total[20:]
    print "processing ", img_names
    if not img_names:
        break

    if len(img_names) > 20:
        print "Only 20 aloud"
        sys.exit()

    img1 = Image.open(img_names[0])
    width, height = img1.size
    img_arr = numpy.asarray(img1).astype(numpy.uint8);
    imgsize = img_arr.nbytes
    dim = img_arr.shape
    host_arr = img_arr.reshape(-1);

    for name in img_names[1:]:
        img1 = Image.open(name)
        img_arr = numpy.asarray(img1).astype(numpy.uint8);
        host_arr = numpy.concatenate((host_arr, img_arr.reshape(-1)));

    host_arr = host_arr.astype(numpy.uint8)
    print dim
    new_dim = (len(img_names), dim[0], dim[1], dim[2])
    print "new dimensions are", new_dim

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=host_arr)

    luma_values_array = numpy.zeros((len(img_names), ), dtype=numpy.long)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, luma_values_array.nbytes)


    print "[%d] Takes " % len(img_names) , naturalsize(luma_values_array.nbytes)

    kernel_code = open("calc_luma.cl").read() % (new_dim[1], new_dim[2], new_dim[3])
    prg1 = cl.Program(ctx, kernel_code).build()

    stime = time.time()
    prg1.calc_luma(queue, (len(img_names),) , None, a_buf, dest_buf)
    etime = time.time()

    print "[%d] GPU takes " % len(img_names), naturaltime(etime - stime)

    cl.enqueue_copy(queue, luma_values_array, dest_buf)

    # result is a array of all images combined
    _index = 0
    size_slice = imgsize

    stime = time.time()
    print "Writing to file"
    for i in xrange(len(img_names)):
        output_file.write("%f\n" % (float(luma_values_array[i])/ (1920 * 1080)))

    etime = time.time()

    print "[%d] Saving takes " % len(img_names), naturaltime(etime - stime)
print "done"
ACTUAL_END_TIME = time.time()
print "Took %s " % naturaltime(ACTUAL_END_TIME - ACTUAL_START_TIME)

output_file.close()

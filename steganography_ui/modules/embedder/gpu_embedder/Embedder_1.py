import pyopencl as cl
import numpy
import Image
import time
import os
from humanize import naturalsize, naturaltime
import sys

if len(sys.argv) >= 3:
    target_dir = sys.argv[2]
else:
    print "give a target_dir"
    sys.exit()

ACTUAL_START_TIME = time.time()

img_names_file = sys.argv[1]
img_names = open(img_names_file).read()
img_names_total = [i.strip() for i in img_names.split('\n') if i.strip() != '']

numpy.set_printoptions(threshold=numpy.nan)

for step in xrange(300):
    img_names = img_names_total[step*20: (step+1) * 20]
    if not img_names:
        break

    if len(img_names) > 20:
        print "Only 20 aloud"
        sys.exit()

    img1 = Image.open(img_names[0])
    # new
    # img1 = img.convert("YCbCr")
    # end all img changed to img1
    width, height = img1.size
    img_arr = numpy.asarray(img1).astype(numpy.uint8);
    imgsize = img_arr.nbytes
    dim = img_arr.shape
    host_arr = img_arr.reshape(-1);

    for name in img_names[1:]:
        img1 = Image.open(name)
        # img1 = img.convert("YCbCr")
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
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, host_arr.nbytes)


    print "[%d] Takes " % len(img_names) , naturalsize(host_arr.nbytes)

    kernel_code = open("embed_1.cl").read() % (new_dim[1], new_dim[2], new_dim[3])
    prg1 = cl.Program(ctx, kernel_code).build()

    stime = time.time()
    prg1.embed_one(queue, (new_dim[0], new_dim[1], new_dim[2]) , None, a_buf, dest_buf)
    etime = time.time()

    print "[%d] GPU takes " % len(img_names), naturaltime(etime - stime)

    result = numpy.empty_like(host_arr)
    cl.enqueue_copy(queue, result, dest_buf)

    # result is a array of all images combined
    _index = 0
    size_slice = imgsize

    stime = time.time()
    for name in img_names:
        img_arr = result[_index * size_slice: (_index +1 )* size_slice]
        img_arr = img_arr.reshape(dim)
        img2 = Image.fromarray(img_arr)
        name, ext = os.path.splitext(name)
        name = os.path.basename(name)
        name = name + "embed_one.bmp"
        img2.save(os.path.join(target_dir, name))
        _index += 1

    etime = time.time()

    print "[%d] Saving takes " % len(img_names), naturaltime(etime - stime)
print "done"
ACTUAL_END_TIME = time.time()
print "Took %s " % naturaltime(ACTUAL_END_TIME - ACTUAL_START_TIME)

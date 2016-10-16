import os
import sys
import Image
import numpy as np
import scipy.ndimage

def embed_in_frame(current_img, prev_img, bit):
    w, h = current_img.size

    mu_min  = 1
    laplacian_matrix = np.array([[-1, -1, -1], [-1, -8, -1], [-1, -1, -1]])
    s = 0.025

    cur_img_arr = np.asarray(current_img)
    prev_img_arr = np.asarray(prev_img)

    lap_cur_img_arr = cur_img_arr.copy()
    scipy.ndimage.filters.laplace(cur_img_arr, lap_cur_img_arr)
    lap_cur_img_arr = s * lap_cur_img_arr

    _min = 10000
    _max = -9999

    for i in xrange(h):
        for j in xrange(w):
            abs_diff = int(cur_img_arr[i][j][0]) - int(prev_img_arr[i][j][0])
            abs_diff = abs(abs_diff)

            mu = mu_min + abs_diff
            v = min(mu, lap_cur_img_arr[i][j][0])

            if v < _min: _min = v
            if v > _max: _max = v

            if bit == 0: v = -v
            new_val = cur_img_arr[i][j][0] + v

            if new_val < 0: new_val = 0
            elif new_val > 255: new_val = 255

            cur_img_arr[i][j].put([0], new_val)

    print "Min: %d max: %d" % (_min, _max)
    return Image.fromarray(cur_img_arr, "YCbCr").convert("RGB")


def main():
    frame_text_file = sys.argv[1]
    output_folder = sys.argv[2]
    bit = sys.argv[3]

    if bit == '1': bit = 1
    else: bit = 0

    frame_list = open(frame_text_file).read().strip()
    frame_list = [i for i in frame_list.split('\n')]
    frame_list = [i for i in frame_list if i != '']

    prev_img = Image.open(frame_list[0])
    ycb_prev_img = prev_img.convert('YCbCr')

    for frame_name in frame_list:
        name, ext = os.path.splitext(os.path.basename(frame_name))
        output_name = os.path.join(output_folder, name + ("embed_%d" % bit) + ext)

        current_img = Image.open(frame_name)
        ycb_current_img = current_img.convert('YCbCr')

        new_img = embed_in_frame(ycb_current_img, ycb_prev_img, bit)
        new_img.save(output_name)

        prev_img = current_img
        ycb_prev_img = ycb_current_img


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Wrong usage"
        print "filename, outputdir, bit"
    else:
        main()


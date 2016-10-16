# take a bitstring, find the files, join using ffmpeg
import os
import sys
import glob
import json


BUCKET_SIZE = -1
NORMAL_SIZE = -1
BITSTRING_SIZE = -1
MIN_ROBUSTNESS_COUNT = -1

def setup_params():
    global BUCKET_SIZE, NORMAL_SIZE, BITSTRING_SIZE, MIN_ROBUSTNESS_COUNT
    fp = open('config.cfg')
    data = json.loads(fp.read())
    fp.close()

    BUCKET_SIZE = data['bucket_size']
    NORMAL_SIZE = data['normal_size']
    BITSTRING_SIZE = data['bitstring_size']
    MIN_ROBUSTNESS_COUNT = data['min_robustness_count']


def valid(bitstring):
    return ((bitstring.count('1') + bitstring.count('0')) == BITSTRING_SIZE)

def sufficient_frames(list_normal_files, list_one_files, list_zero_files):
    number_embed_frames = BUCKET_SIZE * BITSTRING_SIZE * MIN_ROBUSTNESS_COUNT + (2 * NORMAL_SIZE)

    if len(list_normal_files) < number_embed_frames: return False
    if len(list_one_files) < number_embed_frames: return False
    if len(list_zero_files) < number_embed_frames: return False

    return True

def find_robustness_degree(list_normal_files, list_one_files, list_zero_files):
    number_embed_frames = min(len(list_normal_files), len(list_one_files), len(list_zero_files))
    number_robust_embed_frames = number_embed_frames - (2 * NORMAL_SIZE)
    robustness_degree = number_robust_embed_frames / (BUCKET_SIZE * BITSTRING_SIZE)
    return int(robustness_degree)

def main():
    normal_folder = os.path.join(sys.argv[1], '*.bmp')
    one_folder = os.path.join(sys.argv[2], '*.bmp')
    zero_folder = os.path.join(sys.argv[3], '*.bmp')
    bitstring = sys.argv[4]

    output_folder = sys.argv[5]

    if not valid(bitstring):
        print "invalid bitstring"
        return

    list_normal_files = glob.glob(normal_folder)
    list_one_files = glob.glob(one_folder)
    list_zero_files = glob.glob(zero_folder)

    # keep in sorted order
    list_normal_files.sort()
    list_one_files.sort()
    list_zero_files.sort()

    if not sufficient_frames(list_normal_files, list_one_files, list_zero_files):
        print "Insufficient frames"
        return

    robustness_degree = find_robustness_degree(list_normal_files, list_one_files, list_zero_files)

    frame_number = 1
    frame_name = 'img_embed_%08d.bmp'
    frame_name = os.path.join(output_folder, frame_name)
    cmd_str = 'cp %s '+frame_name

    for i in xrange(NORMAL_SIZE):
        print cmd_str % (list_normal_files[frame_number - 1] , frame_number)
        frame_number = frame_number + 1

    for robust_count in xrange(robustness_degree):
        for i in bitstring:
            for ctr in xrange(BUCKET_SIZE):
                if i == '1':
                    print cmd_str % (list_one_files[frame_number - 1], frame_number)
                else:
                    print cmd_str % (list_zero_files[frame_number - 1], frame_number)

                frame_number = frame_number + 1

    for i in xrange(NORMAL_SIZE):
        print cmd_str % (list_normal_files[frame_number - 1] , frame_number)
        frame_number = frame_number + 1

    remaining_files = list_normal_files[frame_number - 1:]
    for i in xrange(len(remaining_files)):
        print cmd_str % (remaining_files[i], frame_number)
        frame_number = frame_number + 1


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "wrong usage"
        print "Normal folder one folder zero folder bitstring"
    else:
        setup_params()
        main()

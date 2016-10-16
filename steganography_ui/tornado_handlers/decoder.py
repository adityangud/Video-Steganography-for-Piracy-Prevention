#take input of two .repr files of luma, output the embedded code in them
import os
import sys
from collections import Counter

BUCKET_SIZE = -1
BITSTRING_SIZE = -1
NORMAL_SIZE = -1
MIN_ROBUSTNESS_COUNT = -1

def get_embedded_string_from_bitstring(input_str, ROBUSTNESS_DEGREE):
    robustness_arr = []
    for i in xrange(ROBUSTNESS_DEGREE):
        bitstring = input_str[i*BITSTRING_SIZE*BUCKET_SIZE:(i+1)*BITSTRING_SIZE*BUCKET_SIZE]
        bit_arr = []
        for j in xrange(BITSTRING_SIZE):
            bit = bitstring[j*BUCKET_SIZE:(j+1)*BUCKET_SIZE]
            if not bit:
                print "%dth iteration" % j
                print "j * bitstring size = "% (j * BITSTRING_SIZE)
            the_bit = max([(v,k) for k,v in Counter(bit).items()])[-1]
            bit_arr.append(the_bit)
        robustness_arr.append(bit_arr)

    robustness_arr = zip(*robustness_arr)

    final_output = ''
    for i in robustness_arr:
        the_bit = max([(v,k) for k,v in Counter(i).items()])[-1]
        final_output += the_bit


    return final_output

def sufficient_frames(list_normal_files, list_recording_files):
    number_embed_frames = (2 * NORMAL_SIZE) + BUCKET_SIZE * BITSTRING_SIZE * MIN_ROBUSTNESS_COUNT
    print "Number of embed frames required is %d " % number_embed_frames
    if len(list_normal_files) > number_embed_frames: return True
    if len(list_recording_files) > number_embed_frames: return True

def find_robustness_degree(list_normal_files, list_recording_files):
    number_embed_frames = min(len(list_normal_files), len(list_recording_files))
    number_robust_embed_frames = number_embed_frames - (2 * NORMAL_SIZE)
    robustness_degree = number_robust_embed_frames / (BUCKET_SIZE * BITSTRING_SIZE)
    return int(robustness_degree)

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

def main_decoder(params, list_normal_files, list_recording_files):

    global BUCKET_SIZE, MIN_ROBUSTNESS_COUNT, BITSTRING_SIZE, NORMAL_SIZE
    BUCKET_SIZE = params['bucket_size']
    MIN_ROBUSTNESS_COUNT = params['min_robustness_count']
    BITSTRING_SIZE = params['bitstring_size']
    NORMAL_SIZE = params['normal_size']

    if params['name'] == 'spidey':
        list_normal_files, list_recording_files = decoder_preprocessing_spidey(list_normal_files, list_recording_files)
    # fp_normal = open(sys.argv[1])
    # fp_recording = open(sys.argv[2])
    # list_normal_files = eval(fp_normal.read())
    # list_recording_files = eval(fp_recording.read())

    if not sufficient_frames(list_normal_files, list_recording_files):
        print "Insufficient frames"
        return
    robustness_degree = find_robustness_degree(list_normal_files, list_recording_files)

    #may need to put a sync between the two lists, but for now assuming that both are perfectly synced and keeping only equal elements
    len_frames = min(len(list_normal_files), len(list_recording_files))
    list_normal_files = list_normal_files[:len_frames]
    list_recording_files = list_recording_files[:len_frames]

    #trimming the normal frames from both
    list_normal_files = list_normal_files[NORMAL_SIZE: len(list_normal_files) - NORMAL_SIZE]
    list_recording_files = list_recording_files[NORMAL_SIZE: len(list_recording_files) - NORMAL_SIZE]

    embedded_data = ""
    for i,j in zip(list_normal_files, list_recording_files):
        if i > j: embedded_data += '0'
        elif i < j: embedded_data += '1'

    return get_embedded_string_from_bitstring(embedded_data, robustness_degree - 1)


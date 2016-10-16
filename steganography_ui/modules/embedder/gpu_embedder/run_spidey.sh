#!/usr/bin/env bash

export PYOPENCL_CTX='0';

ls /media/Seagate__/SplitFrames/Spidey/Frames/*.bmp > spider_frames.txt

python Embedder_1.py spider_frames.txt /media/Seagate___/EmbedFrames/Spidey/embed_1

python Embedder_0.py spider_frames.txt /media/Seagate___/EmbedFrames/Spidey/embed_0


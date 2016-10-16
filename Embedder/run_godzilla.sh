#!/usr/bin/env bash

export PYOPENCL_CTX='0';

ls /media/Seagate__/SplitFrames/Godzilla/Frames/*.bmp > godzilla_frames.txt

python Embedder_0.py godzilla_frames.txt /media/Seagate__/EmbedFrames/Godzilla/embed_0

python Embedder_1.py godzilla_frames.txt /media/Seagate___/EmbedFrames/Godzilla/embed_1


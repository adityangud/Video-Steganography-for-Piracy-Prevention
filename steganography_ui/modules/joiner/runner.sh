#!/usr/bin/env bash
mkdir joiner_result
normal_folder="/media/anthony/Seagate/SplitFrames/Spidey/Frames/"
zero_folder="/media/anthony/Seagate3/EmbedFrames/Spidey/embed_0/";
one_folder="/media/anthony/Seagate3/EmbedFrames/Spidey/embed_1/"
bitstring="11110000";
output_folder="joiner_result";

python joiner.py $normal_folder $one_folder $zero_folder $bitstring $output_folder > instructions.sh
echo "done run bash instructions.sh"
exit
bash instructions.sh
cd $output_folder
ffmpeg -qscale 1 -r 25 -b 32028 -i img_embed_%08d.bmp output.mp4

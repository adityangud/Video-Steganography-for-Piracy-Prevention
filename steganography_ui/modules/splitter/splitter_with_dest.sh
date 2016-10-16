#!/usr/bin/env bash
filename=$(basename "$1");
extension="${filename##*.}";
filename="${filename%.*}";
pretty_separator="-----------------------------------------------------------------------";
image_dir=$2;

if [[ -z "$1" ]]; then
    echo "Usage: ./anto_script.sh video_file destination_folder [framerate=25]"
    exit;
fi
if [[ -z "$3" ]]; then
    frame_rate=25;
else
    frame_rate=$3;
fi

echo $pretty_separator;

if [ -d "$image_dir" ]; then
    echo "Directory $image_dir already exists";
    read -p "Delete directory and continue Y/n? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        # do dangerous stuff
        rm -rf "$image_dir";
    else
        echo "remove and run this again ";
        exit;
    fi
fi
echo "creating $image_dir";
mkdir "$image_dir";

echo "running ffmpeg on $filename storing images in $image_dir, modify script to change framerate, default $frame_rate";
echo $pretty_separator;

ffmpeg -i "$1" -r $frame_rate -f image2 "$image_dir/image_%08d.bmp";

echo $pretty_separator;
echo "done";

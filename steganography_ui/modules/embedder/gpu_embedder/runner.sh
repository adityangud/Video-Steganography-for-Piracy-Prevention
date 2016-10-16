xmen="/media/My Passport/Anthony/Steganography/Frames/xmen/";
dragon="/media/My Passport/Anthony/Steganography/Frames/dragon/";
captain="/media/My Passport/Anthony/Steganography/Frames/captain_america/";
spider="/media/My Passport/Anthony/Steganography/Frames/spiderman_trailer_2/";

additional="Original/*.bmp"

ls "$xmen"$additional > xmen_filenames.txt
ls "$captain"$additional > dragon_filenames.txt
ls "$captain"$additional > captain_america_filenames.txt
ls "$spider"$additional > spiderman_trailer_2_filenames.txt


echo "DRAGON";
export PYOPENCL_CTX='0';
python Embedder_1.py dragon_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/dragon/Embed_1/"
export PYOPENCL_CTX='0';
python Embedder_0.py dragon_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/dragon/Embed_0/"


echo "SPIDERMAN";
export PYOPENCL_CTX='0';
python Embedder_1.py spiderman_trailer_2_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/spiderman_trailer_2/Embed_1/"
export PYOPENCL_CTX='0';
python Embedder_0.py spiderman_trailer_2_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/spiderman_trailer_2/Embed_0/"


echo "captain_america";
export PYOPENCL_CTX='0';
python Embedder_1.py captain_america_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/captain_america/Embed_1/"
export PYOPENCL_CTX='0';
python Embedder_0.py captain_america_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/captain_america/Embed_0/"

echo "xmen";
export PYOPENCL_CTX='0';
python Embedder_1.py xmen_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/xmen/Embed_1/"
export PYOPENCL_CTX='0';
python Embedder_0.py xmen_filenames.txt "/media/My Passport/Anthony/Steganography/Frames/xmen/Embed_0/"


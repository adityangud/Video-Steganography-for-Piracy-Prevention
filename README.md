# Video-Steganography-for-Piracy-Prevention

Video Steganography and Digital Watermarking are domains of Computer Science that
deal with data confidentiality and aim to hide information inside a video, such that it is hidden
in plain sight, but retrievable only by the intended user. Thus they can be used for digital
copyrighting of videos and tackling video piracy, which has become a huge problem in the
entertainment industry. It is reported that the movie industry loses $25 billion a year to it. There
are several companies that offer Direct to Home (DTH) video such as Netflix, Hulu, which
allow viewers to stream and view movies and TV shows on their websites. While there is
current technology to prevent direct screen capture, there is no check to prevent video recording
using an external device. Since the paid websites like Netflix keep account and banking details
of each movie transaction, it becomes easy to track the person buying the movie. Thus by
embedding information unique to a transaction (a transaction identifier) into the video using
video steganography techniques, and the retrieval of the same from any pirated or recreated
copy of that video, it is possible to identify the video pirate.


A 64 bit unique transaction identifier is embedded into every movie by altering the
luminance values of the frames of the video, which persists through recordings and corruption,
and thus each viewer of a video is served a unique copy of that video. Thus any recording of
that video can still be traced back to the owner. A bit value of 1 is represented by an increase,
and 0 by a decrease in the luminance of the frame based on global and local factors of the pixels
of that frame. The transaction identifier is embedded across multiple frames and multiple times
in order to achieve robustness and survive any intentional and unintentional attacks to corrupt
the data. Thus a steganography system is developed using Python and harnesses the power of
the GPU using OpenCL, and built in Ubuntu 13.04.


This novel steganography algorithm is successful in its approach towards embedding
and detecting data in videos of duration 2 minutes or more. A 100% accuracy of embedding
and extraction of a 32-bit string is achieved, and a correspondence factor of 87.19% between
the original video and recording is obtained. The degree of robustness depends on the nature
and length of the video, but high repetition could degrade the video quality, and thus a middle
ground is to be achieved. The system developed provides a great base towards video piracy
prevention and opens up avenues for further research and development.

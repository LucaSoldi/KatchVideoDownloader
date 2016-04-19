# KatchVideoDownloader
Simple Python3 script to download video from katch.me

The usage is very simple:

> python3 katch.py -i < katch_url > -o < output_file >

-i (--input): url of katch.me video (ex: https://katch.me/user/v/id-video-katch)

-o (--output): name of output video saved in your folder (ex: output.mp4)

This script use **ffmpeg** to concat chunks provide by katch.me, install it before use this script :)

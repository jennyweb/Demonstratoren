#!/bin/sh
# see http://www.mplayerhq.hu/DOCS/HTML/de/mencoder.html

# set framerate to 8 if not otherwise specified
framerate=${1:-30}

PNG_DIR=pic
VIDEO_FILE=movie.avi

mencoder -of avi -ovc x264 -fps $framerate -nosound -o $VIDEO_FILE mf://$PNG_DIR/\*.png


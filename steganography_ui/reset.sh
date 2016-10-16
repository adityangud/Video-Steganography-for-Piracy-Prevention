#!/usr/bin/env bash
bash backup.sh
tree -L 1 images/ uploads/ video/
rm -f images/*.png
rm -f uploads/*
rm -f video/*
tree -L 1 images/ uploads/ video/

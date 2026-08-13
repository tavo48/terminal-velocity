#!/bin/zsh
# ssim.sh A.png B.png — scale-normalised SSIM. Prints just the All: score.
F=/opt/homebrew/bin/ffmpeg
$F -i "$1" -i "$2" -lavfi \
  "[0:v]scale=960:540:force_original_aspect_ratio=disable,format=gray[a];\
   [1:v]scale=960:540:force_original_aspect_ratio=disable,format=gray[b];\
   [a][b]ssim" -f null - 2>&1 | grep -o 'All:[0-9.]*' | head -1

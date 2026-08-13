#!/bin/zsh
# chain.sh <name> <url> — download a clip, extract its literal last frame, build a
# motion contact sheet, and report the internal-continuity SSIM samples.
# The last frame is what the NEXT clip must pin its start to (playbook §2).
set -e
A=/Users/octavioortega/Desktop/borra/terminal-velocity/assets
F=/opt/homebrew/bin/ffmpeg
N=$1; URL=$2

curl -s -A "Mozilla/5.0" -o $A/$N.mp4 "$URL"
$F -y -loglevel error -sseof -0.05 -i $A/$N.mp4 -update 1 -q:v 1 $A/$N-last.png
$F -y -loglevel error -i $A/$N.mp4 -vf "select=eq(n\,0)" -frames:v 1 -q:v 1 $A/$N-first.png
$F -y -loglevel error -i $A/$N.mp4 -vf "select='not(mod(n,12))',scale=300:-1,tile=6x1" -frames:v 1 $A/$N-motion.png

echo "$N: $(ls -lh $A/$N.mp4 | awk '{print $5}')  $($F -i $A/$N.mp4 2>&1 | grep -o '[0-9]*x[0-9]*' | head -1)"

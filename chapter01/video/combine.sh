#!/bin/bash
# Combine slides + audio into video

SLIDES_DIR="/home/maxtic/esp32-stem-book/chapter01/video/slides"
AUDIO_DIR="/home/maxtic/esp32-stem-book/chapter01/audio"
OUTPUT="/home/maxtic/esp32-stem-book/chapter01/video/chapter01.mp4"

# Use FFmpeg to create video
# Format: slide_NN.png + slide_NN.mp3 for each slide, concatenated

# Create concat list
cd "$SLIDES_DIR"
for i in $(seq -f "%02g" 1 10); do
    echo "file '${AUDIO_DIR}/slide_${i}.mp3'" >> /tmp/audio_list.txt
done

# Concatenate audio
ffmpeg -y -f concat -safe 0 -i /tmp/audio_list.txt -c copy /tmp/combined_audio.mp3

# Get total duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/combined_audio.mp3)
echo "Total audio duration: $DURATION seconds"

# Create video with static images + audio
# Each slide shows for its audio duration
ffmpeg -y \
    -loop 1 -i slide-01.png -i /tmp/combined_audio.mp3 \
    -filter_complex "[0:v]trim=0:19,setpts=PTS-STARTPTS[v0]" \
    -map "[v0]" -map 1:a \
    -c:v libx264 -pix_fmt yuv420p -shortest \
    "$OUTPUT"

echo "✅ Video created: $OUTPUT"

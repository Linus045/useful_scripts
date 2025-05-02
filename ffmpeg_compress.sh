#!/bin/bash

filename="$1"
fileextension="${filename##*.}"

# compresses video files using ffmpeg
# the idea is to set this as  command inside the file manager e.g. thunar 
# to quickly compress video files

# Check if the file is mp4 or mkv

if [[ "$fileextension" != "mp4" && "$fileextension" != "mkv" ]]; then
  echo "Error: The file must be an mp4 or mkv file."
  notify-send "Error: The file must be an mp4 or mkv file."
  exit 1
fi

output=$(ffmpeg -hide_banner -loglevel error -y -i  "${filename}" "${filename%.*}_compressed.$fileextension" 2>&1)
if [ $? -ne 0 ]; then
	notify-send "Error: Compression failed." "$output"
	echo "Error: Compression failed." "$output"
  exit 1
fi

notify-send "Compression complete" "The file has been compressed and saved as ${filename%.*}_compressed.$fileextension"
echo "Compression complete" "The file has been compressed and saved as ${filename%.*}_compressed.$fileextension"

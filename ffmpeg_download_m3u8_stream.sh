#!/bin/bash
URL="$1"
OUTPUT="$2"


if [ -z "$URL" ] || [ -z "$OUTPUT" ]; then
	echo "Usage: $0 <m3u8_url> <output_file>"
	exit 1
fi

ffmpeg -i "$URL" -map 0:v -map 0:a -map "0:s?" -c copy -bsf:a aac_adtstoasc "${OUTPUT}"


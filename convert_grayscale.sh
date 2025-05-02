#!/bin/bash


if [ ! -d "input" ]; then
	echo "Please place your images in the 'input' directory."
	echo "Converted images will be saved in the 'output' directory."
	mkdir -p output
	mkdir -p input

	exit 1
fi

mask="____mask.png"
grayscaled="_____grayscaled.png"

for i in input/*.png; do
	echo "Processing $i"

	if [ "$i" == "$mask" ]; then
		continue
	fi

	if [ "$i" == "$grayscaled" ]; then
		continue
	fi

	filename="${i##*/}"

	magick "$i" \
		-colorspace gray -colors 16 \
		"$grayscaled"

	magick "$i" \
		-negate -fill "#808040" -colorize 100% \
		"$mask"

	magick "$grayscaled" \
		"$mask" \
		-colorspace sRGB \
		-compose Over -composite \
		-alpha remove -alpha off \
		-gravity Center -crop 3:4 -adaptive-resize 1072x1448^^! \
		"output/${filename%.*}_gray.bmp"

done

rm "$mask"
rm "$grayscaled"

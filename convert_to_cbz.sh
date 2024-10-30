#!/bin/bash

# See also: README_HakuNeko.md

# HowTo:
# Clone kcc from git and install the package (installing the package installs all required
# python libraries, alternatively you can just clone the repo and install the dependencies yourself)


directory=$1
if [ -z "$directory" ]; then
	echo "Please provide the directory that contains the manga volumes"
	echo "./convert_to_cbz.sh <PATH>"
	exit 0
fi


# -m specify manga (not comics, webtoons, etc.)
# -n no processing of files (no formatting, color changes etc.)
# -f CBZ convert to CBZ format
# -b batch mode to create a volume for each subdirectory
./kcc/kcc-c2e.py -m -n -f CBZ -b 2 "$directory"

#!/bin/bash

mkdir -p splits

find . -maxdepth 1 -size +100M -iname '*.cbz' | xargs -I{} bash -c 'split -a 6 -b 100M "{}" "./splits/$(basename "{}")_____"'
find . -maxdepth 1 -size -100M -iname '*.cbz' | xargs -I{} bash -c 'cp "{}" splits/'

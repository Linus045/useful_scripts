#!/bin/bash

mkdir -p splits
find . -size +100M | xargs -I{} bash -c 'split -a 6 -b 100M "{}" "./splits/$(basename "{}")_____"'

1. Move all files into a subdirectory e.g. all One Piece Manga files into a directory called 'One Piece'
2. Copy the split_large_files.sh script into that directory or call:

```
mkdir -p splits
find . -size +100M | xargs -I{} bash -c 'split -b 100M "{}" "./splits/$(basename "{}")_____"'
```

3. Copy the chunks to the webdav server
4. Connect via SSH and call the combine script `python3 combine_splits.py` in the same directory.
It will combine the parts and delete them afterwards leave the fully combined files


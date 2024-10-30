Download the Manga via HakuNeko into /home/linus/Mangas directory.
It will create a subdirectory for the specific manga.

Then call this line which converts each subdirectory into a volume.
Note that -b 2 creates an individual volume per subdirectory. to create one Volume 
which includes all files in the subdirectories see './kcc/kcc-c2e.py --help'
Hint: -b 0 or -b 1

./kcc/kcc-c2e.py -m -n -f CBZ -b 2 '/home/linus/Mangas/One Punch Man'


Next copy them to the Webdav server
If the files are larger than 100M it won't work (Cloudflare file upload limitation)
therefore use the split_large_files.sh script to split them apart, upload them and then recombine them
on the server. See README_splitting_combining.md


ALTERNATIVELY:
use use ./convert_to_cbz.sh script

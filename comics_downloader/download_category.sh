download_list="download_list.txt"

./generate_list.sh "$1" > "$download_list"


echo "Downloading comics..."
cat "$download_list"

echo "Start download? (y/N)"

if [ "$(read -r -n 1 -p "Press y to continue: " key; echo $key)" != "y" ]; then
	echo "Download cancelled."
	exit 0
fi

# cat "$download_list" | xargs -I{} -P $(nproc) bash -c './download.sh {}'  


echo
echo "Download in parallel? (Y/n)"


if [ "$(read -r -n 1 -p "Press Y to continue" key; echo $key)" != "n" ]; then
	echo "Downloading in parallel..."
	cat "$download_list" | xargs -I{} -P $(nproc) bash -c './download.sh {}'  
else
	echo "Downloading sequentially..."
	cat "$download_list" | xargs -I{} bash -c './download.sh {}'  
fi




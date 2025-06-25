
#NR="deadpool-001-2013" 
NR="$1"

mkdir -p htmls


# if html does not exist, download it
if [ ! -f ${NR}.html ]; then
	echo "Downloading HTML for ${NR}..."
	curl "https://readallcomics.com/${NR}/" -s > htmls/${NR}.html 
else
	echo "HTML for ${NR} already exists."
fi


if [ ! -d ${NR} ]; then
	echo "Creating directory for ${NR}..."
	mkdir ${NR}
else
	echo "Directory for ${NR} already exists."
fi

cd "${NR}" || exit 1
cat ../htmls/${NR}.html | grep -Eo 'src="https://.*blogspot\.com[^"]+' | sed 's/^src="//' | xargs -I{} bash -c "wget --quiet --continue --content-disposition '{}' || echo 'Failed to download {}. Check if the URL is valid.'"
cat ../htmls/${NR}.html | grep -Eo 'src="//.*blogspot\.com[^"]+' | sed 's/^src="/https:/' | xargs -I{} bash -c "wget --quiet --continue --content-disposition '{}' || echo 'Failed to download {}. Check if the URL is valid.'"
cat ../htmls/${NR}.html | grep -Eo 'src="https://.*blogger\.googleusercontent\.com[^"]+' | sed 's/^src="//' | xargs -I{} bash -c "wget --quiet --continue --content-disposition '{}' || echo 'Failed to download {}. Check if the URL is valid.'"

find . -maxdepth 1 -iname "*.jpg" -print | zip "../${NR}.zip" --quiet -@  || echo "Failed to create zip file for ${NR}. Check if there are any images downloaded."

if [ $? -ne 0 ]; then
	echo "Error creating zip file. Exiting."
	exit 1
fi
mv ../${NR}.zip ../${NR}.cbz


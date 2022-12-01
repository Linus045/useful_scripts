
filename_full=$1

echo "Filename full: $filename_full"

basename=$(basename $filename_full)
dirname=$(dirname $filename_full)
filename=$(echo "$basename" | cut -f 1 -d '.')
extension="${filename_full##*.}"

echo $filename
echo $extension

if echo $filename | grep -qE '[ "]'
then
   echo "Dateiname DARF KEINE LEERSCHRITTE ENTHALTEN!"
   return 1
fi


if [ -f "$dirname/$filename.$extension" ]; then
    echo "$dirname/$filename.$extension found. Starting conversion"
else 
    echo "$filename does not exist."
    return 2
fi

screen_name="compressing_$basename"
echo "Starting screen: $screen_name"



# ffmpeg -i "$dirname/$filename.$extension" -vcodec libx256 -crf 24 "$dirname/$filename_compressed.$extension"
echo "Inputting from: $dirname/$filename.$extension" 
echo "Outputting to: $dirname/$filename""_compressed.$extension"

screen -dmS $screen_name ffmpeg -i "$dirname/$filename.$extension" -vcodec libx265 -crf 24 "$dirname/$filename_compressed.$extension"


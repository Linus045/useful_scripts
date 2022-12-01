
screen -list

# request SCREEN_NAME here
read -p "Enter screen name where ffmpeg is currently convertig: " SCREEN_NAME


screen -XS $SCREEN_NAME hardcopy screenlog_delete_me 

MAX_FRAMES=$(grep -E -o "NUMBER_OF_FRAMES-?.*:\s*([0-9]+)" screenlog_delete_me | grep -E -o "([0-9]+)" | head -n 1)
CUR_FRAMES=$(grep -E -o "frame=\s*([0-9]+)" screenlog_delete_me | grep -E -o "([0-9]+)")
NAME=$(grep -E -o "title\s*:\s*(.+)$" screenlog_delete_me | grep -E -o "(.+)" | head -n 1)

# clear last 3 lines
# echo "\e[1A\e[K"
# echo "\e[2A\e[K"
# echo "\e[3A\e[K"
# echo "\e[4A\e[K"

# print output
echo "Konvertiere Datei: $NAME"


while [ true ]; do
    screen -XS $SCREEN_NAME hardcopy screenlog_delete_me 

    MAX_FRAMES=$(grep -E -o "NUMBER_OF_FRAMES-?.*:\s*([0-9]+)" screenlog_delete_me | grep -E -o "([0-9]+)" | head -n 1)
    CUR_FRAMES=$(grep -E -o "frame=\s*([0-9]+)" screenlog_delete_me | grep -E -o "([0-9]+)")
    NAME=$(grep -E -o "title\s*:\s*(.+)$" screenlog_delete_me | grep -E -o "(.+)" | head -n 1)

    # clear last line
    echo "\e[1A\e[K"
    echo "\e[2A\e[K"

    # print output
    python3 -c "print(str(round(100.0 / $MAX_FRAMES * $CUR_FRAMES, 2)) + '% [' + str($CUR_FRAMES) + '/' + str($MAX_FRAMES) + ']')"
    sleep 1
done
rm screenlog_delete_me

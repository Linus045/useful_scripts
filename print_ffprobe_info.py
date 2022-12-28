import os
import subprocess
import argparse
import re

# walk through every file in the directory and run ffprobe on ,mkv,mp4,avi files
# log output to a file called ffprobe_info.txt
# print output to screen

LANGUAGES_TO_INCLUDE = ["eng", "ger", "deu", "jpn"]


COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "orange": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}

def print_color(text, color):
    if color in COLORS:
        print(COLORS[color] + text + COLORS["reset"])
    else:
        print(text)

# parse file or directory name from arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Print ffprobe info for a file or directory")
    parser.add_argument("file", help="file or directory to print info for")
    args = parser.parse_args()
    return args

def ffprobe(file):
    output = subprocess.check_output(["ffprobe", file], stderr=subprocess.STDOUT)
    return output.decode("utf-8")


def print_ffprobe_info(file, info, stream_indexes_to_print=None):
    print_color(file, "blue")
    lines = info.split("\n")
    for line in lines:
        if re.search(r"^\s+Stream #\d+:", line):
            index, language, stream_type = get_stream_metadata(line)
            if stream_indexes_to_print is None:
                   print(f"{index}: {line}")
            else:
                if index in stream_indexes_to_print:
                   print(f"{index}: {line}")
    return info


def parse_ffprobe_info(info : str):
    lines = info.split("\n")
    audio_streams = []
    video_streams = []
    subtitle_streams = []
    unknown_streams = []
    for line in lines:
        if re.search(r"^\s+Stream #\d+:", line):
            if "Audio" in line:
                audio_streams.append(line)
            elif "Video" in line:
                video_streams.append(line)
            elif "Subtitle" in line:
                subtitle_streams.append(line)
            else:
                unknown_streams.append(line)
    return {
        "audio": audio_streams,
        "video": video_streams,
        "subtitle": subtitle_streams,
        "unknown": unknown_streams
    }

def parse_language(line):
    # Stream #0:0: Video: h264 (High), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 1k tbn (default)
    # Stream #0:1(eng): Audio: eac3, 48000 Hz, 5.1(side), fltp, 640 kb/s
    # Stream #0:2(eng): Subtitle: subrip:
    matches = re.search(r"^\s+Stream #\d+:\d+\(([a-zA-Z]{3})\):", line)
    if matches:
        return matches.group(1)
    else:
        return None


def has_valid_audio(streams):
    for stream in streams["audio"]:
        language = parse_language(stream)
        if language in LANGUAGES_TO_INCLUDE:
            return True
    return False

def has_valid_subtitle(streams):
    for stream in streams["subtitle"]:
        language = parse_language(stream)
        if language in LANGUAGES_TO_INCLUDE:
            return True
    return False

def has_valid_video(streams):
    # return true if there is only one video stream
    if len(streams["video"]) == 1:
        return True

    for stream in streams["video"]:
        language = parse_language(stream)
        if language in LANGUAGES_TO_INCLUDE:
            return True
    return False

def get_valid_indexes(info):
    # Stream #0:0: Video: h264 (High), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 1k tbn (default)
    # Index: 0
    # Stream #0:1(eng): Audio: eac3, 48000 Hz, 5.1(side), fltp, 640 kb/s
    # Index: 1
    # Stream #0:2(eng): Subtitle: subrip:
    # Index: 2

    # get all stream indexes
    stream_indexes = []
    for line in info.split("\n"):
        if re.search(r"^\s+Stream #\d+:", line):
            # get stream index with regex
            matches = re.search(r"^\s+Stream #\d+:(\d+)", line)
            if matches:
                parsed_index = int(matches.group(1))
                stream_indexes.append(parsed_index)
            else:
                raise Exception("Could not parse stream index from line:\n" + line)
    return stream_indexes

# returns index and language of the stream line
def get_stream_metadata(stream_line):
    # Stream #0:0: Video: h264 (High), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 1k tbn (default)
    # Index: 0 Language: None
    # Stream #0:1(eng): Audio: eac3, 48000 Hz, 5.1(side), fltp, 640 kb/s
    # Index: 1 Language: eng
    # Stream #0:2(eng): Subtitle: subrip:
    # Index: 2 Language: eng

    matches = re.search(r"^\s+Stream #\d+:(\d+)\(([a-zA-Z]{3})\): (Video|Audio|Subtitle)", stream_line)
    if matches:
        index = int(matches.group(1))
        language = matches.group(2)
        stream_type = matches.group(3)
        return index, language, stream_type
    matches = re.search(r"^\s+Stream #\d+:(\d+): (Video|Audio|Subtitle)", stream_line)
    if matches:
        index = int(matches.group(1))
        language = None
        stream_type = matches.group(2)
        return index, language, stream_type
    raise Exception("Could not parse stream index from line:\n" + stream_line)



def get_included_stream_indexes(info):
    # get all stream indexes which are english
    stream_indexes = []
    for line in info.split("\n"):
        if re.search(r"^\s+Stream #\d+:", line):
            index, language, stream_type = get_stream_metadata(line)
            if language is None:
                print_color("WARNING: No language found for stream:", "orange")
                print_color(line, "orange")
            elif language in LANGUAGES_TO_INCLUDE:
                stream_indexes.append(index)
    
    video_streams = parse_ffprobe_info(info)["video"]
    video_stream_count = len(video_streams)
    if video_stream_count == 1:
        index, language, stream_type = get_stream_metadata(video_streams[0])
        if index not in stream_indexes:
            print_color("Note: Added only available video stream:", "orange")
            print_color(video_streams[0], "orange")
            stream_indexes.append(index)
        
    return stream_indexes

def open_file_in_vlc(file_path):
    # make sure vlc is available
    try:
        subprocess.check_output(["vlc", "--version"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("VLC is not available. Please install VLC.")
        return
    subprocess.call(["vlc", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# check if file contains english audio, subtitle, and video
# if not, request user to give a list of stream indexes to include in the output
def request_streams(file):
    info = ffprobe(file)

    valid_indexes = get_valid_indexes(info)

    streams = parse_ffprobe_info(info)
    audio_missing = not has_valid_audio(streams)
    subtitle_missing = not has_valid_subtitle(streams)
    video_missing = not has_valid_video(streams)
    print("Audio Missing:", audio_missing)
    print("Subtitles Missing:", subtitle_missing)
    print("Video Missing:", video_missing)
    if audio_missing or subtitle_missing or video_missing:
        print(file)
        print("Missing audio, subtitle, or video in included format")
        print("Please enter the stream indexes to include in the output")

        print_ffprobe_info(file, info)

        print("Enter stream indexes separated by commas")
        print("Valid indexes: {}".format(valid_indexes))
        print("Enter 'open' to open the file in VLC")
        print("Add '!' as the first character to blacklist streams instead. E.g. !1,2,3,4")
        while True:
            stream_indexes = input("Stream indexes: ")
            if stream_indexes == "open":
                print("Opening file in vlc player")
                open_file_in_vlc(file)
                continue
            # check if stream indexes are valid
            is_blacklist = stream_indexes[0] == '!'
            if is_blacklist:
                print("[BLACKLIST MODE]")
                stream_indexes = stream_indexes[1:]
            stream_indexes = [s for s in stream_indexes.split(",") if s.strip() != '']

            input_valid = True
            for stream_index in stream_indexes:
                try:
                    parsed_index = int(stream_index)
                    if int(stream_index) not in valid_indexes:
                        input_valid = False
                        break
                except ValueError:
                    input_valid = False
                    break


            if not input_valid:
                print("\nInvalid stream indexes.")
                print("Valid indexes: {}".format(valid_indexes))
                print("e.g. 0,1,2")
                continue

            # convert strings to ints
            stream_indexes = [int(index) for index in stream_indexes]

            # if blacklist, invert filter
            if is_blacklist:
                removed_indexes = stream_indexes
                stream_indexes = []
                
                for index in valid_indexes:
                    if index not in removed_indexes:
                        stream_indexes.append(index)
            else:
                removed_indexes = []
                for index in valid_indexes:
                    if index not in stream_indexes:
                        removed_indexes.append(index)

            # confirm choice
            print("-" * 80)
            print("Are you sure you want to include these streams?")
            print("Selected stream indexes: {}".format(stream_indexes))
            print_ffprobe_info(file, info, stream_indexes)
            print("-" * 80)
            print("Removed streams:")
            print_ffprobe_info(file, info, removed_indexes)
            print("-" * 80)
            choice = input("(y/N): ")
            if choice == "y":
                return stream_indexes
    else:
        print_ffprobe_info(file, info)
        indexes = get_included_stream_indexes(info)
        video_added = False
        video_indexes = [ get_stream_metadata(metadata)[0] for metadata in streams["video"]]
        for index in indexes:
            if index in video_indexes:
                if not video_added:
                    video_added = True
                else:
                    choice = input(f"Video added twice. Remove duplicate? [Stream {index}] (Y/n): ")
                    if choice == "n":
                        continue
                    indexes.remove(index)

        print("Including all valid streams")
        print(indexes)
        return indexes

if __name__ == "__main__":
    args = parse_args()
    file = args.file

    # throw error if file or directory does not exist
    if not os.path.exists(file):
        raise Exception("File or directory does not exist")

    # output stream selection to file
    output_filename = "stream_selections.txt"
    output_file = open(output_filename, "w")

    paths = []

    if os.path.isdir(file):
        for root, dirs, files in os.walk(file):
            for file in files:
                if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".avi"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    paths.append(full_path)

    else:
        full_path = os.path.abspath(file)
        paths.append(full_path)

    file_count = 0
    for file in paths:
        file_count += 1
        print("#" * 80)
        print("[{}/{}] {}".format(file_count, len(paths), file))
        selected_streams = request_streams(file)
        print("Selected streams: {}".format(selected_streams))
        # output format:
        # file_path:stream_indexes
        output_file.write(file + ":" + ",".join(map(str, selected_streams)) + "\n")

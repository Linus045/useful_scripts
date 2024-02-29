import os
import subprocess
import datetime
import threading
import io
import shutil


# use print_ffprobe_info.py first
# see beginning of that file for instructions

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Extract streams from videos. Use "print_ffprobe_info.py" beforehand to create the stream_selection.txt file.')
    parser.add_argument('-d', '--delete', help='delete after conversion', action='store_true', default=False)
    parser.add_argument('-f', '--file', help='file to convert (stream_selection.txt file generated by "print_ffprobe_info.py")', required=True)
    return parser.parse_args()


def parse_stream_info_file(stream_info_file):
    # File Format:
    # <path>:<stream indexes>
    # /mnt/HDD/Silicon_Valley/Silicon_Valley_S02/Silicon.Valley.S02E02.mkv:0#video,5#audio,7#subtitle,9#attachment
    # /mnt/HDD/Silicon_Valley/Silicon_Valley_S02/Silicon.Valley.S02E07.mkv:0#video,5#audio,7#subtitle,9#attachment
    # /mnt/HDD/Silicon_Valley/Silicon_Valley_S02/Silicon.Valley.S02E05.mkv:0#video,5#audio,7#subtitle,9#attachment
    # /mnt/HDD/Silicon_Valley/Silicon_Valley_S02/Silicon.Valley.S02E03.mkv:0#video,5#audio,7#subtitle,9#attachment

    with open(stream_info_file, 'r') as f:
        lines = f.readlines()
    streams = []
    for line in lines:
        line = line.strip()
        if line:
            path, stream_indexes = line.split(':')
            stream_indexes = stream_indexes.split(',')
            stream_indexes = [(int(line.split("#")[0]), line.split("#")[1]) for line in stream_indexes]
            streams.append((path, stream_indexes))

    return streams


# starts ffmpeg in a new process and returns the process object
def run_ffmpeg(file, stream_indexes) -> subprocess.Popen:
    # append speed to output filename
    # created 'converted' directory if it doesn't exist in the file's directory
    if not os.path.exists(os.path.join(os.path.dirname(file), "converted")):
        os.makedirs(os.path.join(os.path.dirname(file), "converted"))

    output_filepath = os.path.join(os.path.dirname(file), "converted", os.path.basename(file) + "_converted.mkv")

    log_filepath = os.path.join(os.path.dirname(file), "converted", os.path.basename(file) + "_converted.log")
    log_file = open(log_filepath, 'w')


    # for each index generate a string of the form "-map 0:<index>"
    stream_indexes_params = []
    for (index,stream_type) in stream_indexes:
        stream_indexes_params.append("-map")
        if stream_type == "attachment":
            stream_indexes_params.append(f"0:{index}")
        else:
            stream_indexes_params.append(f"0:{index}")



    # stream_indexes_params.append("-map")
    # stream_indexes_params.append(f"0")
    
    # copy all attachments
    stream_indexes_params.append("-map")
    stream_indexes_params.append(f"0:t?")

    # ffmpeg -i <input file> -map 0:<stream index> -c:v copy -c:a copy -c:s copy <output file>
    parameter = [
        "ffmpeg",
        "-y",
        "-i", file
    ] + stream_indexes_params + [
        "-c", "copy",
        output_filepath
    ]

    # print(parameter)
    log_file.write(" ".join(parameter) + "\n\n")
    log_file.flush()

    # append "_converted.mkv" to the output filename
    print("Copying: " + file + " to " + output_filepath)
    exit_code = subprocess.call(parameter, stdout=log_file, stderr=log_file)
    return exit_code


if __name__ == "__main__":
    args = parse_args()

    DELETE_AFTER_CONVERSION = args.delete
    print("DELETE_AFTER_CONVERSION: " + str(DELETE_AFTER_CONVERSION))
    if DELETE_AFTER_CONVERSION:
        choice = input(f"Deleting files after conversion, are you sure? (y/N): ")
        if choice != "y":
            exit(1)

    stream_info_file = args.file
    if not os.path.exists(stream_info_file):
        print("File not found: {}".format(stream_info_file))
        exit(1)

    streams = parse_stream_info_file(stream_info_file)
    print("Found {} streams".format(len(streams)))

    count = 0
    errored = []
    total_start_time = datetime.datetime.now()
    for path, stream_indexes in streams:
        count += 1

        print("##############################")
        print("Nr. " + str(count) + "/" + str(len(streams)))
        print("Processing: " + path)

        if not os.path.exists(path):
            print("File not found: " + path)
            errored.append(path)
            continue

        start_time = datetime.datetime.now()

        error_code = run_ffmpeg(path, stream_indexes)
        if error_code != 0:
            print("Error converting: " + path)
            errored.append(path)

        end_time = datetime.datetime.now()
        print("Finished: " + path + " in " + str(end_time - start_time))
        try:
            if DELETE_AFTER_CONVERSION:
                os.remove(path)
        except OSError:
            print("ERROR DELETING FILE AFTER CONVERTING")
            errored.append(path)
        # print duration formatted as h:mm:ss (e.g. 1:23:45)
        print("##############################")

    total_end_time = datetime.datetime.now()
    print("Duration: " + str(total_end_time - total_start_time))
    print("Done!")
    print("Errored: " + str(errored))



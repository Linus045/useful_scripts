import os
import subprocess
import datetime
import threading
import io
import shutil

COPYMODE=True

# grabs all .mkv files from this directory
# and adds their full path to the list
files = []
for file in os.listdir(os.getcwd()):
    if file.endswith(".mkv"):
        files.append(os.path.join(os.getcwd(), file))
        print("Added: " + file)
    else:
        print("Ignoring: " + file)


if not os.path.exists("converted"):
    os.makedirs("converted")
    print("converted directory created")

# run ffmpeg for every file in the list
# and save the output to a new file in an output directory 'converted'
# command to run:
# ffmpeg -i <FILENAME>.mkv -map "0:m:language:eng?" -map "0:m:language:ger?" -c:v copy -c:a copy -c:s copy converted/<FILENAME>.mkv
# speeds = ["ultrafast", "superfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
selected_speed = "slower"
errored = []


# starts ffmpeg in a new process and returns the process object
def run_ffmpeg(file, logfile, speed) -> subprocess.Popen:
    # append speed to output filename
    if COPYMODE:
        output_filepath = os.path.join("converted", os.path.basename(file) + "_converted.mkv")
        print("Copying: " + file + " to " + output_filepath)
        process = subprocess.call([
            "ffmpeg",
            "-i", file,
            "-map", "0:m:language:eng?",
            "-map", "0:m:language:deu?",
            "-map", "0:m:language:ger?",
            "-c:v", "copy",
            "-c:a", "copy",
            "-c:s", "copy",
            output_filepath
        ], stdout=logfile, stderr=logfile)
    else:
        output_filepath = os.path.join("converted", os.path.basename(file) + "-" + speed + ".mkv")
        print("Converting: " + file + " to " + output_filepath)
        process = subprocess.call([
            'ffmpeg',
            '-y',
            '-i', file,
            '-map', '0:m:language:eng?',
            '-map', '0:m:language:deu?',
            '-map', '0:m:language:ger?',
            '-c:v', 'libx265',
            '-crf', '22',
            '-tag:v', 'hvc1',
            '-preset', speed,
            '-c:a', 'copy',
            '-c:s', 'copy',
            output_filepath
        ], stdout=logfile, stderr=logfile)
    return process


def ffprobe_max_duration(file) -> float:
    # get total frames of the video stream
    try:
        duration = subprocess.check_output([
            'ffprobe', '-i',
            file,
            '-show_entries', 'format=duration', '-v', 'quiet',
            '-of', 'csv=%s' % ("p=0")])
        return float(duration)
    except ChildProcessError as e:
        print("Error getting duration of: " + file)
        print(e)
        return 0

for file in files:
    log_filename = "converted/" + os.path.basename(file) + ".log"
    log_file = open(log_filename, "w")
    print("##############################")
    print("Processing: " + file)
    print("Logfile: " + log_filename)

    # start ffmpeg and periodically check if it is still running
    # grab output from process and filter it to get the current speed
    # if the process is still running, write the output to the log file
    # if the process is not running, write the output to the log file and close the log file
    start_time = datetime.datetime.now()

    error_code = run_ffmpeg(file, log_file, selected_speed)
    if error_code != 0:
        print("Error converting: " + file)
        errored.append(file)

    end_time = datetime.datetime.now()
    print("Finished: " + file)
    # print duration formatted as h:mm:ss (e.g. 1:23:45)
    print("Duration: " + str(end_time - start_time))
    print("##############################")


print("Done!")
print("Errored: " + str(errored))

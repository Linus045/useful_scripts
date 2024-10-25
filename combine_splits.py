import glob
import subprocess
import os


parts = glob.glob("splits/*_____*")


filenames = dict()

for partname in parts:
    seperatorIdx = partname.find("_____")
    filename = partname[0:seperatorIdx]
    if filename in filenames:
        filenames[filename].append(partname)
    else:
        filenames[filename] = [partname]

print(filenames)


def last_6chars(x):
    return (x[-6:])


for filename, parts in filenames.items():
    command = ["cat"]
    parts = sorted(parts, key=last_6chars)
    for part in parts:
        command.append(part)

    print(command)
    with open(filename, "w") as outputFile:
        subprocess.run(command, stdout=outputFile)

    print(f"Combined parts into {filename}")

    for part in parts:
        if os.path.exists(part):
            os.remove(part)
        else:
            print(f"Failed to delete. The file {part} does not exist.")

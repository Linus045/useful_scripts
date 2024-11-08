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


parts_to_delete = []
for filename, parts in filenames.items():
    command = ["cat"]
    parts = sorted(parts, key=last_6chars)
    for part in parts:
        command.append(part)
        parts_to_delete.append(part)

    print(command)
    with open(filename, "w") as outputFile:
        subprocess.run(command, stdout=outputFile)

    print(f"Combined parts into {filename}")

print("Please validate that everything works as expected")
input = input("Remove part files? [y/N]: ")
if input == 'y' or input == "Y":
    for part in parts_to_delete:
        if os.path.exists(part):
            os.remove(part)
        else:
            print(f"Failed to delete. The file {part} does not exist.")

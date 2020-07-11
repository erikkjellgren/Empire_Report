import glob
import os
import sys
import time
import zipfile


def unpack_gamestate(save_name):
    """Docstring
    """
    archive = zipfile.ZipFile(f"{save_name}", "r")
    lines = archive.read("gamestate").decode("utf-8").replace("\t", "").splitlines()
    cleaned = open(f'{save_name.split(".")[0]}.data', "w")
    found_country = False
    num_brackets = 0
    openbracket_counter = 0
    keys = []
    keys1 = ["country"]
    keys2 = ["0"]
    keys3 = ["budget", "expenses"]
    keys4 = ["current_month"]
    keys5 = ["income", "expenses"]
    for line in lines:
        if "={" in line:
            keys.append(line.split("={")[0])
        elif "{" in line:
            openbracket_counter += 1

        saveline = True
        if len(keys) > 0:
            if keys[0] not in keys1:
                saveline = False
            elif len(keys) > 1:
                if keys[1] not in keys2:
                    saveline = False
                # Stop when all economics data for the player have been collected
                elif keys[0] == "country" and keys[1] != "0":
                    break
                elif len(keys) > 2:
                    if keys[2] not in keys3:
                        saveline = False
                    elif len(keys) > 3:
                        if keys[3] not in keys4:
                            saveline = False
                        elif len(keys) > 4:
                            if keys[4] not in keys5:
                                saveline = False
        if saveline:
            cleaned.write(f"{line}\n")
        if "{" in line:
            num_brackets += 1
        if "}" in line:
            num_brackets -= 1
            if openbracket_counter != 0:
                openbracket_counter -= 1
            else:
                keys.pop(-1)
        if num_brackets == 0 and found_country:
            break


def save_unpacked_files(save_name):
    """Docstring
    """
    saves = glob.glob(f"savefiles/{save_name}/*.sav")

    start_time = time.time()
    off_set = 0
    for j, save in enumerate(saves):
        if os.path.isfile(f'{save.split(".")[0]}.data'):
            continue
        unpack_gamestate(save)
        current_time = time.time()
        if current_time - start_time < 1:
            off_set = j
        progress = f"Percentage complete: {(j+1-off_set)/(len(saves)-off_set)*100:5.2f}%"
        progress += f"  --- Estimated time left: "
        progress += f"{(current_time - start_time)/(j+1-off_set)*(len(saves)-off_set) - (current_time - start_time):5.2f} sec"
        progress += f" --- Time used: {current_time - start_time:5.2f}\r"
        sys.stdout.write(progress)
        sys.stdout.flush()


save_unpacked_files("thrashiantechnocrat7_-1184343043")

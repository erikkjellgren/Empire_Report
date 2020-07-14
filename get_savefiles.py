import glob
import json
import os
import shutil
import time


def get_savefiles(save_games_location):
    """Docstring
    """
    if not os.path.exists("savefiles"):
        os.makedirs("savefiles")
    last_modified = {}
    runs = glob.glob(f"{save_games_location}/save games/*")
    for run in runs:
        if not os.path.exists(f"savefiles/{run.split('/')[-1]}"):
            os.makedirs(f"savefiles/{run.split('/')[-1]}")
        last_modified[run] = 0.0
    while True:
        for folder in last_modified:
            modified = os.path.getmtime(f"{folder}")
            if modified != last_modified:
                last_modified[folder] = modified
                save_file = glob.glob(f"{folder}/*.sav")
                shutil.copy2(save_file[0], f"savefiles/{folder.split('/')[-1]}/{modified}.sav")
        time.sleep(5)


with open("settings.json") as handle:
    SETTINGS = json.loads(handle.read())
get_savefiles(SETTINGS["save_games_location"])

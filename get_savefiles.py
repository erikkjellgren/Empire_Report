import glob
import json
import os
import shutil
import time

from unpack_files import unpack_gamestate


def get_savefiles(save_games_location: str, unpack_on_the_fly: bool) -> None:
    """Docstring
    """
    if not os.path.exists("savefiles"):
        os.makedirs("savefiles")
    last_modified = {}
    runs = glob.glob(f"{save_games_location}/save games/*")
    number_saves = len(runs)
    for run in runs:
        if not os.path.exists(f"savefiles/{run.split('/')[-1]}"):
            os.makedirs(f"savefiles/{run.split('/')[-1]}")
        last_modified[run] = 0.0
    try:
        with open("savefiles_tracker.json", "r") as jsonhandle:
            tracker = json.loads(jsonhandle.read())
        for folder in tracker:
            last_modified[folder] = tracker[folder]
    except FileNotFoundError:
        print("Creating savefiles_tracker.json")
    while True:
        runs = glob.glob(f"{save_games_location}/save games/*")
        if number_saves != len(runs):
            for run in runs:
                if run not in last_modified:
                    if not os.path.exists(f"savefiles/{run.split('/')[-1]}"):
                        os.makedirs(f"savefiles/{run.split('/')[-1]}")
                    last_modified[run] = 0.0
            number_saves = len(runs)
        for folder in last_modified:
            save_file = glob.glob(f"{folder}/*.sav")
            modified = round(os.path.getmtime(f"{save_file[0]}"), 0)
            if modified != last_modified[folder]:
                last_modified[folder] = modified
                shutil.copy2(save_file[0], f"savefiles/{folder.split('/')[-1]}/{modified}.sav")
                with open("savefiles_tracker.json", "w") as outfile:
                    json.dump(last_modified, outfile, indent=2)
                outfile.close()
                if unpack_on_the_fly:
                    unpack_gamestate(
                        folder.split("/")[-1], f"savefiles/{folder.split('/')[-1]}/{modified}.sav"
                    )
        time.sleep(5)


with open("settings.json") as handle:
    SETTINGS = json.loads(handle.read())
get_savefiles(SETTINGS["save_games_location"], SETTINGS["unpack_on_the_fly"])

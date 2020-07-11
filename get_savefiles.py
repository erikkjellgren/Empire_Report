import os
import shutil
import time


def get_savefiles(save_name):
    """Docstring
    """
    if not os.path.exists("savefiles"):
        os.makedirs("savefiles")
    last_modified = 0.0

    while True:
        modified = os.path.getmtime(
            f"/mnt/c/Users/kjellgren/Documents/Paradox Interactive/Stellaris/save games/{save_name}/ironman.sav"
        )
        if modified != last_modified:
            shutil.copy2(
                f"/mnt/c/Users/kjellgren/Documents/Paradox Interactive/Stellaris/save games/{save_name}/ironman.sav",
                f"/mnt/c/Users/kjellgren/Documents/gitreps/Stellaris_Stats/savefiles/{save_name}/{modified}.sav",
            )
            last_modified = modified
        time.sleep(10)


get_savefiles("thrashiantechnocrat7_-1184343043")

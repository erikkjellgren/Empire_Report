import copy
import glob
import json
import sys
import time
import zipfile
from collections import defaultdict

from mpi4py import MPI


def input_tree():
    """Docstring
    """
    return defaultdict(input_tree)


def gamestate_to_dict(lines):
    """Docstring
    """
    keys = []
    gamestate = input_tree()
    openbracket_counter = 0
    for i, line in enumerate(lines):
        if i < 4:
            gamestate[line.split("=")[0]] = line.split("=")[1].strip('"')
        if "={" in line:
            keys.append(line.split("={")[0])
        elif "{" in line:
            openbracket_counter += 1

        saveline = True
        if "{" in line and "}" not in line:
            saveline = False
        elif "}" in line and "{" not in line:
            saveline = False
        elif line.strip() == "}":
            saveline = False
        if saveline:
            if "=" in line:
                if len(keys) == 1:
                    gamestate[keys[0]][line.split("=")[0]] = line.split("=")[1]
                elif len(keys) == 2:
                    gamestate[keys[0]][keys[1]][line.split("=")[0]] = line.split("=")[1]
                elif len(keys) == 3:
                    gamestate[keys[0]][keys[1]][keys[2]][line.split("=")[0]] = line.split("=")[1]
                elif len(keys) == 4:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][line.split("=")[0]] = line.split("=")[1]
                elif len(keys) == 5:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][line.split("=")[0]] = line.split(
                        "="
                    )[1]
                elif len(keys) == 6:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][
                        line.split("=")[0]
                    ] = line.split("=")[1]
                elif len(keys) == 7:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]][
                        line.split("=")[0]
                    ] = line.split("=")[1]
                elif len(keys) == 8:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]][keys[7]][
                        line.split("=")[0]
                    ] = line.split("=")[1]
            else:
                if len(keys) == 1:
                    gamestate[keys[0]][line.split("=")[0]] = True
                elif len(keys) == 2:
                    gamestate[keys[0]][keys[1]][line.split("=")[0]] = True
                elif len(keys) == 3:
                    gamestate[keys[0]][keys[1]][keys[2]][line.split("=")[0]] = True
                elif len(keys) == 4:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][line.split("=")[0]] = True
                elif len(keys) == 5:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][line.split("=")[0]] = True
                elif len(keys) == 6:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][line.split("=")[0]] = True
                elif len(keys) == 7:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]][
                        line.split("=")[0]
                    ] = True
                elif len(keys) == 8:
                    gamestate[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]][keys[7]][
                        line.split("=")[0]
                    ] = True

        if "}" in line:
            if openbracket_counter != 0:
                openbracket_counter -= 1
            else:
                keys.pop(-1)
    return dict(gamestate)


def unpack_gamestate(save_name, save_file):
    """Docstring
    """
    archive = zipfile.ZipFile(f"{save_file}", "r")
    lines = archive.read("gamestate").decode("utf-8").replace("\t", "").replace('"', "").splitlines()
    gamestate = gamestate_to_dict(lines)
    country_dict = {"country": copy.deepcopy(gamestate["country"])}
    country_dict["date"] = gamestate["date"]
    for key in gamestate["country"]:
        if key != "0":
            del country_dict["country"][key]
    for key in gamestate["country"]["0"]:
        if key not in ["budget", "employable_pops"]:
            del country_dict["country"]["0"][key]
    for key in gamestate["country"]["0"]["current_month"]:
        if key not in ["income", "expenses"]:
            del country_dict["country"]["0"]["current_month"][key]
    with open(f"savefiles/{save_name}/{gamestate['date'].replace('.','')}.country.json", "w") as outfile:
        json.dump(country_dict, outfile, indent=2)
    del country_dict

    planets_dict = {"planets": copy.deepcopy(gamestate["planets"])}
    planets_dict["date"] = gamestate["date"]
    controlled_planets = list(gamestate["country"]["0"]["controlled_planets"].keys())[0].split(" ")[:-1]
    for key in gamestate["planets"]["planet"]:
        if key not in controlled_planets:
            del planets_dict["planets"]["planet"][key]
        elif gamestate["planets"]["planet"][key]["total_housing"] == "0":
            del planets_dict["planets"]["planet"][key]
    with open(f"savefiles/{save_name}/{gamestate['date'].replace('.','')}.planets.json", "w") as outfile:
        json.dump(planets_dict, outfile, indent=2)

    pops_dict = {"pop": copy.deepcopy(gamestate["pop"])}
    pops_dict["date"] = gamestate["date"]
    controlled_pops = []
    for key in planets_dict["planets"]["planet"]:
        # When colonizing the number of pops is zero.
        if len(list(planets_dict["planets"]["planet"][key]["pop"].keys())) == 0:
            continue
        controlled_pops = (
            controlled_pops + list(planets_dict["planets"]["planet"][key]["pop"].keys())[0].split(" ")[:-1]
        )
    for key in gamestate["pop"]:
        if key not in controlled_pops:
            del pops_dict["pop"][key]
    with open(f"savefiles/{save_name}/{gamestate['date'].replace('.','')}.pop.json", "w") as outfile:
        json.dump(pops_dict, outfile, indent=2)
    del planets_dict
    del pops_dict


def save_unpacked_files(save_name):
    """Docstring
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocess = comm.Get_size()

    saves = sorted(glob.glob(f"savefiles/{save_name}/*.sav"))

    if rank == 0:
        start_time = time.time()
    for j, save in enumerate(saves):
        if j % nprocess != rank:
            continue
        unpack_gamestate(save_name, save)

        if rank != 0:
            continue
        current_time = time.time()
        progress = f"Percentage complete: {(j+1)/(len(saves))*100:5.2f}%"
        progress += f"  --- Estimated time left: "
        progress += f"{(current_time - start_time)/(j+1)*(len(saves)) - (current_time - start_time):5.2f} sec"
        progress += f" --- Time used: {current_time - start_time:5.2f}\r"
        sys.stdout.write(progress)
        sys.stdout.flush()


if __name__ == "__main__":
    with open("settings.json") as handle:
        SETTINGS = json.loads(handle.read())
    save_unpacked_files(SETTINGS["save_folder_name"])

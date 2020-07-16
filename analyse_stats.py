import glob
import json
import time
from typing import Tuple

import numpy as np


def get_happiness(stratum: str, save_name: str) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.pop.json"))

    happiness = np.zeros((3, len(saves)))
    happiness[1, :] = 100
    counter = np.zeros(len(saves))
    time_array = np.zeros((3, len(saves)))

    start_time = time.time()
    print(f"Starting happiness {stratum}".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        for pop in gamestate["pop"].keys():
            if gamestate["pop"][pop]["category"] == stratum:
                # Sometimes pops do not have a happiness state.
                if "happiness" not in gamestate["pop"][pop]:
                    continue
                happiness[0, i] += float(gamestate["pop"][pop]["happiness"])
                happiness[1, i] = min(happiness[1, i], float(gamestate["pop"][pop]["happiness"]))
                happiness[2, i] = max(happiness[2, i], float(gamestate["pop"][pop]["happiness"]))
                counter[i] += 1
    happiness[0, :] = happiness[0, :] / counter

    current_time = time.time()
    print(f" --- Finished happiness {stratum} in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, happiness


def get_political_power(stratum: str, save_name: str) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.pop.json"))

    political_power = np.zeros(len(saves))
    time_array = np.zeros((3, len(saves)))

    start_time = time.time()
    print(f"Starting political power {stratum}".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        for pop in gamestate["pop"].keys():
            if gamestate["pop"][pop]["category"] == stratum:
                if "power" not in gamestate["pop"][pop]:
                    continue
                political_power[i] += float(gamestate["pop"][pop]["power"])
    current_time = time.time()
    print(f" --- Finished political power {stratum} in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, political_power


def get_unemployment(save_name: str) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.pop.json"))

    unemployment = np.zeros(len(saves))
    time_array = np.zeros((3, len(saves)))

    start_time = time.time()
    print(f"Starting unemployment".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        if i == 0:
            continue
        for pop in gamestate["pop"].keys():
            if "job" not in gamestate["pop"][pop].keys():
                unemployment[i] += 1
        if i == 2:
            unemployment[0] = unemployment[1]
    current_time = time.time()
    print(f" --- Finished unemployment in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, unemployment


def get_homeless(save_name: str) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.planets.json"))

    homeless = np.zeros(len(saves))
    time_array = np.zeros((3, len(saves)))

    start_time = time.time()
    print(f"Starting homeless".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        if i == 0:
            continue
        for planet in gamestate["planets"]["planet"].keys():
            homeless[i] -= min(0, float(gamestate["planets"]["planet"][planet]["free_housing"]))
        if i == 2:
            homeless[0] = homeless[1]
    current_time = time.time()
    print(f" --- Finished homeless in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, homeless


def get_pops(save_name: str, print_timing: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.country.json"))

    pops = np.zeros(len(saves))
    time_array = np.zeros((3, len(saves)))
    if print_timing:
        start_time = time.time()
        print(f"Starting pops".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        if i == 0:
            continue
        pops[i] += float(gamestate["country"]["0"]["employable_pops"])
        if i == 2:
            pops[0] = pops[1]

    if print_timing:
        current_time = time.time()
        print(f" --- Finished pops in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, pops


def get_gdp(save_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.country.json"))

    gdp = np.zeros(len(saves))
    start_time = time.time()
    print(f"Starting GDP".ljust(39), end=" ", flush=True)
    resources = [
        "energy",
        "minerals",
        "food",
        "alloys",
        "consumer_goods",
        "volatile_motes",
        "rare_crystals",
        "exotic_gases",
        "sr_dark_matter",
        "sr_living_metal",
        "sr_zro",
    ]

    for resource in resources:
        time_array, stats = get_resource_stats(resource, save_name, print_timing=False)
        if resource in ["energy", "minerals", "food"]:
            gdp += stats[0, :]
        elif resource in ["volatile_motes", "rare_crystals", "exotic_gases"]:
            gdp += 10 * stats[0, :]
        elif resource in ["sr_dark_matter", "sr_living_metal", "sr_zro"]:
            gdp += 20 * stats[0, :]
        elif resource == "consumer_goods":
            gdp += 2 * stats[0, :]
        elif resource == "alloys":
            gdp += 4 * stats[0, :]
    time_array, pops = get_pops(save_name, print_timing=False)
    current_time = time.time()
    print(f" --- Finished GDP in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, gdp, gdp / pops


def get_resource_stats(
    resource: str, save_name: str, print_timing: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.country.json"))

    stats = np.zeros((2, len(saves)))
    time_array = np.zeros((3, len(saves)))
    if print_timing:
        start_time = time.time()
        print(f"Starting {resource}".ljust(39), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        for key in gamestate["country"]["0"]["budget"]["current_month"]["income"].keys():
            if resource in gamestate["country"]["0"]["budget"]["current_month"]["income"][key].keys():
                stats[0, i] += float(
                    gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                )
        for key in gamestate["country"]["0"]["budget"]["current_month"]["expenses"].keys():
            if resource in gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key].keys():
                stats[1, i] += float(
                    gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                )

    if print_timing:
        current_time = time.time()
        print(f" --- Finished {resource} in ".ljust(47) + f"{current_time - start_time:5.2f} sec")
    return time_array, stats


def get_resource_stats_detailed(
    resource: str, save_name: str
) -> Tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Docstring
    """
    saves = sorted(glob.glob(f"savefiles/{save_name}/*.country.json"))

    time_array = np.zeros((3, len(saves)))
    megastructures = np.zeros((2, len(saves)))
    buildings = np.zeros((2, len(saves)))
    jobs = np.zeros((2, len(saves)))
    pops = np.zeros((2, len(saves)))
    leaders = np.zeros((2, len(saves)))
    ships = np.zeros((2, len(saves)))
    starbases = np.zeros((2, len(saves)))
    stations = np.zeros((2, len(saves)))
    armies = np.zeros((2, len(saves)))
    trade = np.zeros((2, len(saves)))

    start_time = time.time()
    print(f"Starting detailed {resource}".ljust(40), end=" ", flush=True)
    for i, save in enumerate(saves):

        with open(f"{save}") as handle:
            gamestate = json.loads(handle.read())

        year = float(gamestate["date"].split(".")[0])
        month = float(gamestate["date"].split(".")[1])
        day = float(gamestate["date"].split(".")[2])
        time_array[0, i] = day + month * 30 + year * 12 * 30
        time_array[1, i] = time_array[0, i] / 30
        time_array[2, i] = time_array[1, i] / 12

        for key in gamestate["country"]["0"]["budget"]["current_month"]["income"].keys():
            if resource in gamestate["country"]["0"]["budget"]["current_month"]["income"][key].keys():
                if "megastructure" in key:
                    megastructures[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "building" in key or "district" in key:
                    buildings[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "planet" in key:
                    jobs[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "pop" in key:
                    pops[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "leader" in key:
                    leaders[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "ship" in key:
                    ships[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "orbital" in key:
                    starbases[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "stations" in key:
                    stations[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "armies" in key:
                    armies[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
                elif "trade" in key:
                    trade[0, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["income"][key][resource]
                    )
        for key in gamestate["country"]["0"]["budget"]["current_month"]["expenses"].keys():
            if resource in gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key].keys():
                if "megastructure" in key:
                    megastructures[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "building" in key or "district" in key:
                    buildings[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "planet" in key:
                    jobs[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "pop" in key:
                    pops[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "leader" in key:
                    leaders[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "ship" in key:
                    ships[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "starbase" in key:
                    starbases[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "station" in key:
                    stations[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "armies" in key:
                    armies[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )
                elif "trade" in key:
                    trade[1, i] += float(
                        gamestate["country"]["0"]["budget"]["current_month"]["expenses"][key][resource]
                    )

    current_time = time.time()
    print(f"--- Finished detailed {resource} in ".ljust(46) + f"{current_time - start_time:5.2f} sec")
    return (
        time_array,
        megastructures,
        buildings,
        jobs,
        pops,
        leaders,
        ships,
        starbases,
        stations,
        armies,
        trade,
    )

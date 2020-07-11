from collections import defaultdict


def input_tree():
    """Docstring
    """
    return defaultdict(input_tree)


def get_gamestate(save_name):
    """Docstring
    """
    with open(f"{save_name}", "r") as fileio:
        lines = fileio.read().splitlines()
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
    return gamestate

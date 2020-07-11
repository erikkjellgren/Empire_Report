import os

import matplotlib.pyplot as plt

from analyse_stats import get_gdp, get_pops, get_resource_stats, get_resource_stats_detailed


def write_report(save_name):
    """Docstring
    """
    if not os.path.exists("report"):
        os.makedirs("report")
    size = 12
    plt.rc("font", size=size)  # controls default text sizes
    plt.rc("axes", titlesize=size)  # fontsize of the axes title
    plt.rc("axes", labelsize=size)  # fontsize of the x any y labels
    plt.rc("xtick", labelsize=size)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=size)  # fontsize of the tick labels
    plt.rc("legend", fontsize=size)  # legend fontsize
    plt.rc("figure", titlesize=size)  # size of the figure title

    index_file = open("report/index.rst", "w")
    index_file.write("Stellaris GameStats\n")
    index_file.write(f'{"="*len("Stellaris GameStats")}\n\n')
    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 2\n")
    index_file.write("   :caption: Summary\n\n")

    resource_groups = [
        ["energy", "minerals", "food"],
        ["alloys", "consumer_goods"],
        ["volatile_motes", "rare_crystals", "exotic_gases"],
        ["sr_dark_matter", "sr_living_metal", "sr_zro"],
        ["unity", "physics_research", "society_research", "engineering_research"],
    ]
    index_file.write(f"   summary.rst\n")
    summary_file = open(f"report/summary.rst", "w")
    for resource_group in resource_groups:
        summary_file.write(f'{"".join(map(str, resource_group))}\n')
        summary_file.write(f'{"="*len("".join(map(str, resource_group)))}\n\n')
        summary_file.write(f'.. image:: {"".join(map(str, resource_group))}.png\n')
        summary_file.write(f"   :width: 480\n\n")
        time_array, stat1 = get_resource_stats(resource_group[0], save_name)
        time_array, stat2 = get_resource_stats(resource_group[1], save_name)
        if len(resource_group) > 2:
            time_array, stat3 = get_resource_stats(resource_group[2], save_name)
        if len(resource_group) > 3:
            time_array, stat4 = get_resource_stats(resource_group[3], save_name)
        if "unity" in resource_group:
            sizex = 5
            sizey = 5
            _, ax1 = plt.subplots(1, 1, figsize=(sizex, sizey))
        else:
            sizex = 5
            sizey = 10
            _, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(sizex, sizey))
        ax1.plot(time_array[2, :], stat1[0, :], label=resource_group[0])
        ax1.plot(time_array[2, :], stat2[0, :], label=resource_group[1])
        if len(resource_group) > 2:
            ax1.plot(time_array[2, :], stat3[0, :], label=resource_group[2])
        if len(resource_group) > 3:
            ax1.plot(time_array[2, :], stat4[0, :], label=resource_group[3])
        if "unity" not in resource_group:
            ax2.plot(time_array[2, :], stat1[1, :])
            ax2.plot(time_array[2, :], stat2[1, :])
            if len(resource_group) > 2:
                ax2.plot(time_array[2, :], stat3[1, :])
            ax3.plot(time_array[2, :], stat1[0, :] - stat1[1, :])
            ax3.plot(time_array[2, :], stat2[0, :] - stat2[1, :])
            if len(resource_group) > 2:
                ax3.plot(time_array[2, :], stat3[0, :] - stat3[1, :])
            ax2.set_xlabel("Year")
            ax3.set_xlabel("Year")
            ax2.set_ylabel("Expenses Per Month")
            ax3.set_ylabel("Balance Per Month")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Income Per Month")
        ax1.legend(frameon=False)
        plt.tight_layout()
        plt.savefig(f'report/{"".join(map(str, resource_group))}.png')
        plt.close()

    # Population
    sizex = 5
    sizey = 5
    _, ax1 = plt.subplots(1, 1, figsize=(sizex, sizey))
    time_array, pops = get_pops(save_name)
    summary_file.write(f"Population\n")
    summary_file.write(f'{"="*len("Population")}\n\n')
    summary_file.write(f".. image:: pops.png\n")
    summary_file.write(f"   :width: 480\n\n")
    ax1.plot(time_array[2, :], pops)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Population")
    plt.tight_layout()
    plt.savefig(f"report/pops.png")
    plt.close()

    # GDP
    sizex = 8
    sizey = 4
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(sizex, sizey))
    time_array, gdp, gdp_per_capita = get_gdp(save_name)
    summary_file.write(f"Gross Domestic Product\n")
    summary_file.write(f'{"="*len("Gross Domestic Product")}\n\n')
    summary_file.write("GDP calculated according to the standard market place prices:\n\n")
    summary_file.write(f".. math::\n\n")
    summary_file.write(r"    \text{GDP} = &\text{Energy} + \text{Minerals} + \text{Food}\\" + "\n")
    summary_file.write(
        r"    &+ 10\left(\text{Volatile Motes} + \text{Rare Crystal} + \text{Exotic Gases}\right)\\" + "\n"
    )
    summary_file.write(
        r"    &+ 20\left(\text{Dark Matter} + \text{Living Metal} + \text{Zro}\right)" + "\n\n"
    )
    summary_file.write(f".. image:: gdp.png\n")
    summary_file.write(f"   :width: 960\n\n")
    ax1.plot(time_array[2, :], gdp)
    ax2.plot(time_array[2, :], gdp_per_capita)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("GDP")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("GDP per capita")
    plt.tight_layout()
    plt.savefig(f"report/gdp.png")
    plt.close()
    summary_file.close()

    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 2\n")
    index_file.write("   :caption: Per Resource\n\n")
    resources = [
        "energy",
        "minerals",
        "food",
        "alloys",
        "consumer_goods",
        "volatile_motes",
        "rare_crystals",
        "exotic_gases",
        "unity",
        "physics_research",
        "society_research",
        "engineering_research",
        "sr_dark_matter",
        "sr_living_metal",
        "sr_zro",
    ]
    index_file.write(f"   resource_detailed.rst\n")
    resource_file = open(f"report/resource_detailed.rst", "w")
    for resource in resources:
        resource_file.write(f"{resource}\n")
        resource_file.write(f'{"="*len(resource)}\n\n')
        resource_file.write(f".. image:: {resource}.png\n")
        resource_file.write(f"   :width: 960\n\n")

        (
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
        ) = get_resource_stats_detailed(resource, save_name)

        sizex = 8
        sizey = 8
        _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(sizex, sizey))
        ax1.stackplot(
            time_array[2, :],
            jobs[0, :],
            buildings[0, :],
            megastructures[0, :],
            pops[0, :],
            leaders[0, :],
            ships[0, :],
            starbases[0, :],
            stations[0, :],
            armies[0, :],
            trade[0, :],
            labels=[
                "Jobs",
                "Buildings",
                "Megastructures",
                "Pops",
                "Leaders",
                "Ships",
                "Starbases",
                "Stations",
                "Armies",
                "Trade",
            ],
        )
        ax2.stackplot(
            time_array[2, :],
            jobs[1, :],
            buildings[1, :],
            megastructures[1, :],
            pops[1, :],
            leaders[1, :],
            ships[1, :],
            starbases[1, :],
            stations[1, :],
            armies[1, :],
            trade[1, :],
            labels=[
                "Jobs",
                "Buildings",
                "Megastructures",
                "Pops",
                "Leaders",
                "Ships",
                "Starbases",
                "Stations",
                "Armies",
                "Trade",
            ],
        )

        total_income = (
            jobs[0, :]
            + buildings[0, :]
            + megastructures[0, :]
            + pops[0, :]
            + leaders[0, :]
            + ships[0, :]
            + starbases[0, :]
            + stations[0, :]
            + armies[0, :]
            + trade[0, :]
        )
        total_income[total_income == 0] = 0.01
        total_expenses = (
            jobs[1, :]
            + buildings[1, :]
            + megastructures[1, :]
            + pops[1, :]
            + leaders[1, :]
            + ships[1, :]
            + starbases[1, :]
            + stations[1, :]
            + armies[1, :]
            + trade[1, :]
        )
        total_expenses[total_expenses == 0] = 0.01
        ax3.stackplot(
            time_array[2, :],
            jobs[0, :] / total_income,
            buildings[0, :] / total_income,
            megastructures[0, :] / total_income,
            pops[0, :] / total_income,
            leaders[0, :] / total_income,
            ships[0, :] / total_income,
            starbases[0, :] / total_income,
            stations[0, :] / total_income,
            armies[0, :] / total_income,
            trade[0, :] / total_income,
            labels=[
                "Jobs",
                "Buildings",
                "Megastructures",
                "Pops",
                "Leaders",
                "Ships",
                "Starbases",
                "Stations",
                "Armies",
                "Trade",
            ],
        )
        ax4.stackplot(
            time_array[2, :],
            jobs[1, :] / total_expenses,
            buildings[1, :] / total_expenses,
            megastructures[1, :] / total_expenses,
            pops[1, :] / total_expenses,
            leaders[1, :] / total_expenses,
            ships[1, :] / total_expenses,
            starbases[1, :] / total_expenses,
            stations[1, :] / total_expenses,
            armies[1, :] / total_expenses,
            trade[1, :] / total_expenses,
            labels=[
                "Jobs",
                "Buildings",
                "Megastructures",
                "Pops",
                "Leaders",
                "Ships",
                "Starbases",
                "Stations",
                "Armies",
                "Trade",
            ],
        )

        ax1.set_xlabel("Year")
        ax1.set_ylabel(f"{resource} Income Per Month")
        ax2.set_xlabel("Year")
        ax2.set_ylabel(f"{resource}  Expenses Per Month")
        ax3.set_xlabel("Year")
        ax3.set_ylabel(f"{resource}  Income Per Month %")
        ax4.set_xlabel("Year")
        ax4.set_ylabel(f"{resource}  Expenses Per Month %")
        ax1.legend(frameon=False, loc=2)
        ax2.legend(frameon=False, loc=2)
        ax3.set_ylim(0, 1)
        ax3.set_xlim(time_array[2, 0], time_array[2, -1])
        ax4.set_ylim(0, 1)
        ax4.set_xlim(time_array[2, 0], time_array[2, -1])

        plt.tight_layout()
        plt.savefig(f"report/{resource}.png")
        plt.close()
    resource_file.close()
    index_file.close()


write_report("thrashiantechnocrat7_-1184343043")

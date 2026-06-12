import json
from entities import Player
from engine import game
from world import set_job_items, STARTING_ROOM
from term_utils import cls, wait_enter, slowrite, low_strip, end_game, apply_art


def main():
    cls()

    start_data = load_start("start.json")

    # prints logo
    slowrite(apply_art(start_data["logo"][0], "tarty1", "green"))

    # prints rest
    slowrite(low_strip(start_data["logo"][1:], "cybermedium", "green"))

    wait_enter()

    # prints intro and asks for a job
    intro = "\n".join(start_data["common"]).expandtabs(1)
    slowrite(intro + "\n")
    job = input("> ").lower().strip()

    player = create_player(job)

    # if player is unemployed skip this, starts game that ends immediatlely
    if player.job != "unemployed":

        # create two-by-four or lart
        set_job_items(job)

        # prints intro based on job
        cls()
        for intro in start_data[player.job]:
            slowrite("\n".join(start_data[player.job][intro]) + "\n")
            wait_enter()

        slowrite("\n".join(start_data["help"]) + "\n")
        wait_enter()

    starting_id = STARTING_ROOM

    # game starts here
    end = game(starting_id, player)

    slowrite(end_game(end))


def load_start(start_file):
    with open(start_file, "r") as start:
        return json.load(start)


def get_job(job):
    job = job.lower().strip()
    return job if job in ["hp", "bofh"] else None


def create_player(job):
    if job == "hp":
        return Player("hp", 3, 3)
    elif job == "bofh":
        return Player("bofh", 2, 2)
    else:
        return Player("unemployed")


if __name__ == "__main__":
    main()

import json
import re
from world import get_room, get_job_item
from combat import attack, lart_attack
from map_fn import visited_layout
from term_utils import wait_enter, slowrite, cls

with open("help.json", "r") as help:
    help_data = json.load(help)


# player and id are not used in help function
# they are still passed as arguments to be group called in router

def help(player, argument, id):
    if argument != "":
        return "You meant help?\n"
    return f"{'\n'.join(help_data["entries"])}"


def status(player, argument, id):  # returns player info such hit points and inventory
    if argument != "":
        return "You meant status?\n"

    status = "Job: "

    if player.job == "hp":
        status += "HEMA Professional\n\n"
    else:
        status += "Bastard Operator From Hell\n\n"

    status += (
        f"Hit points: {str(player.hit_points)} out of {str(player.max_hit_points)}\n\n"
    )

    status += f"Location: {get_room(id).name.upper()}\n\n"
    status += "Inventory: "

    if not player.inventory:
        status += "you have no items."
    else:
        items = list()
        for item in player.inventory:
            items.append(player.inventory[item].name)
        status += ", ".join(items) + "."

    status += "\n"
    return status


def go(
    player, direction, id
):  # returns new room, can be the same if direction is invalid

    room = get_room(id)

    valid_directions = {"n", "north", "s", "south", "w", "west", "e", "east"}

    if direction not in valid_directions:
        slowrite("That's not a valid direction!\n")

    elif hasattr(room, "enemy") and direction[0] in room.enemy.lock_directions:
        slowrite(
            f"{room.enemy.name.upper()} prevents you going {get_direction(direction[0])}!\n"
        )

    elif direction[0] in room.routes:  # world uses n,s,w,e for brevity
        new_id = room.routes[direction[0]]

        if hasattr(get_room(new_id), "lock"):
            slowrite("Room locked!\n")
        else:
            slowrite(f"{player.job.upper()} goes to {get_direction(direction[0])}\n")
            return new_id

    else:  # if a direction is valid but not in route
        slowrite("You can't go there!\n")

    return id


def get_direction(direction):  # gets long direction (eg  w -->  west)
    map_directions = {"n": "north", "s": "south", "w": "west", "e": "east"}
    return map_directions[direction]


def take(
    player, item_name, id
):  # moves item to room.loot to player.inventory, if possible

    room = get_room(id)

    if item_name in player.inventory:
        return "You already have that.\n"
    elif item_name not in room.loot:
        return "Take what?\n"
    elif player.job in room.loot[item_name].allowed_jobs:
        if hasattr(room, "enemy"):
            return f"{room.enemy.name.upper()} prevents you to take {item_name}!\n"
        player.inventory[item_name] = room.loot[item_name]
        del room.loot[item_name]
        return f"You take {player.inventory[item_name].name}\n"
    elif item_name in room.loot and room.loot[item_name].allowed_jobs:
        # item collectible but non for the current job, returns conditional string
        return (
            "You aren't interested in nerd stuff!\n"
            if player.job == "hp"
            else "This stuff is for fanatics, you don't want touch it!\n"
        )
    else:  # item not collectible
        return "You can't take that!\n"


def look(player, name, id):  # return room, item or enemy detail
    room = get_room(id)

    if name == "":
        return room.description + "\n"

    elif name == "map":
        return visited_layout(id)

    elif name in room.loot:
        if name == "lart":
            get_job_item("lart").look = True
        return room.loot[name].description + "\n"

    elif name in player.inventory:
        if name == "lart":
            get_job_item("lart").look = True
        return player.inventory[name].description + "\n"

    # checks if room has an enemy and if you are looking for that enemy
    elif hasattr(room, "enemy") and name == room.enemy.name.lower():
        return room.enemy.description + "\n"

    return "Look at what?\n"


def use(player, item_name, id):
    room = get_room(id)
    if item_name == "keypad":

        if item_name not in room.loot:
            return "There are no keypads here!\n"

        if hasattr(room, "enemy"):
            return f"{room.enemy.name.upper()} prevents you to use {item_name}!\n"

        if "keycard" not in player.inventory:
            return "You need an authorized keycard!\n"

        password, unlock_id = (
            room.loot["keypad"].password,
            room.loot["keypad"].unlock_id,
        )

        if not hasattr(get_room(unlock_id), "lock"):
            return "Already unlocked!\n"

        if check_password(password):
            delattr(get_room(unlock_id), "lock")
            return "Room unlocked!\n"
        else:
            return "Wrong password"

    elif item_name == "imperial stout":
        if item_name in player.inventory:
            del player.inventory[item_name]
        elif item_name in room.loot:
            del room.loot[item_name]
        else:
            return "You can't use that!\n"

        player.heal(2)
        return "You feel better\n"

    else:
        return "You can't use that!\n"


# handles room unlock with password, unlocked id is inside keypad Item
def check_password(password):
    slowrite("Enter password:\n")
    if (input("> ")) == password:
        return True
    else:
        return False


def press(player, item_name, id):  # implemented for button
    valid_buttons = {"button", "blue button", "red button", "winged button"}
    room = get_room(id)

    if item_name not in valid_buttons or item_name not in room.loot:
        return "Press what?\n"

    else:
        locked_room = get_room(
            room.loot[item_name].unlock_id
        )  # room unlocked by button

        if hasattr(room, "enemy"):
            return f"{room.enemy.name.upper()} prevents you to press {item_name}!\n"
        elif hasattr(locked_room, "lock"):
            delattr(locked_room, "lock")
            return (
                "You press the button with all your might and unlock a door!\n"
                if player.job == "hp"
                else "You unlock a door just pressing this button. What kind of security is that?\n"
            )
        else:
            return "This seems to do nothing\n"


fn = {
    "help": help,
    "status": status,
    "take": take,
    "look": look,
    "use": use,
    "press": press,
    "attack": attack,
    "lart": lart_attack,
}


def router(player, id, tokens):
    try:  # checks if syntax is valid
        command, whitespace, argument = tokens
    except TypeError:
        slowrite("I don't understand.\n")
        return id

    if not whitespace and argument:
        slowrite("Whitespaces are free!\n")  # remarks wrong syntax

    args = (player, argument, id)

    if command == "go":
        return go(*args)

    else:
        slowrite(fn[command](*args))
        wait_enter()
        return id


def available_directions(id):  # adds avaliable directions each cycle
    room = get_room(id)
    open_directions = list()
    closed_directions = list()
    for direction in get_room(id).routes:
        if hasattr(get_room(room.routes[direction]), "lock"):
            closed_directions.append(get_direction(direction))
        else:
            open_directions.append(get_direction(direction))

    open_str = ", ".join(open_directions)
    closed_str = ", ".join(closed_directions)

    return_str = ""

    if open_str:
        return_str += f"\nYou can go to: {', '.join(open_directions)}."

    if closed_str:
        return_str += f"\nLocked: {', '.join(closed_directions)}."

    return return_str


def game(starting_id, player):
    cls()

    # game over if not hp of bofh
    if player.job == "unemployed":
        return end(player, "fail")

    id = starting_id
    while True:
        if check_end(id, player):  # checks win condition
            return end((player), check_end(id, player))  # returns ending string
        slowrite(f"{get_room(id)}\n{available_directions(id)}")
        slowrite("\nWhat do you do?\n")
        tokens = parse(input("> "))
        cls()
        id = router(player, id, tokens)


def check_end(id, player):
    if player.hit_points <= 0:
        return "fail"
    elif id == "6":
        return "standard_win"
    elif id == "0":
        return "full_win"
    else:
        return False


def end(player, win):

    with open("scores.json", "r") as scores:
        scores_data = json.load(scores)
    if win != "fail":
        # prints room description
        slowrite("\n".join(scores_data[win]))
        wait_enter()
        # prints customized end
        slowrite("\n".join(scores_data[player.job][win]["end"]))
        wait_enter()

    slowrite("Your adventure ends!\n")
    wait_enter()

    ending = "\n".join(scores_data[player.job][win][get_tier(player.score)])
    slowrite(ending)
    wait_enter()

    return win


def get_tier(score):  # used to get ending string
    if score == 0:
        return "0"
    elif score == 1:
        return "1"
    elif score < 5:
        return "2"
    elif score < 10:
        return "3"
    elif score < 15:
        return "4"
    else:
        return "5"


def parse(action):  # tokenizes input sentence
    allowed_commands = [
        "help",
        "status",
        "go",
        "take",
        "look",
        "use",
        "press",
        "attack",
        "lart",
    ]
    reg_commands = "|".join(allowed_commands)

    if words := re.search(
        r"^({commands})(\s*)(.*)".format(commands=reg_commands), action.lower().strip()
    ):
        return words.groups()

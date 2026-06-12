from world import get_room, get_job_item
import json

with open("enemies.json", "r") as enemies:
    enemies_data = json.load(enemies)


def attack(player, enemy_name, id):  # used with attack command
    room = get_room(id)
    if not hasattr(room, "enemy") or room.enemy.name != enemy_name:
        return "Attack who?\n"
    elif player.job == "hp":
        return hp(player, room.enemy, room)
    else:
        return bofh(player, room.enemy, room)


def hp(player, enemy, room):  # checks for hp gear and calculate damage

    if "power armor" in player.inventory:
        gear = "armor"

    elif "excalibur" in player.inventory:
        gear = "excalibur"

    else:
        gear = "none"

    damage = int(enemies_data[enemy.name][player.job][gear]["damage"])

    return combat(player, enemy, room, gear, damage)


def bofh(player, enemy, room):  # checks for hp gear and calculate damage
    gear = ""

    if "laptop" in player.inventory:
        gear = "laptop"
    else:
        gear = "none"

    damage = int(enemies_data[enemy.name][player.job][gear]["damage"])

    return combat(player, enemy, room, gear, damage)


def combat(player, enemy, room, gear, damage):  # combat result

    if player.hit_points > damage:  # player can go on
        player.score += int(enemies_data[enemy.name]["xp"])
        delattr(room, "enemy")

        win_message = "\n".join(enemies_data[enemy.name][player.job][gear]["win"])
        return f"{win_message} {player.get_hit(damage)}\n"

    else:  # player incapacitated
        loss_message = "\n".join(enemies_data[enemy.name][player.job][gear]["loss"])
        return f"{loss_message} {player.get_hit(damage)}.\nYou are out of Megacorp and not able to enter ever again.\n"


def lart_attack(player, enemy_name, id):  # used with lart command
    non_lusers = {"mech"}
    room = get_room(id)

    if get_job_item("lart").look == False:
        return "I don't understand.\n"

    if "lart" not in player.inventory:
        return "You need to pick it up first!\n"

    elif not hasattr(room, "enemy") or room.enemy.name != enemy_name:
        return "LART what? LART who? This is not a toy, use with care!\n"

    elif enemy_name in non_lusers:
        return f"{enemy_name} is not a luser, what were you thinking?\n"

    else:
        delattr(room, "enemy")
        player.score += int(enemies_data[enemy_name]["xp"])
        return "\n".join(enemies_data[enemy_name]["bofh"]["lart"]) + "\n"

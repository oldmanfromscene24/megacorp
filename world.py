from entities import Room, Item, Enemy
from random import randint
import json

STARTING_ROOM = "15"


# read items
with open("items.json", "r") as items:
    items_data = json.load(items)

# read enemies
with open("enemies.json", "r") as enemies:
    enemies_data = json.load(enemies)

# read rooms
with open("rooms.json", "r") as rooms:
    rooms_data = json.load(rooms)

# read job_items = created depending on job
with open("job_items.json", "r") as job_items:
    job_items_data = json.load(job_items)


def create_item(name, data):
    return Item(
        data[name]["id"],
        data[name]["name"],
        "\n".join(data[name]["description"]),
        data[name]["allowed_jobs"],
    )


def create_enemy(name):  # id is room id, used to spawn enemy in the correct room
    return Enemy(
        enemies_data[name]["id"],
        enemies_data[name]["name"],
        "\n".join(enemies_data[name]["description"]),
        enemies_data[name]["lock_directions"],
    )


def get_room(id):  # avoids to export rooms
    return rooms[int(id)]


def set_job_items(job):
    for name, item in job_items_dict.items():
        if item.allowed_jobs[0] == job:
            get_room(item.id).loot[name] = item


def get_job_item(job):
    return job_items_dict[job]


# loads items
items_dict = {}
for item in items_data:
    items_dict[item] = create_item(item, items_data)

# loads job_items
job_items_dict = {}
for job_item in job_items_data:
    job_items_dict[job_item] = create_item(job_item, job_items_data)

# set specific items properties
items_dict["keypad"].password = str(randint(0, 999999)).zfill(6)
items_dict["keypad"].unlock_id = "9"

items_dict["blue note"].description += items_dict["keypad"].password[:3]
items_dict["red note"].description += items_dict["keypad"].password[3:]

items_dict["winged button"].pressed = False
items_dict["winged button"].unlock_id = "3"

items_dict["blue button"].pressed = False
items_dict["blue button"].unlock_id = "23"

items_dict["red button"].pressed = False
items_dict["red button"].unlock_id = "22"

items_dict["button"].pressed = False
items_dict["button"].unlock_id = "21"


job_items_dict["lart"].look = False

# build loot
loot = {}
for name, item in items_dict.items():
    id = item.id
    if id not in loot:
        loot[id] = {}
    loot[id][name] = item

# spawn enemies
enemy_spawns = {id["id"]: create_enemy(name) for name, id in enemies_data.items()}


# locked ids
locked_ids = {"3", "9", "21", "22", "23"}


# Create world
rooms = []
for id in rooms_data:
    room = rooms_data[id]
    rooms.append(Room(id, room["name"], "\n".join(room["description"]), room["routes"]))
    if id in loot:
        rooms[int(id)].loot = loot[id]
    if id in locked_ids:
        rooms[int(id)].lock = True
    if id in enemy_spawns:
        rooms[int(id)].enemy = enemy_spawns[id]

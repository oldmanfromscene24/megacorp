# MEGACORP
## Video Demo: https://www.youtube.com/watch?v=clhjnjwTU5w

## Description: MEGACORP is a short and silly text adventure with a cyberpunk setting.

### Note
This is the original project I submitted for CS50P. Additionally, it has been integrated with PyScript and deployed to Cloudflare Pages to play it online at https://megacorp-text-adventure.pages.dev/

### How to run
Install required libraries with `pip install -r requirements.txt`.
Run python `project.py` in your terminal to start the game.

### Quick customization
- to add enemies, use `enemies.json`
- to add items, use `items.json`
- to add items only to a job, use `job_items.json`
- to add rooms, use `rooms.json`
- to set specific item properties, use `world.py` (check for "# set specific items properties comment")
- to lock a room, use `world.py` `locked_ids` set
- of course, you can edit all `JSON` to adapt various descriptions

Further customizations imply deeper modifications.

### General design:
The game is built with some scalability in mind.
While it's not perfect, like having to define special properties in `world.py` file and not with class methods, and some things are cumbersome, like having to write lots of text for combat (but, in return you can fine tune it) you can add rooms, enemies and items fairly easily.
I tried to avoid `if` statements and use dictionaries instead of them.
I used sets where possible if i have to check if something is in a group of values.
I used json to store descriptions, some are quite long.
I replaced all `print` statements with a function called `slowrite` that has a small, random delay between characters.
I used art and termcolor as external libraries, they are used at the start and at the end.
There is just one `try... except` block. The program intentionally relies on file consistency, if they are not properly configured, the program will fail. And that's fine, because going on without consistency will lead to unexpected behaviour. If there's something wrong in the file, the standard error should point out where the problem is.
On the user side, all inputs are accepted, the worst thing that could happen is being asked for a command again.

### Features:
- 2 types of player characters to choose from, named jobs
- over 20 interconnected rooms
- some enemies, but no one dies
- many items with various uses
- a puzzle
- a secret, locked command
- a standard ending and a true ending, you can also lose
- many commands, the most notable being `look map`, which draws recursively the visited map starting from current room
- minimal ASCII art during the opening and closing of the game
- lots of descriptions stored in `JSON` files
- nerd, hema, medieval and renaissance references

### Overview:
It's possible to add rooms, items and enemies just editing the relative json.
Extra properties need to be added in the code; this is done in the `world.py` file.
It's also possible to initialize different items for the two jobs. For example, a job could recognize an item and the other not.

## Python file details

### combat.py
Handles combat logic. Combat is invoked with the attack command and is autoresolved checking `player.inventory` and `player.hit_points`. The result is read in `enemies.json` and is fully customized for each enemy and job.

#### functions overview:
- `attack`: used with `attack` command, checks enemy presence and invokes functions depending on `player.job`
- `hp`: checks for hp gear and calculate damage
- `bofh`: checks for bofh gear and calculate damage
- `combat`: resolves combat based on previous functions
- `lart_attack`: handles special bofh attack. Works only if lart has been looked upon

### engine.py
Core gameplay logic is here.
`while True` is called by the `game` function.
If the job is valid the game starts, otherwise a fail string is displayed and the game ends.
The game cycle is a `while True` with an end check as escape. It returns an end string if the end condition is true.
Then, it prints room details and asks for an action.
The input is processed by the `parse` function.
Then the `router` is responsible for elaborating the tokens and returns a new room id for the cycle. The id can be the same, meaning the action is not changing the room.
Enemies can prevent some actions and need to be dealt with to make them possible.
Input takes the whitespace between command and argument and renders it optional: you can write `go n` or `gon` and it will still work but points out that whitespaces are free. It doesn't break multy word arguments. For example, `press red button` or `pressred button` works (the argument red button still needs space).


#### functions overview:
- `help`: display a list of commands
- `status`: returns player info such as hit points and inventory
- `go`: goes in the specified direction. It's the only function that moves to another room and the most used command. valid_directions = {"n", "north", "s", "south", "w", "west", "e", "east"} 
- `get_direction`: helper function used to print long direction (n or north both return north and so on)
- `take`: moves an item from a room to the inventory, if possible
- `look`: this is the most complex command. Refer to the ingame `help` for usage (or check in `help.json`)
- `use`: to use some items (keypads and imperial stout)
- `check_password`: used by keypads
- `press`: for buttons, unlock rooms
- `router`: main orchestrator, calls other functions and returns a room id. If the input is invalid it asks again for a command
- `available_directions`: returns available directions of the current room
- `game`: called by main, the main cycle is here. Checks for end, calls `parse` and `router`
- `check_end`: checks for player.hit_points or if player is in an end room
- `end`: if `check_end` is true, prints ending and return win condition
- `get_tier`: returns tier based on score, needed by `end` function to print ending
- `parse`: tokenizes input, accepts all input. If it's not allowed, returns None

### entities.py
Here is where the classes reside.
An `Enemy` is defined as a property of a `Room`. A `Room` can have only 1 enemy. For the scope of the game, more in a room are not needed. More enemies in a room would be treated as single entities and it would not be believable they would not cooperate. A workaround could be to create a single enemy object for more opponents and manage the encounter with `enemies.json` content.
Some properties are `dict` initialized with `None` and checked to prevent mutable default argument problems, they are still initialized for comfort.

#### classes overview:

`Room`: 
- `id`: room identifier, it must be unique
- `name`: name of room
- `description`: description of room
- `routes`: dictionary pairing directions and `id` of next room
- `loot`: a dictionary of items it contains, {name : item}
- `visited`: set to `False`, changes upon visit
- `__str__`: returns room `str`
- `print_all`: returns a `str` with room details

`Enemy`:
- `id`: room `id` where this enemy spawns
- `name`: name of enemy
- `description`: description of enemy
- `lock_directions`: prevents the player from moving in those directions if enenmy is present

`Player`:
- `job`: character class
- `hit_points`: current hit points, they cannot exceed `max_hit_point`
- `max_hit_point`: maximum hit points
- `inventory`: dict of items in `player.inventory`. It has no limits, so it should satisfy compulsive hoarders like myself
- `score`: current score. Needed to get end strings.
- `heal`: increase hit points, they cannot exceed `max_hit_point`
- `get_hit`: decrease hit points and returns a `str` of damage


`Item`:
- `id`: room `id` where this item spawns
- `name`: name of item
- `description`: description of item
- `allowed_jobs`: set with jobs allowed to pick up that item. If empty, the item cannot be picked up


### map_fn.py
This is used to print a map with explored rooms and a legend. Rooms are identified by their id. Room connections are printed.
The legend prints room id, room name, uncharted directions and points out where the player is.
The map is drawn by a recursive function that checks for visited rooms. The traversal starts from the id where the function is invoked.
If a room is locked, it is not displayed in uncharted. If you unlock the room and the adjacent room is visited, the direction to the newly unlocked room becomes uncharted even if you are not there.
Initially, this was not planned, but it seemed a nice feature to have and a decent challenge. I learnt about mutable default arguments. Initially the function was working only if starting exploring from the start room, because there was a default value in `track_map`. Then i fixed it by initializing the value to `None` and setting a new empty dict if value is `None`. Then i refactored the function because it was overcomplicated. At last, i removed defaults and streamlined the code.

#### functions overview:
- `track_map`: recursive function that tracks visited rooms, returns a dictionary {coordinates: room} of visited rooms, starts exploring in the room it was called from. Current room has (0,0) coordinates. North is (0,-1), south (0,1), west (-1,0), east (1,0). If you remove `if not room.visited` check, the dictionary will contain all rooms and `look map` will output the complete map, which can be useful for debugging.
- `visited_layout`: returns the full string of the map
- `get_bounds`: gets min and max coordinates from `track_map`
- `get_map_string`: returns a string representation of the map of visited rooms with connections
- `get_legend`: returns legend string
- `check_directions`: returns joined string of unexplored directions without locked ones

### project.py
Main file.

#### functions overview:
- `main`: prints intro, asks for a job, creates player, sets `job_items` (some items can be created only for a job), calls `game`, calls `end`
- `load_start`: loads `start.json` content in a dict
- `get_job`: clean job string if is valid and returns it, otherwise returns None
- `create_player`: creates player object depending on job

### term_utils.py
Some tools needed to prettify the experience

#### functions overview:
- `cls`: clear screen
- `wait_enter`: a `slowrite` with an `input` followed by a `cls`
- `slowrite`: prints with a delay between characters; simulates very fast typing or a very slow computer
- `low_strip`: used to cut bottom extra space from art `cybermedium` characters on first screen
- `end_game`: returns last characters with art and termcolor
- `apply_art`: returns character of first screen

### test_project.py
Tests functions in `project.py`, main aside.

### world.py
Builds the worlds and handles specific cases.
Note on locked rooms: for simplicity there are no actual doors. A room can be locked, that means it is not reachable by any direction and when is unlocked, it is reachable by any valid direction. It's much simpler than implementing doors and for a game of this scope is just fine. Locked rooms are specified in the `locked_ids` set.

#### functions overview:
- `create_items`: creates items from `items_data` that come from `items.json`. Id is room id spawn
- `create_enemy`: creates enemy from `enemies_data` that comes from `enemies.json`. Id is room id spawn
- `get_room`: returns room object from his id. Avoids exporting rooms
- `set_job_items`: creates job items from `job_items_data` that come from `job_items.json`. Id is room id spawn

#### other:
- `items_dict`: creates all base items
- `job_items_dict`: creates all base job_items
- `keypad`: has a random password. In the game the code is broken in two. unlock_id is the room that is unlocked completing the puzzle
- various buttons: set `pressed` to `False`. `unlock_id` is the `id` locked when the button is pressed
- after setting properties, a dict is built. It stores various items by `id`, an `id` can have multiple items and is used to build loot of the room
- `enemy_spawns`: spawn enemies in the correct rooms
- `locked_ids`: specify locked rooms
- `rooms`: builds all rooms with `id`, `name`, `description` and `routes`. Checks for `loot`, `lock` and `enemy_spawns` and builds all.

## JSON details:
`JSON` contents are lists. In the game, `JSON` are loaded as dictionaries and the lists are joined with "\n" to get a `str`.
In general, `JSON` keys corresponds to `Class` properties where applicable.

### enemies.json
Contains:
- `id`: room id spawn
- `name`: enemy name
- `description`: enemy descriptions
- `lock_directions`: if an enemy is in the room, you cannot move in these directions
- `xp`: score increase when defeated
- job stats: set damage taken by player per job, win or loss and equipment

### help.json
Displays standard commands.

### items.json
Contains:
- `id`: room id spawn
- `name`: item name
- `description`: item description
- `allowed_jobs`: which job can pick it up. If left empty, no one can take it.

### job_items.json
As items, but allowed_jobs must contain one job and the item is created only for that job. This allows to customize the same ingame item for a given job, of course the code item is different. This seems much easier than conditionally building an item.

### rooms.json
Contains:
- `name`: room name
- `description`: this is shown only if `room.visited == False` or with the `look` command
- `routes`: dictionary pairing directions and id of next room

### scores.json
The standard win and full win are mock room descriptions. When those rooms are reached, `game` calls `check_end` which checks for the win condition, one of which is based on reaching certain rooms by their id, before printing the room.

Contains:
- `standard_win`: used to print last room of standard win
- `full_win`: used to print last room of full win
- content based on the job, the win condition, and the score

### start.json
Contains:
- `"logo"`: used on start screen
- `"common"`: used on the job selection screen
- content based on class selection, serves as a customized intro
- `"help"`: informs the player about help function before entering the game

## Misc

### requirements.txt
Lists external libraries, used to install them with pip install -r requirements.txt .

### README.md
This file.

### spoilers.txt
Full map of the game. Avoid looking at it if you plan to play the game!


## Acknowledgements
I borrowed lots of ideas for my text.
Only the MEGACORP acronym is mine, and it stands for:
Megacorp
Engineered
Gears
Aids
Chivalry
Obsessed
Reenactment
Professionals

Main inspirations were:
- Simon Travaglia for BOFH and LART (i haven't read his works, but i should)
- The Wallace Collection: they posted some of the coolest armor photos you can find
- Robocop for Enforcement Droid
- Terminator for Skynet
- Gene Wolfe for Autarch Citadel, not to mention his fantastic books
- Cyberpunk, nerd and HEMA culture
- Renaissance, medieval, Escher and Giger art


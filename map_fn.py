from world import get_room


# returns a dictionary {coordinates: room} of visited rooms, start exploring in room called
def track_map(room, pos, traversed_rooms):

    # if room is already visited by function, skip it
    if pos in traversed_rooms:
        return
    # if room is not already visited dy player, skip it
    if not room.visited:
        return

    traversed_rooms[pos] = (
        room  # tracks room traversed by track map and stores coordinates
    )

    directions = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}

    # checks if a direction exists and is not traversed by track.
    for direction in directions:
        # no need to check next room existance, if direction is in routes the room must exists, otherwise the error is in json
        if direction in room.routes:
            offset = directions[direction]
            next_pos = (pos[0] + offset[0], pos[1] + offset[1])
            next_room = get_room(room.routes[direction])
            track_map(next_room, next_pos, traversed_rooms)

    return traversed_rooms


def visited_layout(id):  # returns string of map visited by player and legend

    visited_rooms = track_map(get_room(id), (0, 0), {})

    bounds = get_bounds(visited_rooms)

    map_string = get_map_string(visited_rooms, bounds)

    map_string += "\n"

    map_string += get_legend(visited_rooms, id)

    return map_string


def get_bounds(visited_rooms):
    x_coordinates = [x for x, y in visited_rooms.keys()]
    y_coordinates = [y for x, y in visited_rooms.keys()]

    return (
        min(x_coordinates),
        max(x_coordinates),
        min(y_coordinates),
        max(y_coordinates),
    )


# returns maps of string of visited rooms with connections
def get_map_string(visited_rooms, bounds, map_string=""):
    min_x, max_x, min_y, max_y = bounds
    width = 4
    blank = f"{'':<{width}}"
    pipe = f"{'|':<{width}}"
    for h in range(min_y, max_y + 1):
        found = (
            []
        )  # tracks south connected rooms, used to print vertical connections "|"

        map_string += "\n"

        for w in range(min_x, max_x + 1):
            room_str = ""
            if (w, h) in visited_rooms:
                current_room = visited_rooms[w, h]
                try:
                    if (w + 1, h) in visited_rooms and visited_rooms[
                        w + 1, h
                    ].id == current_room.routes["e"]:
                        room_str = f"{current_room.id:-<{width}}"
                    else:
                        room_str = f"{current_room.id:<{width}}"
                except KeyError:
                    room_str = f"{current_room.id:<{width}}"

                try:  # checks if south room exists and if is in route of current room
                    if visited_rooms[(w, h + 1)].id == current_room.routes["s"]:
                        found.append(w)
                except KeyError:
                    pass
            else:
                room_str = blank
            map_string += room_str

        line = "\n"
        for w in range(min_x, max_x + 1):
            if w in found:
                line += pipe
            else:
                line += blank
        map_string += line

    return map_string


def get_legend(visited_rooms, id):  # returns legend string

    legend = list()
    for coordinates in visited_rooms:
        # current id (convert to int to sort later), current room name, returns directions if unexplored to not locked rooms
        entry = (
            int(visited_rooms[coordinates].id),
            visited_rooms[coordinates].name,
            check_directions(visited_rooms, visited_rooms[coordinates]),
        )
        legend.append(entry)

    full_legend = ""

    for entry in sorted(legend):
        current_id = str(entry[0])
        unexplored = ""
        if entry[2]:
            unexplored = f", uncharted: {entry[2]}"
        full_legend += f"{current_id} = {entry[1]}{unexplored}."

        if current_id == id:
            full_legend += " * YOU ARE HERE\n"
        else:
            full_legend += "\n"

    return full_legend


def check_directions(
    visited_rooms, room
):  # returns joined string of unexplored directions without locked ones
    directions = list()
    visited = list(visited_rooms.values())  # list of visited rooms

    for direction in ["n", "s", "w", "e"]:
        if direction in room.routes:
            next_room = get_room(room.routes[direction])
            if not hasattr(next_room, "lock") and next_room not in visited:
                directions.append(direction)

    return ", ".join(directions)

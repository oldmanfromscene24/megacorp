''' Some Class attributes are initialised to None to
prevent reference anomalies with mutable default arguments'''


class Room:
    def __init__(self, id, name, description, routes, loot=None, visited=False):
        self.id = id
        self.name = name
        self.description = description
        self.routes = routes

        if loot is None:
            self.loot = {}
        else:
            self.loot = loot

        self.visited = visited

    def __str__(self):
        return f"You are here: {self.name.upper()}{self.print_all()}"

    def print_all(self):#prints room details and set visited
        elements = ""
        if not self.visited:
            elements += f"\n{self.description}"
            self.visited = True

        if hasattr(self, "enemy"):
            elements += f"\n\n{self.enemy.name.upper()} is waiting for you."

        if self.loot:
            elements += "\n\nYou see:"
            for item in self.loot:
                elements += f"\n-{self.loot[item].name.capitalize()}"
        return elements


class Enemy:
    def __init__(self, id, name, description, lock_directions):
        self.id = id
        self.name = name
        self.description = description
        self.lock_directions = lock_directions


class Player:
    def __init__(self, job, hit_points=0, max_hit_points=0, inventory=None, score=0):
        self.job = job
        self.hit_points = hit_points
        self.max_hit_points = max_hit_points

        if inventory is None:
            self.inventory = {}
        else:
            self.inventory = inventory

        self.score = score

    def heal(self, points):
        if self.hit_points + points > self.max_hit_points:
            self.hit_points = self.max_hit_points
        else:
            self.hit_points += points

    def get_hit(self, damage):
        if damage == 0:
            return ""
        else:
            self.hit_points -= damage
            return f"You took {damage} damage.\n"


class Item:
    def __init__(self, id, name, description, allowed_jobs=None):
        self.id = id
        self.name = name
        self.description = description

        # sets who can collect the item, can be empty if not collectible
        if allowed_jobs is None:
            self.allowed_jobs = {}
        else:
            self.allowed_jobs = allowed_jobs

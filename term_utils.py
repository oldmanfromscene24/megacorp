import os
from random import uniform
import time
from art import *
from termcolor import colored


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    slowrite("Press ENTER to continue.")
    input("")
    cls()


def slowrite(text):
    for char in text:
        print(char, end="", flush=True)
        delay = uniform(0.001, 0.005)
        time.sleep(delay)
    print()


"""
takes a list of words
apply art with font specified
split art word in lines
remove last line that is likely empty
join lines
print all words, one per line
apply color
basically, it removes interline, works fine with cybermedium font
"""


def low_strip(word_list, font, color):
    full_form = []

    for word in word_list:

        word_art = text2art(word, font=font)
        lines = word_art.splitlines()
        lines = lines[:-1]
        full_form.append("\n".join(lines))

    return colored("\n".join(full_form), color)


def end_game(end):

    ends = {
        "fail": {"message": "YOU\nFAILED!", "color": "red", "font": "cyberlarge"},
        "standard_win": {
            "message": "VICTORY\nACHIEVED!",
            "color": "green",
            "font": "cyberlarge",
        },
        "full_win": {
            "message": "FULL\nVICTORY\nACHIEVED!",
            "color": "yellow",
            "font": "cyberlarge",
        },
    }

    color = ends[end]["color"]
    message = ends[end]["message"]
    font = ends[end]["font"]

    return colored(text2art(message, font=font), color)


# to avoid import art and termcolor in project
def apply_art(text, font, color):
    return colored(text2art(text, font=font), color)

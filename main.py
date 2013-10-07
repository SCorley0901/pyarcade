#!/usr/bin/env python
#
# Main
#
# Runs and manages PyArcade 1.0
#
# What is PyArcade?
#
# PyArcade is a very small collection of
# simple games made using the popular
# Pygame library and games.py (a wrapper
# for the library, updated to Python 3).
# It showcases the flexibility of programming
# games in Python.
#
# Requirements: Python 3.3.x and Pygame 1.9.2a0 (latest release)
#
# Download sites: * Python (http://python.org/download/)
#                 * Pygame (http://pygame.org/download.shtml)
#
# Programmer: Abner Coimbre
# http://github.com/abner7

"""Runs and manages PyArcade 1.0"""

name = input("PyArcade 1.0 -- Enter a player name (5 characters or less): ")

NAME = name[:5]

import sys

import pygame

from menu import Menu

import score

from utility import games, constants

# Games
# ------------------
from pong import Pong

from simon import Simon

from phone import Game
# ------------------

SCORE_FILES = {constants.PONG: "utility/pong_score.txt",
               constants.SIMON: "utility/simon_score.txt",
               constants.PHONE: "utility/phone_score.txt"}

def handle_input(menu):
    """
    Handle player input.

    Will handle the input given by the player
    when he or she was at the menu; e.g. start
    the game of Pong.
    
    Keyword argument:
    menu -- an instance of Menu() from menu.py
    
    """
    if games.keyboard.is_pressed(games.K_ESCAPE):
        games.music.stop()
        games.load_sound("sound/menu/exit.wav").play()
        pygame.time.wait(800)
        sys.exit(0)

    if menu.option == constants.EXIT:
        sys.exit(0)

    if menu.option == constants.SCORE:
        score.ScoreMenu().start()
        return

    if menu.option == constants.PONG:
        Pong().start()
    elif menu.option == constants.SIMON:
        Simon().start()
    else:
        Game().start() # [Note: Game() refers to the game "Save the Phone"]

    handle_score(menu.option)
        
    menu.option = None # Reset
    

def handle_score(option):
    """
    Add game points to high score.

    Keyword argument:
    option -- a valid value from menu.option or directly from
              constants.py
              
    """
    current_score = open("utility/current_score.txt", "r")

    # Score will not be added by the function if the player's
    # score doesn't make it to the current high score table.
    score.add_score(name=NAME,
                    value=int(current_score.read()),
                    txt_file_path = SCORE_FILES[option])

    current_score.close()
                   

def main():
    """Kickstart PyArcade."""
    menu = Menu()
    
    while True:
        # Start the menu. Here, the player sets values
        # for menu.option
        menu.start()

        # Once a value for menu.option is set (e.g. when
        # the player hits 'Enter' to play Pong), this
        # function will handle the event.
        handle_input(menu)
        
# start PyArcade
if __name__ == '__main__':
    main()

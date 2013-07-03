#/usr/bin/env python
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
# for the library, updated by Michael Dawson
# and myself --see the script for more details).
# It showcases the flexibility of programming
# games in Python.
#
# Requirements: Python 2.7.x and Pygame 1.9.2a0 (latest release)
#
# Download sites: * Python (http://python.org/download/)
#                 * Pygame (http://pygame.org/download.shtml)
#
# Programmer: Abner Coimbre
# http://github.com/abner7

"""Runs and manages PyArcade 1.0"""

name = raw_input("PyArcade 1.0 -- Enter a player name (5 characters or less): ")

NAME = name[:5]

import sys

import pygame

from menu import Menu

import score

from score import ScoreMenu

from utility import games, constants

# ------------------
# games
from pong import Pong

from simon import Simon

from phone import Game
# ------------------

def handle_input(menu):
    """
    Handle player input.

    Will handle the input given by the player
    when he or she was at the menu; e.g. start
    the game of Pong.
    
    Keyword argument:
    menu -- an instance of Menu() from menu.py
    
    """
    # Notice that one could avoid the multiple if statements, but it
    # might make the code a little less readable.
    if games.keyboard.is_pressed(games.K_ESCAPE):
            games.music.stop()
            games.load_sound("sound/menu/exit.wav").play()
            pygame.time.wait(800)
            sys.exit(0)
            
    current_score = open("utility/current_score.txt", "r")
        
    if menu.option == constants.PONG:
        Pong().start()
        score.add_score(name=NAME,
                        value=int(current_score.read()),
                        txt_file_path="utility/pong_score.txt")
                
    if menu.option == constants.SIMON:
        Simon().start()
        score.add_score(name = NAME,
                        value=int(current_score.read()),
                        txt_file_path = "utility/simon_score.txt")
            
    if menu.option == constants.PHONE:
        Game().start()
        score.add_score(name = NAME,
                        value=int(current_score.read()),
                        txt_file_path = "utility/phone_score.txt")
            
    if menu.option == constants.EXIT:
        sys.exit(0)
            
    if menu.option == constants.SCORE:
        ScoreMenu().start()

    menu.option = None # Reset

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
main()

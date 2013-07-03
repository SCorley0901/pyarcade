#/usr/bin/env python
#
# Menu Constants
#
# Used by main.py and menu.py
#
# E.g. If the player enters 'Pong' on
# the menu to play Pong, menu.py sets
# menu.option = PONG, which can later
# be used by main.py to verify:
#
# if menu.option == PONG:
#     Pong.start()
#
# This is important because menu.py cannot
# directly access the game modules --only
# main.py. Having a set of common constants
# helps the communication between these scripts.
#
# Programmer: Abner Coimbre

"""Menu constants used by main.py and menu.py"""

PONG = 0

SIMON = 1

PHONE = 2

EXIT = 3

SCORE = 4

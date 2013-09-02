#/usr/bin/env python
#
# Score
#
# PyArcade's Scoring System
#
# Programmer: Abner Coimbre

"""PyArcade's high score system."""

import sys

import pygame

from utility import games, color

if __name__ == '__main__':
    print("-score.py-\n")
    print("You ran this module directly. Try main.py\n")
    input("* Press the enter key to exit.")
    sys.exit(1)

EXIT = 0

NEXT = 1

def get_scores(txt_file_path):
    """
    Get the high scores from a game.
    
    Read from text file and return a list of the
    current high scores, where each element is a tuple
    containing two strings: player name and score.
    
    Text file must start with a player name, followed
    by his or her score below. This pattern should
    continue until the end of the file.

    Keyword argument:
    txt_file_path -- the path to the .txt high score file
    
    """
        
    score_file = open(txt_file_path, "r")
    
    temp_list = score_file.readlines()
    
    score_list = []
    
    i = 0
    while i < len(temp_list):
        score_list.append((temp_list[i].replace('\n',""),
                           temp_list[i+1].replace('\n',"")))
        i += 2
    
    score_file.close()
    
    return score_list


def check_score(value=0, txt_file_path="utility/pong_score.txt"):
    """
    Return True if given value makes it to the high score.

    Keyword arguments:
    value -- the int value to be checked
    txt_file_path -- the path to the .txt high score file. Default is
                     utility/pong_score.txt
    
    """
    scores = get_scores(txt_file_path)
    smallest_score = int(scores[len(scores)-1][1])

    if value > smallest_score:
        return True

    return False


def add_score(
        name="Player", value=0,
        game_title = "Pong",
        txt_file_path = "utility/pong_score.txt"):
    """
    Adds a high score to the file.

    Keyword arguments:
    name -- player name. Default is 'Player'
    value -- the int value to add as high score. Default is 0
    game_title -- the title of the game. Default is 'Pong'
    txt_file_path -- the path to the .txt high score file. Default is
                     utility/pong_score.txt
    
    """
    if not check_score(value, txt_file_path):
        return
    
    scores = get_scores(txt_file_path)

    for i in range(len(scores)):
        if value > int(scores[i][1]):
            scores.insert(i, (name, str(value)))
            break

    new_scores = open(txt_file_path, "w")

    # Only add top 5 high scores.
    for i in range(5):
        new_scores.write(scores[i][0] + '\n')
        new_scores.write(scores[i][1] + '\n')

    new_scores.close()
        

def show_scores(game_title="Pong", txt_file_path="utility/pong_score.txt"):
    """
    Show the high scores on the Pygame window.

    Keyword arguments:
    game_title -- the title of the game. Default is 'Pong'
    txt_file_path -- the path to the .txt high score file. Default is
                     utility/pong_score.txt
    
    """
    # Clear the screen (except the 'Exit' and 'Next' options).
    for sprite in games.screen.all_objects:
        if sprite not in ScoreMenu.all_options:
            if sprite != Cursor.cursor:
                sprite.destroy()
    
    # Load high scores
    high_scores = get_scores(txt_file_path)
    
    # Draw game title
    games.screen.add(games.Text(value = game_title,
                                size = 40,
                                color = color.white,
                                x = games.screen.width/2,
                                y = 30))
    
    
    y_offset = 0 # Used in 'draw numbers' and 'draw high
                 # scores on screen'.
    
    x_offset = 0 # Used in 'draw high scores on screen'
                 # to determine the number of pixels the player's
                 # score should be away from his or her name.
    
    # Draw numbers
    number_x_pos = 80
    for i in range(len(high_scores)):
        games.screen.add(games.Text(value = str(i+1) + ".",
                                    size = 35,
                                    color = color.white,
                                    x = number_x_pos,
                                    y = 165 + y_offset))
        y_offset += 50
    
    # Draw high scores on screen.
    # ---------------------------------
    y_offset = 0 # reset
    for player_score in high_scores:
        for item in player_score:
            games.screen.add(games.Text(value = item,
                                        size = 35,
                                        color = color.white,
                                        x = number_x_pos + 50 + x_offset,
                                        y = 165 + y_offset))
            x_offset += 380
        x_offset = 0
        y_offset += 50
    # ---------------------------------
    
    # Draw relevant info about high scores.
    info = "Player"
    games.screen.add(games.Text(value = info,
                                size = 45,
                                color = color.white,
                                x = number_x_pos + 35,
                                y = 115))
    if game_title.lower() == "simon says":
        info = "Sequences"
    elif game_title.lower() == "save the phone":
        info = "Objects Avoided"
    else:
        info = "Score"
    games.screen.add(games.Text(value = info,
                                size = 45,
                                color = color.white,
                                x = number_x_pos + games.screen.width - 220,
                                y = 115))


class Cursor(games.Sprite):
    """The cursor for the score's menu."""
    image = games.load_image("graphics/menu/cursor.png")

    cursor = None # Referencing its instance.
                  # Used by the show_scores() function.
    
    def __init__(self, menu):
        """Initialize the cursor."""
        super(Cursor, self).__init__(image=Cursor.image,
                                     x=0,
                                     y=0)

        Cursor.cursor = self
        
        self.menu = menu

        self.current_option = NEXT

        self.draw()

    def update(self):
        """Called at every frame."""
        self.check_input()

    def check_input(self):
        """Check for any player input while on the score menu."""
        if games.keyboard.is_pressed(games.K_RIGHT):
            if self.current_option == NEXT:
                return
            self.current_option = NEXT
            games.load_sound("sound/menu/cursor.wav").play()
            self.draw() # Update cursor's position
            return

        if games.keyboard.is_pressed(games.K_LEFT):
            if self.current_option == EXIT:
                return
            self.current_option = EXIT
            games.load_sound("sound/menu/cursor.wav").play()
            self.draw()
            return

        if games.keyboard.is_pressed(games.K_RETURN):
            # Exit game
            if self.current_option == EXIT:
                pygame.time.wait(500)
                games.screen.quit()
                return
            
            # Otherwise, show the next set of high scores
            games.load_sound("sound/menu/enter2.wav").play()
            pygame.time.wait(100)
            next = ScoreMenu.get_next()
            show_scores(next[0], next[1])
            
    def draw(self):
        """Draw the cursor at a new position"""
        screen = games.screen.display

        menu = self.menu.menu_options

        background = pygame.image.load("graphics/menu/background.png").convert()

        # Blit screen with background to erase previous drawing.
        screen.blit(background, (0,0))

        pygame.time.Clock().tick(15)

        # Make new drawing of the cursor.
        # -----------------------------------
        pos = (menu[self.current_option].left - 8,
               menu[self.current_option].y - 22,
               menu[self.current_option].width + 15,
               menu[self.current_option].height + 15)
        thickness = 3
        
        pygame.draw.rect(screen, color.yellow, pos, thickness)
        # -----------------------------------

        pygame.display.update()


class ScoreMenu(object):
    """PyArcade's score interface."""

    all_options = None

    high_scores = (("Pong", "utility/pong_score.txt"),
                   ("Simon Says", "utility/simon_score.txt"),
                   ("Save The Phone", "utility/phone_score.txt"))

    current_game = high_scores[0]

    def __init__(self):
        """Initialize PyArcade's score menu."""
        self.exit = games.Text(value="Exit",
                                size=35,
                                color=color.white,
                                x=50,
                                bottom=games.screen.height - 35)

        self.next = games.Text(value="Next",
                               size=35,
                               color=color.white,
                               x=games.screen.width - 45,
                               bottom=games.screen.height - 35)
        
        ScoreMenu.all_options = (self.exit, self.next)
        # ^ So it may be accessed by outside functions (such as show_scores()).
        # Equivalent to the get_options() method and its property 'options'.

        games.music.load("sound/menu/high_score_theme.wav")

    def start(self):
        """Start the score's menu."""
        games.screen.clear()

        games.screen.background = games.load_image("graphics/menu/background.png",
                                                   transparent=False)

        ScoreMenu.current_game = ScoreMenu.high_scores[0]

        games.screen.add(self.exit)

        games.screen.add(self.next)

        games.screen.add(Cursor(self))

        games.music.play(-1)

        show_scores("Pong", "utility/pong_score.txt")

        # Start Score Menu
        games.screen.mainloop()

    def get_menu_options(self):
        """Return the options available on the score menu."""
        return (self.exit, self.next)
    
    menu_options = property(get_menu_options)

    def get_next():
        """Return the next game being shown when 'Next' is pressed."""
        if ScoreMenu.current_game == ScoreMenu.high_scores[0]:
            ScoreMenu.current_game = ScoreMenu.high_scores[1]
            return ScoreMenu.current_game
        
        if ScoreMenu.current_game == ScoreMenu.high_scores[1]:
            ScoreMenu.current_game = ScoreMenu.high_scores[2]
            return ScoreMenu.current_game
        
        ScoreMenu.current_game = ScoreMenu.high_scores[0]
        return ScoreMenu.current_game
    
    get_next = staticmethod(get_next)
            

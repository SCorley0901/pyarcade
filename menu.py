#/usr/bin/env python
#
# Menu
#
# PyArcade's Menu
#
# Programmer: Abner Coimbre

"""PyArcade's menu system."""

import sys

import pygame

from utility import games, color, constants

if __name__ == '__main__':
    print "-menu.py-\n"
    print "You ran this module directly. Try main.py\n"
    raw_input("* Press the enter key to exit.")
    sys.exit(1)

# Initialize screen
games.init(screen_width = 640, screen_height = 480, fps = 50)

games.window.title = "PyArcade"

# [Note: Always manage games.window after the graphics screen
#        is initialized (not before).]

class Cursor(games.Sprite):
    """The cursor for the menu."""
    image = games.load_image("graphics/menu/cursor.png")
    
    def __init__(self, menu):
        """Initialize the cursor."""
        super(Cursor, self).__init__(image=Cursor.image,
                                         x=0,
                                         y=0)
        self.menu = menu

        self.current_option = constants.PONG

        self.draw()
    
    def __str__(self):
        return "cursor"

    def update(self):
        """Called at every frame."""
        self.check_input()
    
    def check_input(self):
        """Check for any player input while on the menu."""
        if games.keyboard.is_pressed(games.K_DOWN):
            if self.current_option < constants.EXIT:
                self.current_option += 1
                games.load_sound("sound/menu/cursor.wav").play()
                self.draw() # Update cursor's position
            return

        if games.keyboard.is_pressed(games.K_UP):
            if self.current_option == constants.SCORE:
                self.current_option = constants.PHONE
                games.load_sound("sound/menu/cursor_up.wav").play()
                self.draw()
                return
            if self.current_option > constants.PONG:
                self.current_option -= 1
                games.load_sound("sound/menu/cursor_up.wav").play()
                self.draw()
                return

        if games.keyboard.is_pressed(games.K_RIGHT):
            if self.current_option == constants.EXIT:
                self.current_option += 1
                games.load_sound("sound/menu/cursor.wav").play()
                self.draw()
            return

        if games.keyboard.is_pressed(games.K_LEFT):
            if self.current_option == constants.SCORE:
                self.current_option -= 1
                games.load_sound("sound/menu/cursor.wav").play()
                self.draw()

        if games.keyboard.is_pressed(games.K_RETURN):
            self.menu.option = self.current_option
            
            games.music.stop()
            
            if self.menu.option == constants.EXIT:
                games.load_sound("sound/menu/exit.wav").play()
            else:
                games.load_sound("sound/menu/enter.wav").play()

            # May also use pygame.time.delay() for better
            # accuracy (at the cost of consuming more
            # processor time).
            pygame.time.wait(1000)
            
            games.screen.quit() # main.py takes control

    def draw(self):
        """Draw the cursor at a new position."""
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

    
class Menu(object):
    """PyArcade's main interface."""
    def __init__(self):
        """Initialize PyArcade's menu."""
        self.title = games.Text(value="PyArcade 1.0",
                                size=80,
                                color=color.white,
                                x=games.screen.width/2,
                                y=50)

        # Set text for the available games.
        i = 0
        self.games = []
        for game in ("Pong", "Simon Says", "Save the Phone"):
            self.games.append(games.Text(value=game,
                                         size=40,
                                         color=color.white,
                                         x=games.screen.width/2,
                                         y=(games.screen.height/2-60) + i))
            i += 70
        
        self.exit = games.Text(value="Exit",
                               size=40,
                               color=color.white,
                               x=50,
                               y=games.screen.height - 30)
        
        self.score = games.Text(value="Scores",
                                 size=40,
                                 color=color.white,
                                 x=games.screen.width - 70,
                                 y=games.screen.height- 30)

        self._option = None # Option chosen by player

        self.game_started = False
    
    def start(self):
        """Start the menu."""
        games.screen.clear()

        # Show transitions
        if not self.game_started:
            self.transition()
            self.game_started = True

        games.screen.background = games.load_image("graphics/menu/background.png",
                                                   transparent=False)
        
        games.screen.add(self.title)
        
        for text in self.games:
            games.screen.add(text)
        
        games.screen.add(self.exit)
    
        games.screen.add(self.score)

        games.screen.add(Cursor(self))

        games.music.load("sound/menu/theme.mp3")
        
        games.music.play(-1)
        
        # start PyArcade 1.0
        games.screen.mainloop()

    def transition(self):
        """Show game's preliminary images."""
        image_paths = ("graphics/menu/transition1.png",
                       "graphics/menu/transition2.png")
        for path in image_paths:
            self._blit(path)

    def _blit(self, image_path=None, waiting_time=3000):
        """Show image for a given waiting time (in millisecs)."""
        if image_path == None:
            return

        screen = games.screen.display
        
        try:
            image = pygame.image.load(image_path).convert()
        except pygame.error:
            return
        
        screen.blit(image, (0,0))
        pygame.display.update()
        pygame.time.wait(waiting_time)

    def get_option(self):
        """Return the menu option chosen by the player."""
        return self._option

    def set_option(self, option):
        """
        Set an option chosen by the player.

        Keyword argument:
        option -- a valid int value from utility/constants.py
        
        """
        self._option = option

    option = property(get_option, set_option)

    def get_menu_options(self):
        """Return the options available on the menu."""
        options = self.games[:]
        options.append(self.exit)
        options.append(self.score)
        return options
    
    menu_options = property(get_menu_options)

    def get_game_started(self):
        """Return whether or not PyArcade has started."""
        return self.game_started

    def set_game_started(self, value):
        """
        Set the value for self.game_started.

        Keyword argument:
        value -- True or False
        
        """
        self.game_started = value

    game_start = property(get_game_started, set_game_started)
        

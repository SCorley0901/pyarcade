#/usr/bin/env python
#
# Simon Says
#
# A version of the Simon Says game, in which the player has to repeat an
# ever-growing, random sequence of colors and sounds.
#
# Programmer: Abner Coimbre

"""Simon Says -- A Pygame version."""

import sys

import random

from pygame import time

from utility import games, color

from score import check_score

if __name__ == '__main__':
    print("-simon.py-\n")
    print("You ran this module directly. Try main.py\n")
    input("* Press the enter key to exit.")
    sys.exit(1)

score = None

class Button(games.Sprite):
    """A Simon Says button."""
    label = ("yellow", "red", "blue", "green")
    
    # Map each button to a key
    keyboard = {label[0]: games.K_UP,
                label[1]: games.K_LEFT,
                label[2]: games.K_DOWN,
                label[3]: games.K_RIGHT}
    
    # Button images (to be accessed by the Simon() class).
    bttn_img = (games.load_image("graphics/simon/yellow_bttn.png"),
                games.load_image("graphics/simon/red_bttn.png"),
                games.load_image("graphics/simon/blue_bttn.png"),
                games.load_image("graphics/simon/green_bttn.png"))

    # Pressed button images (to be accessed by the Simon() class).
    bttn_pressed_img = (games.load_image("graphics/simon/yellow_bttn_pressed.png"),
                        games.load_image("graphics/simon/red_bttn_pressed.png"),
                        games.load_image("graphics/simon/blue_bttn_pressed.png"),
                        games.load_image("graphics/simon/green_bttn_pressed.png"))

    # Each button's unique sound (to be accessed by the Simon() class and
    # every Button instance).
    sound = (games.load_sound("sound/simon/tone1.wav"),
             games.load_sound("sound/simon/tone2.wav"),
             games.load_sound("sound/simon/tone3.wav"),
             games.load_sound("sound/simon/tone4.wav"))

    # Location of buttons highly dependent on background image.
    location = ((318,102), (138,240), (319,376), (504,240))
    
    # Keep track of how many button presses have been made.
    times_pressed = 0

    def __init__(self, label, bttn_img, bttn_pressed_img, sound, x, y):
        """Initialize a Simon Says button."""
        super(Button, self).__init__(image=bttn_img,
                                           x=x,
                                           y=y)
        
        # ------------------
        # Button attributes
        self.label = label
        self.bttn_img = bttn_img
        self.bttn_pressed_img = bttn_pressed_img
        self.sound = sound
        # ------------------
        
        # ----------------------------------------------------------------------
        # Allow button to remain 'pressed' for the time you specify.
        self.__timer = 0
        # Note: To be used with the light_up() and check_if_pressed() methods.
        # ----------------------------------------------------------------------
    
    def __str__(self):
        return "Simon button"
    
    def update(self):
        """Called at every frame."""
        self.check_if_pressed(Button.keyboard[self.label])

    def light_up(self):
        """Light up the button."""
        self.sound.play()
        self.set_image(self.bttn_pressed_img)
        self.__timer = 0.5 * games.screen.fps # Stay lit about 0.5 sec.

    def check_if_pressed(self, button):
        """
        Check if button is pressed and handle the event.

        Keyword argument:
        button - the Simon Says button to check
        
        """
        if self.__timer:
            self.__timer -= 1
            return
        
        # Return button to its original state if it was
        # already pressed.
        self.set_image(self.bttn_img)

        if Simon.player_turn:
            if games.keyboard.is_pressed(button):
                # ---------------------------------------------------------
                # End the game if player button presses are not
                # equal to the computer's.
                if self != Computer.sequence[Button.times_pressed]:
                    Simon.end()
                    return
                # ---------------------------------------------------------
                
                self.light_up() # press button
                
                Button.times_pressed += 1

                # ---------------------------------------------------------
                # It's now the computer's turn if all presses
                # made by player were correct.
                if Button.times_pressed == Computer.count:
                    Simon.score += 1
                    games.load_sound("sound/simon/round_end.wav").play()
                    Simon.yield_turn()
                    Button.times_pressed = 0
                # ---------------------------------------------------------


class Computer(games.Sprite):
    """The computer. Plays the button sequence the player must follow."""
    image = games.load_image("graphics/simon/computer.png")

    count = 0

    sequence = []

    seq_copy = []

    def __init__(self):
        super(Computer, self).__init__(image=Computer.image,
                                       x=0,
                                       y=0)

        self.__wait = 0
    
    def __str__(self):
        return "Simon Says computer"
    
    
    def update(self):
        """Called at every frame. """
        if Simon.computer_turn:
            self.play()

    def play(self):
        """Play an ever-growing sequence of simon buttons."""
        # Don't play next button until waiting time is over.
        if self.__wait:
            self.__wait -= 1
            return
        
        # Play all buttons from the sequence
        if Computer.seq_copy:
            Computer.seq_copy.pop(0).light_up()
            self.__wait = 1 * games.screen.fps
            return
        
        # ------------------------------------
        # If all buttons from the sequence were pressed, play
        # a new random button and append it to the sequence.
        next_bttn = random.choice(Simon.bttn_list)
        next_bttn.light_up()
        
        Computer.sequence.append(next_bttn)
        Computer.seq_copy = Computer.sequence[:]
        
        self.__wait = 1.5 * games.screen.fps
        
        Computer.increase_count()
        
        Simon.yield_turn()
        # ------------------------------------

    def increase_count():
        """Increase Computer.count by 1."""
        Computer.count += 1

    increase_count = staticmethod(increase_count)


class Simon(object):
    """A version of the game of Pong using Pygame."""
    player_turn = False
    
    computer_turn = True

    score = 0
    
    bttn_list = []
    
    def __init__(self):
        """Initialize important game values and settings."""
        games.screen.background = games.load_image("graphics/simon/background.png",
                                           transparent=False)
        
        Simon.reset()

        # Create buttons
        Simon.initialize()
        
        self.computer = Computer()

        # game-screen settings
        games.screen.event_grab = False # focus input on game screen (i.e. don't
                                        # allow the mouse to exit the graphics
                                        # window while playing). This happens if
                                        # it's set to True.
                                       
        games.mouse.is_visible = False # forbid mouse visibility
    
    def __str__(self):
        return "Simon Says"
    
    
    def start(self):
        """Start the game."""
        games.screen.clear()
        
        # Add buttons on screen
        for i in range(4):
            games.screen.add(Simon.bttn_list[i])
            
        # Add computer
        games.screen.add(self.computer)

        # Start Simon Says
        games.screen.mainloop()
    
    def initialize():
        """Initialize Button objects."""
        # -------------------------------------------------------------
        for i in range(4):
            Simon.bttn_list.append(Button(Button.label[i],
                                      Button.bttn_img[i],
                                      Button.bttn_pressed_img[i],
                                      Button.sound[i],
                                      Button.location[i][0],
                                      Button.location[i][1]))
        # -------------------------------------------------------------
    
    initialize = staticmethod(initialize)

    def reset():
        """Reset game values."""
        Button.times_pressed = 0
        Computer.count, Computer.sequence, Computer.seq_copy = 0, [], []
        Simon.score, Simon.bttn_list = 0, []
        Simon.player_turn = False
        Simon.computer_turn = True

    reset = staticmethod(reset)

    def yield_turn():
        """Control access to the buttons between player and computer."""
        if Simon.computer_turn:
            Simon.computer_turn = False
            Simon.player_turn = True
            return
        
        Simon.computer_turn = True
        Simon.player_turn = False

    yield_turn = staticmethod(yield_turn)

    def end():
        """End the game."""
        # Add score obtained to text file.
        score_file = open("utility/current_score.txt", "w")

        score_file.write(str(Simon.score))

        score_file.close()
        
        games.load_sound("sound/simon/game_over.wav").play()

        time.wait(2000)

        if check_score(value=Simon.score, txt_file_path="utility/simon_score.txt"):
            games.load_sound("sound/menu/high_score.wav").play()
            time.wait(1500)
        
        games.screen.quit()

    end = staticmethod(end)

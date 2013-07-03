#/usr/bin/env python
#
# Save the Phone
#
# Control a phone to steer it away from objects that fall from the sky.
#
# Programmer: Abner Coimbre

"""Save the Phone -- Original Pygame game."""

import sys

import random

import pygame

from utility import games, color

from score import check_score

if __name__ == '__main__':
    print "-phone.py-\n"
    print "You ran this module directly. Try main.py\n"
    raw_input("* Press the enter key to exit.")
    sys.exit(1)

L_BOUNDARY = 17 
    
R_BOUNDARY = 12 

class Phone(games.Sprite):
    """Phone sprite that the player controls. Only moves horizontally."""
    images = { "happy" : games.load_image("graphics/phone/phone_happy.png"),
               "scared" : games.load_image("graphics/phone/phone_scared.png") }
    
    def __init__(self, game):
        """Initialize Phone sprite object."""
        super(Phone, self).__init__(image=Phone.images["happy"],
                                    x=games.mouse.x,
                                    bottom=games.screen.height - 35)
        
        self.game = game

        self.can_play_sound = True
    
    def __str__(self):
        return "Phone"
    
    def update(self):
        """Called at every frame."""
        self.x = games.mouse.x

        self.game.update()

        # End game if any object has collided with phone.
        if self.overlapping_sprites:
            phone_explosion = Explosion(x=self.x, y=self.y)
            games.screen.add(phone_explosion)
            self.destroy()
            self.game.end()
            return
        
        # Stay within boundaries
        if self.left < L_BOUNDARY:
            self.left = L_BOUNDARY
            return
        if self.right > games.screen.width - R_BOUNDARY:
            self.right = games.screen.width - R_BOUNDARY
            return

    def alert(self, sprite):
        """
        Checks if the phone is in danger or not.

        Phone is either happy or scared depending on its status.

        Keyword argument:
        sprite -- the sprite on the screen to verify
        
        """
        # Game hasn't encountered a dangerous sprite.
        if sprite == None:
            return

        # In danger
        if sprite.right >= self.left and sprite.right <= self.right:
            self.image = Phone.images["scared"]
            if self.can_play_sound:
                games.load_sound("sound/phone/scared.wav").play()
                self.can_play_sound = False
            return

        # No longer in danger
        self.image = Phone.images["happy"]
        self.game.no_danger()
        self.can_play_sound = True


class FallingObject(games.Sprite):
    """A random object that falls from the sky."""
    # ----------------------
    # Load sprite images
    objects = open("graphics/phone/objects.txt", "r")

    images = []
    for image_path in objects:
        images.append(games.load_image(image_path.replace("\n", "")))
        
    objects.close()
    # ----------------------

    speed = 1 
    
    def __init__(self, game):
        """Initialize Falling object."""
        super(FallingObject, self).__init__(image=random.choice(FallingObject.images),
                                             x=random.randrange(580),
                                             y=70,
                                             dy=FallingObject.speed)
        games.load_sound("sound/phone/new_object.wav").play()
        
        self.game = game

    def __str__(self):
        return "Falling object"
        
    def update(self):
        """Called at every frame."""
        # Stay within boundaries
        if self.left < L_BOUNDARY:
            self.left = L_BOUNDARY
            return
        if self.right > games.screen.width - R_BOUNDARY:
            self.right = games.screen.width - R_BOUNDARY
            return
        
        # Destroy object and update score when it reaches the bottom.
        if self.bottom > games.screen.height - 35:
            self.destroy()
            self.game.update_score()
            return

    def increase_speed():
        """Increases the speed of the falling object."""
        FallingObject.speed += 0.5

    increase_speed = staticmethod(increase_speed)


class Explosion(games.Animation):
    """An animated explosion."""
    
    frames = ("graphics/phone/explosion1.bmp",
              "graphics/phone/explosion2.bmp",
              "graphics/phone/explosion3.bmp",
              "graphics/phone/explosion4.bmp",
              "graphics/phone/explosion5.bmp",
              "graphics/phone/explosion6.bmp",
              "graphics/phone/explosion7.bmp",
              "graphics/phone/explosion8.bmp",
              "graphics/phone/explosion9.bmp")

    def __init__(self, x, y):
        """Initialize explosion."""
        super(Explosion, self).__init__(images=Explosion.frames,
                                        x=x,
                                        y=y,
                                        repeat_interval=4,
                                        n_repeats=1,
                                        is_collideable=False)
        games.load_sound("sound/phone/explosion.wav").play()


class Game(object):
    """The game of 'Save the Phone' using Pygame."""
    time = 0
    
    timer = 25 * games.screen.fps
    
    def __init__(self):
        """Initialize important game values and settings."""
        games.screen.background = games.load_image("graphics/phone/background.png",
                                                   transparent=False)
        
        self.mobile = Phone(self)
        
        self.initial_msg = games.Message(value="Random objects are falling!",
                                         size=30,
                                         color=color.white,
                                         right=games.screen.width - 10,
                                         bottom=games.screen.height - 10,
                                         lifetime=3*games.screen.fps)
        
        self.score = 0 # [Note: score = # of objects avoided by phone]
        
        games.music.load("sound/phone/theme.mp3")

        self._count = 3 * games.screen.fps

        self.object_above_phone = None
    
        # game-screen settings
        games.screen.event_grab = True # Focus input on game screen (e.g. don't
                                       # allow the mouse to exit the graphics
                                       # window while playing).
                                       
        games.mouse.is_visible = False
    
    def __str__(self):
        return "Save the Phone"
    
    def start(self):
        """Start the game."""
        games.screen.clear()
        
        games.screen.add(self.mobile)
        
        games.screen.add(self.initial_msg)
        
        games.music.play(-1)
        
        # start 'Save the Phone'
        games.screen.mainloop()

    def update(self):
        """Called at every frame."""
        Game.time += 1

        # Update timer
        Game.timer -= 1
        self.check_timer()

        # Alert phone as to whether or not it's in danger.
        self.mobile.alert(self.object_above_phone)

        # Check if a falling object is above the phone.
        for sprite in games.screen.all_objects:
            if sprite not in (self.mobile, self.initial_msg):
                if sprite.right >= self.mobile.left and sprite.right <= self.mobile.right:
                    if self.object_above_phone == None:
                        self.object_above_phone = sprite

        # See if it's time to add a new random object.
        if self._count > 0:
            self._count -= 1
            return
        falling_object = FallingObject(self)
        games.screen.add(falling_object) # add object
        
        # Set so buffer will be about 30% of falling_object's height (Formula by Michael Dawson).
        self._count = int(falling_object.height * 1.3 / FallingObject.speed) + 1

    def check_timer(self):
        """Checks if it's time to increase game difficulty."""
        if Game.timer <= 0:
            FallingObject.increase_speed()
            Game.timer = 15 * games.screen.fps
    
    def update_score(self, score=1):
        """Increase game score when invoked."""
        self.score += score

    def no_danger(self, no_danger = True):
        if no_danger:
            self.object_above_phone = None
    
    def end(self):
        """End the game."""
        # Add score obtained to text file.
        score_file = open("utility/current_score.txt", "w")

        score_file.write(str(self.score))

        score_file.close()
        
        # Reset falling object's speed
        FallingObject.speed = 1
        
        # Remove falling objects
        for sprite in games.screen.all_objects:
            if str(sprite) == "Falling object":
                sprite.destroy()

        games.music.stop()
        
        # Play game over sound
        games.load_sound("sound/phone/game_over.wav").play()

        # Set the Game Over message. Note that self.check_if_high_score()
        # will be called after the message dissappears.
        message = games.Message(value="Game Over",
                                size=30,
                                color=color.white,
                                right=games.screen.width - 10,
                                bottom=games.screen.height - 10,
                                lifetime=6.5 * games.screen.fps,
                                after_death=self.check_if_high_score)
        # Game Over
        games.screen.add(message)

    def check_if_high_score(self):
        """Check if player made it to the high scores."""
        if check_score(value=self.score, txt_file_path="utility/phone_score.txt"):
            games.load_sound("sound/menu/high_score.wav").play()
            games.screen.add(games.Message(value="High Score",
                                size=30,
                                color=color.white,
                                x=games.screen.width - 60,
                                y=games.screen.height - 20,
                                lifetime=5.5 * games.screen.fps,
                                after_death = games.screen.quit))
            return
        games.screen.quit()

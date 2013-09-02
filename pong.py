#/usr/bin/env python
#
# Pong
#
# A version of the famous Pong game. A player must bounce off a ball.
# If he or she misses the ball, game over.
#
# Programmer: Abner Coimbre

"""Pong -- A Pygame version"""

import sys

import math

import random

from pygame import time

from utility import games, color

from score import check_score

if __name__ == '__main__':
    print("-pong.py-\n")
    print("You ran this module directly. Try main.py\n")
    input("* Press the enter key to exit.")
    sys.exit(1)

class Paddle(games.Sprite):
    """Player's paddle that moves up and down with the mouse."""
    image = games.load_image("graphics/pong/paddle.png")
    
    x_coord = games.screen.width/6

    def __init__(self):
        super(Paddle, self).__init__(image=Paddle.image,
                                     x=Paddle.x_coord, # fixed x
                                     y=games.mouse.y)

    def __str__(self):
        return "Paddle"

    def update(self):
        """Called at every frame."""
        self.y = games.mouse.y

        # Maintain paddle within boundaries
        if self.top < Pong.top_wall_y:
            self.top = Pong.top_wall_y + 4
            return
        if self.bottom > Pong.bottom_wall_y:
            self.bottom = Pong.bottom_wall_y - 4


class CPUPaddle(games.Sprite):
    """Computer's paddle. Can track the ball."""
    image = games.load_image("graphics/pong/paddle.png")
    
    x_coord = 7 * games.screen.width / 8
    
    def __init__(self):
        super(CPUPaddle, self).__init__(image=CPUPaddle.image,
                                           x=CPUPaddle.x_coord, # fixed x
                                           y=games.screen.height/2,
                                           dx=0,
                                           dy=0)
    
    def __str__(self):
        return "CPU paddle"
    
    def update(self):
        """Called at every frame."""
        if Ball.current_dx > 0: # dx = x-velocity
            # Stay within boundaries
            if self.top < Pong.top_wall_y:
                self.top = Pong.top_wall_y + 4
                return
            if self.bottom > Pong.bottom_wall_y:
                self.bottom = Pong.bottom_wall_y - 4
                return
            # ------------
            
            # Track ball
            if Ball.y_coord > self.y:
                self.dy = 0.85 * Ball.current_dx
                return
            if Ball.y_coord < self.y:
                self.dy = -0.85 * Ball.current_dx
                return
            # ------------
       
        self.dy = 0


class Ball(games.Sprite):
    """Bouncing Ball object."""
    image = games.load_image("graphics/pong/ball.png")

    sound = games.load_sound("sound/pong/bounce.wav")

    time_limit = 15 * games.screen.fps
    
    x_coord = games.screen.width/2
    
    y_coord = games.screen.height/2
    
    top_coord = 0
    
    bottom_coord = 0
    
    current_dx = 0
    
    def __init__(self, game):
        """Initialize the ball."""
        super(Ball, self).__init__(image=Ball.image,
                                   x=games.screen.width/2,
                                   y=games.screen.height/2,
                                   dx=random.choice((1.5, -1.5)),
                                   dy=random.choice((1.5, -1.5)))
        self.game = game # Maintain contact with the game object itself (e.g. useful
                         # when notifying the game that the score should be updated
                         # or that the game must end).

    def __str__(self):
        return "Ball"

    def update(self):
        """Called at every frame."""
        Ball.update_coord(self.x, self.y)
        
        Ball.update_dx(self.dx)
        
        # End the game once the ball reaches left screen boundary.
        if self.left < 0:
            self.destroy()
            self.game.end()
            
        # Advance to next level if the cpu paddle misses the ball.
        if self.left > games.screen.width:
            self.game.advance()

        Ball.time_limit -= 1
        self.check_time()
        
        # Bounce when needed
        self.bounce()

    def check_time(self):
        """Increase speed of Ball object based on time passed."""
        if Ball.time_limit < 0:
            self.increase_dx()
            self.increase_dy()
            Ball.time_limit = 25 * games.screen.fps # Reset time limit
    
    def update_coord(x, y):
        """
        Update the ball's coordinates.

        Set the ball instance's x and y coordinates
        values to Ball.x_coord and Ball.y_coord. Useful
        for other objects to access these values without
        having a reference to the instance.

        Keyword arguments:
        Ball.x_coord -- x-coordinate of the ball
        Ball.y_coord -- y-coordinate of the ball

        """
        Ball.x_coord = x
        Ball.y_coord = y
    
    update_coord = staticmethod(update_coord)
    
    def update_dx(dx):
        """
        Update the ball's x-velocity component.

        Set the ball instance's dx value to
        Ball.current_dx. Useful for other objects
        to access this value without having a reference
        to the instance.

        Keyword argument:
        Ball.current_dx -- x-velocity of the ball

        """
        Ball.current_dx = dx
        
    update_dx = staticmethod(update_dx)

    def increase_dx(self, dx=0.3):
        """
        Increase the ball's x-velocity.

        Keyword argument:
        dx -- new value for dx. Default is 0.3

        """
        if self.dx < 0:
            self.dx -= dx
            return
        self.dx += dx

    def increase_dy(self, dy=0.3):
        """
        Increase the ball's y-velocity.

        Keyword argument:
        dy -- new value for dx. Default is 0.3

        """
        if self.dy < 0:
            self.dy -= dy
            return
        self.dy += dy
    
    def bounce(self):
        """Bounce off the walls or paddles."""
        # Bounce off bottom and top walls
        if self.bottom > Pong.bottom_wall_y or self.top < Pong.top_wall_y:
            Ball.sound.play()
            self.dy = -self.dy
            return

        # Bounce off paddles
        if self.overlapping_sprites:
            # change ball's x-component when hitting player's paddle
            if self.x < games.screen.width/2 and self.dx < 0:
                if self.left > Paddle.x_coord: # alter dx only if the ball isn't at the tip of the paddle
                    Ball.sound.play()
                    self.dx = -self.dx * math.cos(self.angle) # [Note: Should use a better formula in the future.
                                                              #  Also add one that accounts for the ball's y-component].
                    self.game.update_score() # update score since the ball
                                             # hit the player paddle
                return
            # change ball's x-component when hitting enemy's paddle
            if self.x > games.screen.width/2 and self.dx > 0:
                if self.right < CPUPaddle.x_coord: # alter dx only if the ball isn't at the tip of the paddle
                    Ball.sound.play()
                    self.dx = -self.dx * math.cos(self.angle) # [Note: See previous note.]


class Pong(object):
    """A version of the game of Pong using Pygame."""
    bottom_wall_y = 7 * games.screen.height / 8
    
    top_wall_y = games.screen.width/12
    
    # ^ Note that by allowing access to the y-coordinates of the top
    # and bottom walls, the ball and paddles will be able to know
    # when they reach their boundary.
    
    def __init__(self):
        """Initialize important game values and settings."""
        games.screen.background = games.load_image("graphics/pong/background.png",
                                                   transparent = False)
        
        self.score = games.Text(value=0,
                                size=35,
                                color=color.white,
                                top=5,
                                right=games.screen.width - 10)
        
        self.bottom_wall = games.Sprite(image=games.load_image("graphics/pong/wall.png"),
                                        x=games.screen.width/2,
                                        y=Pong.bottom_wall_y,
                                        is_collideable=False)
        
        self.top_wall = games.Sprite(image=games.load_image("graphics/pong/wall.png"),
                                  x=games.screen.width/2,
                                  y=Pong.top_wall_y,
                                  is_collideable=False)
        
        # Net
        self.net = []
        for i in range(23):
            self.net.append(games.Sprite(image=games.load_image("graphics/pong/net.png"),
                                         x=games.screen.width/2,
                                         y=Pong.bottom_wall_y - (16*(i+1)),
                                         is_collideable=False))
        
        self.logo = games.Sprite(image=games.load_image("graphics/pong/logo.png"),
                                 x=40,
                                 y=games.screen.height - (Pong.top_wall_y-27),
                                 is_collideable=False)

        self.initial_msg = games.Message(value="Control paddle with mouse",
                                         size = 30,
                                         color=color.white,
                                         left=self.logo.right + 10,
                                         y=self.logo.y,
                                         lifetime=5 * games.screen.fps)
        
        self.game_objects = (Paddle(), CPUPaddle(), Ball(self),
                             self.top_wall, self.bottom_wall,
                             self.score)
        
        # game-screen settings
        games.screen.event_grab = True # focus input on game screen (i.e. don't
                                       # allow the mouse to exit the graphics
                                       # window while playing)
                                       
        games.mouse.is_visible = False # forbid mouse visibility
        
        games.music.load("sound/pong/theme.wav")

    def __str__(self):
        return "Pong"
    
    def start(self):
        """Start the game."""
        games.screen.clear()
        
        for square in self.net:
            games.screen.add(square)
   
        games.screen.add(self.logo)

        games.screen.add(self.initial_msg)
        
        for object in self.game_objects:
            games.screen.add(object)
            
        games.music.play(-1)
            
        # Start Pong
        games.screen.mainloop()
    
    def update_score(self, score=10):
        """
        Increase game score when invoked.

        Keyword argument:
        score -- new value for score. Default is 10

        """
        self.score.value += score
        self.score.right = games.screen.width - 10
    
    def advance(self):
        """Advance to 'next level'."""
        self.update_score(score=100)
        
        games.load_sound("sound/pong/advance.wav").play()
       
        time.wait(2000)
        
        # Place ball at center and reverse its dx and dy components.
        ball_settings = (games.screen.width/2, games.screen.height/2,
                         -self.game_objects[2].dx, -self.game_objects[2].dy)
        
        # Relocate ball adjusted to its new settings.
        self.game_objects[2].x, self.game_objects[2].y, \
        self.game_objects[2].dx, self.game_objects[2].dy = ball_settings

    def end(self):
        """End the game."""
        # Add score obtained to text file.
        score_file = open("utility/current_score.txt", "w")

        score_file.write(str(self.score.value))

        score_file.close()
        
        # Remove net as to not obstruct the game over message.
        for square in self.net:
            square.destroy()
        
        games.load_sound("sound/pong/game_over.wav").play()
        
        # Set the message. Note that games.screen.quit()
        # will be called after the message dissappears.
        message = games.Message(value="Game Over",
                                size=40,
                                color=color.white,
                                x=games.screen.width/2,
                                y=games.screen.height/2,
                                lifetime=5 * games.screen.fps,
                                after_death=self.check_if_high_score)
        # Game Over
        games.screen.add(message)

    def check_if_high_score(self):
        """Check if player made it to the high scores."""
        if check_score(value=self.score.value, txt_file_path="utility/pong_score.txt"):
            games.load_sound("sound/menu/high_score.wav").play()
            games.screen.add(games.Message(value="High Score",
                                           size=40,
                                           color=color.white,
                                           x=games.screen.width/2,
                                           y=games.screen.height/2,
                                           lifetime=5 * games.screen.fps,
                                           after_death=games.screen.quit))
            return
        games.screen.quit()

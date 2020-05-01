import math
import pygame
import random
from colors import *
from pygame.locals import *


class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen.

    Args:
        speed (int or float): The initial speed of the ball.
    
    Attributes:
        image (Surface): The Surface object that represents the ball.
        rect (Rect): The position and size of the ball.
        area (Rect): The area that the ball must stay inside.
        initial_speed (int or float): The initial speed of the ball.
        speed (int or float): The current speed of the ball.
        angle (float): The angle at which the ball is moving, in radians.
    """

    WIDTH = 16
    HEIGHT = 16

    def __init__(self, speed, maxspeed):
        pygame.sprite.Sprite.__init__(self)
        # self.image, self.rect = load_image('ball.png', -1)
        self.image = pygame.Surface((Ball.WIDTH, Ball.HEIGHT))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, WHITE, self.rect.center, Ball.WIDTH / 2)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = self.area.center
        self.initial_speed = speed
        self.maxspeed = maxspeed
        self.speed = speed
        self.angle = self._random_angle()

    def _random_angle(self):
        """Return a random angle (in radians) between 0.15π and 0.3π

        Returns:
            float: The random angle.
        """
        return math.pi * random.uniform(0.15, 0.3)

    def reinit(self):
        """Resets the ball to center of screen, initial speed, moving at a random angle.
        
        This method can be used to reset the ball after every goal
        or at the beginning of a new game.
        """
        self.angle = self._random_angle()
        self.rect.center = self.area.center
        self.speed = self.initial_speed

    def update(self):
        """Move the ball based on its current angle and speed.
        
        Changes angle of the ball based on what part of the paddle it
        collides with. This method also resets the ball if it collides
        with the left or right side of the screen
        """
        newpos = self.calcnewpos(self.rect, self.speed, self.angle)
        self.rect = newpos

        if not self.area.contains(newpos):
            if newpos.top <= 0 or newpos.bottom >= self.area.height:
                self.angle = -self.angle
            if newpos.left <= 0:
                self.game.state.player1_scored()
                self.reinit()
            if newpos.right >= self.area.width:
                self.game.state.player2_scored()
                self.reinit()
        else:
            for paddle in pygame.sprite.spritecollide(
                self, self.game.spritegroups["paddlesprites"], False
            ):
                if self.speed < self.maxspeed:
                    self.speed += 1
                collision_location = (self.rect.centery - paddle.rect.top) / (
                    paddle.rect.bottom - paddle.rect.top
                )
                if paddle.side == "left":
                    self.angle = (collision_location * -0.5 + 0.25) * math.pi
                if paddle.side == "right":
                    self.angle = (collision_location * 0.5 + 0.75) * math.pi

    def calcnewpos(self, rect, speed, angle):
        """Calculates the new position of the rect based on speed and angle."""
        dx, dy = speed * math.cos(angle), -(speed * math.sin(angle))
        return rect.move(dx, dy)


class Paddle(pygame.sprite.Sprite):
    """A user controlled paddle that moves up and down to hit the ball
    
    Args:
        side (str): "left" or "right"

    Attributes:
        image (Surface): The Surface object that represents the paddle.
        rect (Rect): The position and size of the paddle.
        area (Rect): The area that the paddle must stay inside.
        side (str): "left" or "right"
        speed (int or float): Speed of the paddle.
        state (str): "still", "moveup" or "movedown"
        movepos([int or float, int or float]): How much to move in each direction
            each frame
    """

    WIDTH = 16
    HEIGHT = 100

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((Paddle.WIDTH, Paddle.HEIGHT))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, WHITE, self.rect)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 5
        self.state = "still"
        self.reinit()

    def reinit(self):
        """Reset paddles to initial state."""
        self.state = "still"
        self.movepos = [0, 0]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        if self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        """Move paddles based on current state and speed."""
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos

    def moveup(self):
        """Make paddle start moving up."""
        self.movepos[1] = -self.speed
        self.state = "moveup"

    def movedown(self):
        """Make paddle start moving down."""
        self.movepos[1] = self.speed
        self.state = "movedown"

    def stop(self):
        """Stop paddle movement."""
        self.movepos = [0, 0]
        self.state = "still"


class Player1Score(pygame.sprite.Sprite):
    """A sprite that shows player 1's score
    
    Attributes:
        font (Font): The font family and size to display score with
        image (Surface): The Surface object that represents the score sprite.
        rect (Rect): The position and size of the score sprite.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 48)
        self.image = self.font.render(str(0), 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = pygame.display.get_surface().get_rect().centerx + 10

    def update(self):
        """Update score text based on current game state."""
        self.image = self.font.render(str(self.game.state.player1_score), 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = pygame.display.get_surface().get_rect().centerx + 10


class Player2Score(pygame.sprite.Sprite):
    """A sprite that shows player 2's score
        
    Attributes:
        font (Font): The font family and size to display score with
        image (Surface): The Surface object that represents the score sprite.
        rect (Rect): The position and size of the score sprite.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 48)
        self.image = self.font.render(str(0), 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.right = pygame.display.get_surface().get_rect().centerx - 10

    def update(self):
        """Update score text based on current game state."""
        self.image = self.font.render(str(self.game.state.player2_score), 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.right = pygame.display.get_surface().get_rect().centerx - 10

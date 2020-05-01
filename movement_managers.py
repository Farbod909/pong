import math
import pygame
import random
from abc import ABC, abstractmethod
from pygame.locals import *


class PaddleMovementManager(ABC):
    """Abstract Base Class of all PaddleMovement types."""

    def __init__(self, paddle):
        self.paddle = paddle
        self.moveup = False
        self.movedown = False

    @abstractmethod
    def update(self):
        pass

    def move(self):
        """Sets movemement direction of paddle.
        
        After is determined what direction the paddle should move,
        this method calls the paddle sprite's movement methods to
        set the direction of movement.
        """
        if self.moveup and self.movedown:
            self.paddle.stop()
        elif self.moveup:
            self.paddle.moveup()
        elif self.movedown:
            self.paddle.movedown()
        else:
            self.paddle.stop()


class PaddleMovementManager_Manual(PaddleMovementManager):
    """Controls paddle movement based on user input.
    
    Args:
        paddle (Sprite): the paddle being controlled.
        moveup_key (pygame.key): The key that should move the paddle up
        movedown_key (pygame.key): The key that should move the paddle down    
    """

    def __init__(self, paddle, moveup_key, movedown_key):
        super().__init__(paddle)
        self.moveup_key = moveup_key
        self.movedown_key = movedown_key

    def update(self):
        """Determines and sets the movement direction of a paddle based on event queue."""
        for event in self.paddle.game.events:
            if event.type == KEYDOWN:
                if event.key == self.moveup_key:
                    self.moveup = True
                if event.key == self.movedown_key:
                    self.movedown = True
            elif event.type == KEYUP:
                if event.key == self.moveup_key:
                    self.moveup = False
                if event.key == self.movedown_key:
                    self.movedown = False

        self.move()


class PaddleMovementManager_AI(PaddleMovementManager):
    """Controls paddle movement based on heuristics
    
    Args:
        paddle (Sprite): the paddle being controlled.
        type (str): "basic" or "advanced"

    Attributes:
        target_y (float): The y value that the paddle has determined
            it should move to, based on heuristics.
        offset (float): An offset that is randomized with respect to
            target_y in order to add some variance to the angle at which
            the ball is launched.
    """

    def __init__(self, paddle, type):
        super().__init__(paddle)
        self.target_y = None
        self.offset = 0

        if type == "basic":
            self.set_target_y = self.basic_target_y
        elif type == "advanced":
            self.set_target_y = self.advanced_target_y

    def basic_target_y(self):
        """Paddle follows the ball."""
        ball = self.paddle.game.spritegroups["ballsprite"].sprite
        self.target_y = ball.rect.centery

    def advanced_target_y(self):
        """Determine the final location of the ball depending on angle and distance from paddle.
        
        This method also adds a randomized offset to the target_y (limited to
        the height of the paddle) in order to add some variance to the angle at
        which it launches the ball (otherwise it would always launch ball at an
        angle of 0 or π).
        """
        screen_height = pygame.display.get_surface().get_height()
        ball = self.paddle.game.spritegroups["ballsprite"].sprite

        angle = ball.angle
        if angle < 0:
            angle = 2 * math.pi + ball.angle

        ball_direction = (
            "left" if angle > 0.5 * math.pi and angle < 1.5 * math.pi else "right"
        )
        if ball_direction == "left":
            if self.paddle.side == "left":
                angle = math.pi - angle
                dx = ball.rect.centerx - self.paddle.rect.right
                dy = dx * math.tan(angle)
                self.target_y = math.pow(
                    -1, abs(ball.rect.centery - dy) // screen_height
                ) * (abs(ball.rect.centery - dy) % screen_height)
                if self.target_y < 0:
                    self.target_y = screen_height + self.target_y
                if self.offset == 0:
                    self.offset = random.uniform(
                        -self.paddle.rect.height / 2, self.paddle.rect.height / 2
                    )
                self.target_y = self.target_y + self.offset
            else:
                self.target_y = screen_height / 2
                self.offset = 0
        else:
            if self.paddle.side == "right":
                dx = self.paddle.rect.left - ball.rect.centerx
                dy = dx * math.tan(angle)
                self.target_y = math.pow(
                    -1, abs(ball.rect.centery - dy) // screen_height
                ) * (abs(ball.rect.centery - dy) % screen_height)
                if self.target_y < 0:
                    self.target_y = screen_height + self.target_y
                if self.offset == 0:
                    self.offset = random.uniform(
                        -self.paddle.rect.height / 2, self.paddle.rect.height / 2
                    )
            else:
                self.target_y = screen_height / 2
                self.offset = 0

    def update(self):
        """Sets the movement direction of a paddle based on target_y."""
        self.set_target_y()

        if self.target_y > self.paddle.rect.centery:
            self.moveup = False
            self.movedown = True
        if self.target_y < self.paddle.rect.centery:
            self.moveup = True
            self.movedown = False

        self.move()

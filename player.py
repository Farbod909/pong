from abc import ABC, abstractmethod
from pygame.locals import *

class PaddleMovement(ABC):
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


class PaddleMovement_Manual(PaddleMovement):
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

    def update(self, events):
        """Determines and sets the movement direction of a paddle based on event queue.
        
        Args:
            events (List[pygame.event]): The event queue in a given frame
        """
        for event in events:
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


class PaddleMovement_AI(PaddleMovement):
    """Controls paddle movement based on heuristics"""
    def __init__(self, paddle):
        super().__init__(paddle)

    def update(self, ball):
        """Determines and sets the movement direction of a paddle based on ball location.
        
        Args:
            ball (Sprite)
        """
        if ball.rect.centery > self.paddle.rect.centery:
            self.moveup = False
            self.movedown = True
        if ball.rect.centery < self.paddle.rect.centery:
            self.moveup = True
            self.movedown = False
        
        self.move()
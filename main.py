"""
Farbod's Pong Game
A simple pong game made for me to better understand Pygame.

Released under the GNU General Public License.
"""

VERSION = "0.1.0"

import pygame
import sys
from game import Game
from colors import *
from objects import *
from movement_managers import *
from pygame.locals import *


SIZE = WIDTH, HEIGHT = 640, 480

def main():
    # Setup    
    game = Game(SIZE, DARKGRAY)

    # Initialize sprites
    paddle1 = Paddle("right")
    paddle2 = Paddle("left")
    player1_score = Player1Score()
    player2_score = Player2Score()
    ball = Ball(speed=5, maxspeed=15)
    
    # Add sprites to groups
    paddlesprites = pygame.sprite.RenderPlain((paddle1, paddle2))
    scoresprites = pygame.sprite.RenderPlain((player1_score, player2_score))
    ballsprite = pygame.sprite.GroupSingle(ball)

    # Add groups (and the other groups they depend on) to the game
    game.add_sprites({
        'paddlesprites': paddlesprites,
        'scoresprites': scoresprites,
        'ballsprite': ballsprite
    })

    # Initialize objects to control paddle movement (manually or by AI)
    player1_movement_manager = PaddleMovementManager_Manual(paddle1, K_UP, K_DOWN)
    player2_movement_manager = PaddleMovementManager_AI(paddle2, "advanced")

    # Add movement manager objects to game
    game.add_movement_managers(
        player1_movement_manager,
        player2_movement_manager
    )

    game.start()


if __name__ == "__main__":
    main()
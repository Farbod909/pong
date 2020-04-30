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
from movement import PaddleMovement_Manual, PaddleMovement_AI
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
        paddlesprites: None,
        scoresprites: None,
        ballsprite: [paddlesprites]
    })

    # Initialize objects to control paddle movement (manually or by AI)
    player1_movement = PaddleMovement_Manual(paddle1, K_UP, K_DOWN)
    player2_movement = PaddleMovement_AI(paddle2, "advanced")

    game.initial_frame()

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        # Store events in a list to be passed to player-controlled sprites
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            else:
                events.append(event)

        # Update paddle movement direction based on keyboard events (manual)
        # or ball location (AI)
        player1_movement.update(events)
        player2_movement.update(ball)

        # Clear sprites from screen and re-render them based on new values
        game.update_frame()


if __name__ == "__main__":
    main()
import pygame
import sys
from colors import *
from pygame.locals import *


class Game:
    """A class that encapsulates all game data and generic functions.

    Args:
        size ((int, int))
        color: (Color or (int, int, int))
    
    Attributes:
        state (State): The current state of the game.
        screen (Surface): The display surface.
        background (Surface): The background surface.
        spritegroups: A dictionary of all sprite groups in the game.
            The key is the name of the group and the value is a reference
            to the Group.
        events (List[event]): pygame events from the current frame.
    """

    class State:
        """A representation of the state of the game.
        
        Attributes:
            player1_score (int)
            player2_score (int)
        """

        def __init__(self):
            self.player1_score = 0
            self.player2_score = 0

        def player1_scored(self):
            self.player1_score += 1

        def player2_scored(self):
            self.player2_score += 1

        def reset_scores(self):
            self.player1_score = 0
            self.player2_score = 0

    def __init__(self, size, color):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong")
        self.state = Game.State()
        self.background = self.make_background(color)
        self.spritegroups = {}
        self.movement_managers = []

    def make_background(self, color):
        """Create a background surface.
        
        Args:
            color (Color or (int, int, int)): Color of the field.

        Return:
            Surface: The background.
        """
        screen = pygame.display.get_surface()
        background = pygame.Surface((screen.get_width(), screen.get_height()))
        background = background.convert()
        background.fill(color)
        pygame.draw.line(
            background,
            (250, 250, 250),
            background.get_rect().midtop,
            background.get_rect().midbottom,
        )
        return background

    def add_sprite(self, sprite):
        """Add a sprite to the game.
        
        This adds a `game` property to each sprite in the game
        so the sprite can access the game's functions and properties
        such as the state.

        Args:
            sprite (Sprite): The sprite to be added to the game.
        
        Returns:
            Sprite: the same sprite, slightly modified.
        """
        sprite.game = self
        return sprite

    def add_sprites(self, *sprites):
        """Adds several sprites to the game.
        
        This adds a `game` property to each sprite in the game
        so the sprite can access the game's functions and properties
        such as the state.
        """
        for sprite in sprites:
            self.add_sprite(sprite)

    def add_spritegroups(self, spritegroups_dict):
        """Adds references to Sprites and Game so they can access eachother.

        Creates a reference to this Game instance in all sprites and
        creates a reference to all spritegroups in this Game instance.

        Args:
            spritegroups_dict (Dict[str, Group]): A dictionary of the
                spritegroups in the game where the key is the name of each
                spritegroup and the value is a reference to the Group.
        """
        self.spritegroups.update(spritegroups_dict)
        for spritegroup in self.spritegroups.values():
            for sprite in spritegroup.sprites():
                self.add_sprite(sprite)

    def add_movement_managers(self, movement_managers):
        """Adds reference to movement managers in Game.
        
        Args:
            movement_managers (List[PaddleMovementManager])
        """
        self.movement_managers.extend(movement_managers)

    def update_movement_managers(self):
        """Update all movement managers."""
        for movement_manager in self.movement_managers:
            movement_manager.update()

    def initial_frame(self):
        """Blit initial frame onto display surface."""
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def update_frame(self):
        """Clear sprites from screen and re-render them based on new values
        
        Blits the background onto all sprites in the game and then
        blits the sprites with new locations onto the screen again.
        """
        for spritegroup in self.spritegroups.values():
            for sprite in spritegroup.sprites():
                self.screen.blit(self.background, sprite.rect, sprite.rect)
            spritegroup.update()
            spritegroup.draw(self.screen)
        pygame.display.update()

    def startloop(self):
        self.initial_frame()
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # Store events in a list to be available to player-controlled sprites
            self.events = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                else:
                    self.events.append(event)

            # Update paddle movement direction based on keyboard events (manual)
            # or the state of other game sprites (AI)
            self.update_movement_managers()

            # Clear sprites from screen and re-render them based on new values
            self.update_frame()

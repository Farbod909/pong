import pygame
from colors import *
from typing import Dict, List, Optional


class Game:
    """A class that encapsulates all game data and generic functions.
    
    Attributes:
        state (State): The current state of the game.
        screen (Surface): The display surface.
        background (Surface): The background surface.
        spritegroups_with_dependencies: A dictionary of all sprite groups
            in the game mapped to a list of all other spritegroups that each
            one is dependent on (or None if that spritegroup has no dependencies).
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
        self.state = self.State()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong")
        self.background = self.make_background(color)
        self.spritegroups_with_dependencies: Dict[pygame.sprite.Group, Optional[List[pygame.sprite.Group]]] = {}

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
            background.get_rect().midbottom)
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
    
    def add_sprites(self, spritegroups_with_dependencies: Dict[pygame.sprite.Group, Optional[List[pygame.sprite.Group]]]):
        """Associates sprite with this Game instance.

        Creates a reference to this Game instance in all sprites and
        creates a reference to all spritegroups and their dependencies
        in this Game instance.
        """
        for spritegroup, dependencies in spritegroups_with_dependencies.items():
            self.spritegroups_with_dependencies[spritegroup] = dependencies
            for sprite in spritegroup.sprites():
                self.add_sprite(sprite)

    def initial_frame(self):
        """Blit initial frame onto display surface."""
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def update_frame(self):
        """Clear sprites from screen and re-render them based on new values
        
        Blits the background onto all sprites in the game and then
        blits the sprites with new locations onto the screen again.
        """
        for spritegroup, dependencies in self.spritegroups_with_dependencies.items():
            for sprite in spritegroup.sprites():
                self.screen.blit(self.background, sprite.rect, sprite.rect)
            if dependencies is not None:
                spritegroup.update(*dependencies)
            else:
                spritegroup.update()
            spritegroup.draw(self.screen)
        pygame.display.update()


import pygame
from supports import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size: int, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, shift: int) -> None:
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size: int, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Tree(StaticTile):
    def __init__(self, size: int, x, y, path, shift_y):
        super().__init__(size, x, y, pygame.image.load(path))
        # self.image = pygame.image.load(path).convert_alpha()
        new_y = y + shift_y
        self.rect = self.image.get_rect(bottomleft = (x, new_y))

class Stone(StaticTile):
    def __init__(self, size, x, y, path: str, shift_x, shift_y):
        super().__init__(size, x, y, pygame.image.load(path))
        new_x = x + shift_x
        new_y = y + shift_y
        self.rect = self.image.get_rect(bottomleft = (new_x, new_y))

class Bush(StaticTile):
    def __init__(self, size: int, x, y, path, shift_x, shift_y):
        super().__init__(size, x, y, pygame.image.load(path))
        new_x = x + shift_x
        new_y = y + shift_y
        self.rect = self.image.get_rect(bottomright = (new_x, new_y))

class Ladder(StaticTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, pygame.image.load(path))


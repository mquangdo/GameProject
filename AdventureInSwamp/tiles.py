import pygame
from supports import import_folder, import_cut_graphics
import random
import numpy as np

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

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


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


class Ridge(StaticTile):
    def __init__(self, size, x, y, path: str, shift_y):
        super().__init__(size, x, y, pygame.image.load(path))
        new_y = y + shift_y
        self.rect = self.image.get_rect(bottomleft=(x, new_y))


class Ladder(StaticTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, pygame.image.load(path))

class Spike(StaticTile):
    def __init__(self, size, x, y, path: str, shift_y):
        super().__init__(size, x, y, pygame.image.load(path))
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))

class Portal(AnimatedTile):

    def __init__(self, size, x, y, path, shift_y):
        super().__init__(size, x, y, path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))

class Flag(AnimatedTile):
    def __init__(self, size, x, y, path, shift_y):
        super().__init__(size, x, y, path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom=(x, new_y))

class Chest(AnimatedTile):
    def __init__(self, size, x, y, path, shift_y):
        super().__init__(size, x, y, path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom=(x, new_y))

class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path: str):
        super().__init__(size, x, y,path)
        self.speed = random.randint(2, 4)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift_x):
        self.rect.x += shift_x
        self.animate()
        self.reverse_image()
        self.move()

class Trap(AnimatedTile):
    def __init__(self, size , x, y, path: str):
        super().__init__(size, x, y, path)


class FlyEye(Enemy):
    def __init__(self, size, x, y, folder_path, shift_y):
        super().__init__(size, x, y, folder_path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))


class Slime(Enemy):
    def __init__(self, size, x, y, folder_path, shift_y):
        super().__init__(size, x, y, folder_path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))


class Effect(AnimatedTile):
    def __init__(self,size, x, y):
        super().__init__(size, x, y, 'graphics/explosion')
        self.rect = self.image.get_rect(center = (x, y))

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

class Rocket(Enemy):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics/fly_eye')

class Crab(Enemy):
    def __init__(self, size, x, y, folder_path, shift_y):
        super().__init__(size, x, y, folder_path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))


class Fire(Trap):
    def __init__(self, size , x, y, path: str):
        super().__init__(size, x, y, path)

class Saw(Trap):
    def __init__(self, size, x, y, path: str):
        super().__init__(size, x, y, path)


class MoveSaw(Enemy):
    def __init__(self, size, x, y, folder_path, shift_y):
        super().__init__(size, x, y, folder_path)
        new_y = y + shift_y
        self.rect = self.image.get_rect(midbottom = (x, new_y))

class Banana(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)


class Elevator(Enemy):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)

    def move(self):
        self.rect.y += self.speed


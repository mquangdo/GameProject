import pygame
from supports import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size: int, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((size, size)) # vừa có thể là bề mặt Surface vừa có thể là pygame.image.load

        self.rect = self.image.get_rect(topleft = (x, y))# tương tự như pygame.image.load, ta cũng có thể get_rect

    def update(self, shift: int):
        self.rect.x += shift

class StaticTile(Tile):#dành cho các tile tĩnh như cỏ, crate, terrain
    def __init__(self, size: int, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size: int, x, y):
        super().__init__(size, x, y, pygame.image.load('graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y)) #nếu ta để là y thì các crate sẽ trôi lơ lửng cách mặt đất đúng 1 đoạn bằng size = 64
                                                                    #nên ta cộng thêm size để đẩy nó xuống

class AnimatedTile(Tile):
    def __init__(self,size: int, x, y, path: str):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frames_index = 0
        self.image = self.frames[self.frames_index]

    def animate(self) -> None:
        self.frames_index += 0.15
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self, shift: int) -> None: #ghi đè update ở trên
        self.animate()
        self.rect.x += shift

class Coin(AnimatedTile):
    def __init__(self, size: int, x, y, path: str):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))

class Palm(AnimatedTile):
    def __init__(self, size: int, x, y, path: str, offset: int):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect = self.image.get_rect(topleft = (x, offset_y))

class Enemy(AnimatedTile):
    def __init__(self, size: int, x, y, path: str):
        super().__init__(size, x, y, path)
        offset_y = y + size
        self.rect = self.image.get_rect(midbottom = (x, offset_y))








import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size: int, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((size, size))

        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, shift):
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
    def __init__(self,size: int, x, y):
        super().__init__()
import pygame
from settings import vertical_tile_number, screen_height, screen_width, tile_size
from supports import import_folder

class Sky:
    def __init__(self, horizon: int):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png')
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png')
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png')
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))#nhan tham so la surface va kich co bien doi
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))#nhan tham so la surface va kich co bien doi
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))#nhan tham so la surface va kich co bien doi

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class Water:
    def __init__(self, horizon: int, path: str):
        self.frames = import_folder(path)
        self.frames_index = 0
        self.image = self.frames[self.frames_index]









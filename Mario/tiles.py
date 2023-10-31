import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))# tao ra 1 surface hinh vuong size = size ( width = height)
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos )

    def update(self, x_shift_pos):
        self.rect.x += x_shift_pos
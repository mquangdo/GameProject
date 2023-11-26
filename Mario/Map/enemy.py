import pygame
from tiles import AnimatedTile
import random

class Enemy(AnimatedTile):
    def __init__(self, size: int, x, y):
        super().__init__(size, x, y, 'graphics/enemy/run')
        offset_y = self.rect.y + size
        self.rect = self.image.get_rect(midbottom = (x, offset_y))
        self.speed = random.randint(4,6)

    def move(self) -> None:
        self.rect.x += self.speed

    def reverse_image(self) -> None:
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self) -> None:
        self.speed = self.speed * -1

    def update(self, shift: int) -> None:
        self.animate()
        self.rect.x += shift
        self.move()
        self.reverse_image()


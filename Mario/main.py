import pygame
from pygame.locals import *
import sys
from settings import *
from tiles import Tile
from level import Level
from player import Player
from support import import_folder   

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# test_tile = pygame.sprite.Group(Tile((100, 100), 200))
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()




    screen.fill('Black')
    level.run()



    # test_tile.draw(screen)

    pygame.display.update()
    clock.tick(60)

import pygame, sys
from settings import *
from level import Level
from game_data import level_0, level_1, level_2

class Map0(Level):
    def __init__(self, level_0):
        super().__init__(level_0, screen)
class Map1(Map0):
    def __init__(self, level_1):
        super().__init__(level_1)
class Map2(Map0):
    def __init__(self, level_2):
        super().__init__(level_2)


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
background = pygame.image.load('graphics/background/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
background_rect = background.get_rect(topleft = (0, 0))

map0 = Map0(level_0)
map1 = Map1(level_1)
map2 = Map2(level_2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, background_rect)

    if map0.switch_level():
        map0.run()
    else:
        if map1.switch_level():
            map1.run()
        else:
            if map2.switch_level():
                map2.run()

    pygame.display.update()
    clock.tick(60)
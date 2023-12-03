import pygame, sys
from settings import *
from level import Level
from game_data import level_0




pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
background = pygame.image.load('graphics/background/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
background_rect = background.get_rect(topleft = (0, 0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    screen.blit(background, background_rect)
    level.run()

    pygame.display.update()
    clock.tick(60)
import pygame, sys
from settings import *
from level import Level
from game_data import level_0, level_1




pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
background = pygame.image.load('graphics/background/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
background_rect = background.get_rect(topleft = (0, 0))

obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 100)

stone_surf = pygame.image.load('graphics/stone/1.png')
stone_rect = stone_surf.get_rect(midbottom = (100, 100))

def movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x += 5
            screen.blit(stone_surf, stone_rect)

        return obstacle_list
    else:
        return []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == obstacle_timer:
            obstacle_rect_list.append(stone_surf.get_rect(midbottom = (100, 100)))



    screen.fill('grey')
    screen.blit(background, background_rect)
    level.run()


    pygame.display.update()
    clock.tick(60)
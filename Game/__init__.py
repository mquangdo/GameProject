import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Game")
test_font = pygame.font.Font('Font/Pixeltype.ttf',50)






ground_surface = pygame.image.load('GameImages/ground.png')
sky_surface = pygame.image.load('GameImages/Sky.png')
text_surface = test_font.render('My game',False,'Black')
text_rect = text_surface.get_rect(center = (400,50))


clock = pygame.time.Clock()

snail_surface = pygame.image.load('GameImages/snail1.png')
snail_x_pos = 600
snail_rect = snail_surface.get_rect(midbottom = (600,300))


player_surface = pygame.image.load('GameImages/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                if player_rect.bottom >= 300:
                    player_gravity = -20

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20

        if event.type == pygame.KEYUP :
            print("up")

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))

    pygame.draw.rect(screen, 'Pink', text_rect)
    pygame.draw.rect(screen, 'Pink', text_rect,10)
    #pygame.draw.line(screen,'Yellow',(0,0),pygame.mouse.get_pos(),10)
    pygame.draw.ellipse(screen, 'Brown',pygame.Rect(50,200,100,100))

    screen.blit(text_surface,text_rect)

    #Snail
    snail_rect.right-= 4
    if snail_rect.right<=0:
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    #Player
    i = 1
    player_gravity += i
    player_rect.y += player_gravity
    if player_rect.bottom >= 300 :
        player_rect.bottom = 300
        #screen.blit(player_surface,player_rect)(nếu dòng này trong vòng for sẽ làm player tàng hình)
    screen.blit(player_surface, player_rect)

    if snail_rect.colliderect(player_rect):
        pygame.quit()
        sys.exit()

    #endgame condition


    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE] :
    #     print('sth')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print("1")


    pygame.display.update()
    clock.tick(60)

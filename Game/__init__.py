import pygame, sys
from pygame.locals import *

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time #cho ta thời gian tính bằng đơn vị mili giây
    score_surf = test_font.render(f'Score:{current_time}', False, (64, 64, 64))#cứ đặt là False, vì sao thì chưa rõ
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

def intro():
    text_surface = test_font.render('Press SPACE to run', False, 'White')
    text_rect = text_surface.get_rect(center = (400, 100))
    screen.blit(text_surface, text_rect)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Game")
test_font = pygame.font.Font('Font/Pixeltype.ttf',50)
game_active = False
start_time = 0



ground_surface = pygame.image.load('GameImages/ground.png')
sky_surface = pygame.image.load('GameImages/Sky.png')
# score_surface = test_font.render('My game', False, 'Black')
# score_rect = score_surface.get_rect(center = (400, 50))

clock = pygame.time.Clock()

snail_surface = pygame.image.load('GameImages/snail1.png')
snail_x_pos = 600 # can comment this cause i used rec instead
snail_rect = snail_surface.get_rect(midbottom = (600,300))


player_surface = pygame.image.load('GameImages/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

player_gravity = 0

#Intro
player_stand = pygame.image.load('GameImages/player_stand.png').convert_alpha()

#pygame.transform.scale(surface, tuple) co tac dung thay doi don vi truc Ox, Oy cua surface
#ví dụ
#player_stand_scale = pygame.transform.scale(player_stand, (400, 200))
# nếu ta viết dòng code trên rồi thay het player_stand bằng player_stand_scale thì
#nhân vật của ta sẽ bị kéo giãn ra



player_stand = pygame.transform.rotozoom(player_stand, 0, 2)#ta không cần phải khởi taạo biến player_stand_scale mới
player_stand_rect = player_stand.get_rect(center = (400, 200))

#haàm pygame.transform.rotozoom nhận vào 3 tham số là surface, góc quay, và độ phóng đại -> phóng to surface cũ của ta lên 2 lần
#hàm này còn làm surface của ta trông smooth hơn và do đó nó ưu việt hơn

#Cụ thể ở đây là đầu tiên ta import ảnh, sau đó ta update surface player_stand bằng phương thức pygame.transform.scale, nó sẽ trả về một surface mới ghi đè lên surface cũ, nghĩa là gán surface cũ bằng surface mới
game_name = test_font.render('Pixel Runner', False, 'white')
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = test_font.render('Press SPACE to run', False, 'white')
game_message_rect = game_message.get_rect(center = (400, 350))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if game_active == True:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.x = 800
                    start_time = int(pygame.time.get_ticks() / 1000)



    if game_active:  #khoi tao gia tri game_active = True, neu va cham thi dat lai = False
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # pygame.draw.rect(screen, 'Pink', score_rect)
        # pygame.draw.rect(screen, 'Pink', score_rect, 10)
        #pygame.draw.line(screen,'Yellow',(0,0),pygame.mouse.get_pos(),10)
        # pygame.draw.ellipse(screen, 'Brown',pygame.Rect(50,200,100,100))

        # screen.blit(score_surface, score_rect)
        display_score() #dùng hàm này thay 3 câu lệnh trên để có thể update trên score_surface


        #Snail
        snail_rect.right -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        #Player

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300 :
            player_rect.bottom = 300
            #screen.blit(player_surface,player_rect)(nếu dòng này trong vòng for sẽ làm player tàng hình)
        screen.blit(player_surface, player_rect)

        if snail_rect.colliderect(player_rect):
            game_active = False # do game ko update them bat cu hinh anh nao trong khoi lenh nay nen game stop

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        # intro()
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)

    #endgame condition


    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE] :
    #     print('sth')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print("1")


    pygame.display.update()
    clock.tick(60)

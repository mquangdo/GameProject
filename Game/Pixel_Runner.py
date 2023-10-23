import pygame, sys
from pygame.locals import *
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time #cho ta thời gian tính bằng đơn vị mili giây
    score_surf = test_font.render(f'Score:{current_time}', False, (64, 64, 64))#cứ đặt là False, vì sao thì chưa rõ
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

def intro():
    text_surface = test_font.render('Press SPACE to run', False, 'White')
    text_rect = text_surface.get_rect(center = (400, 100))
    screen.blit(text_surface, text_rect)

def obstacle_movement(obstacle_list: list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            elif obstacle_rect.bottom == 210:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collision(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    #play walking if on floor, jump if not on floor
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

def snail_animation():
    global snail_surface, snail_index
    snail_index += 0.1
    if snail_index >= len(snail_frame):
        snail_index = 0
    snail_surface = snail_frame[int(snail_index)]

def fly_animate():
    global fly_surface, fly_index
    fly_index += 0.1
    if fly_index >= len(fly_frame):
        fly_index = 0
    fly_surface = fly_frame[int(fly_index)]


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

#Fly frame
fly_frame_1 = pygame.image.load('GameImages/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('GameImages/Fly2.png').convert_alpha()
fly_frame = [fly_frame_1, fly_frame_2]
fly_index = 0

fly_surface = fly_frame[fly_index]


#snail frame
snail_frame_1 = pygame.image.load('GameImages/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('GameImages/snail2.png').convert_alpha()
snail_frame = [snail_frame_1, snail_frame_2]
snail_index = 0

snail_surface = snail_frame[snail_index]
# snail_x_pos = 600 # can comment this cause i used rec instead
# snail_rect = snail_surface.get_rect(midbottom = (600,300))

fly_surface = pygame.image.load('GameImages/Fly1.png').convert_alpha()

obstacle_rect_list = []


#Player frame
player_walk_1 = pygame.image.load('GameImages/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('GameImages/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('GameImages/jump.png').convert_alpha()

player_surface = player_walk[player_index]
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

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)#bien 1500 hoat dong giong nhu 1 chu ki spawn enemies

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
                    # snail_rect.x = 800
                    start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100),300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))


    if game_active:  #khoi tao gia tri game_active = True, neu va cham thi dat lai = False
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # pygame.draw.rect(screen, 'Pink', score_rect)
        # pygame.draw.rect(screen, 'Pink', score_rect, 10)
        #pygame.draw.line(screen,'Yellow',(0,0),pygame.mouse.get_pos(),10)
        # pygame.draw.ellipse(screen, 'Brown',pygame.Rect(50,200,100,100))

        # screen.blit(score_surface, score_rect)
        display_score() #dùng hàm này thay 3 câu lệnh trên để có thể update trên score_surface



        #vi ta da dung cac spawn enemies o tren nên ta không cần đoạn code spawn ốc sên này nữa
        #Snail
        # snail_rect.right -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)



        #Player
        player_animation()
        snail_animation()
        fly_animate()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300 :
            player_rect.bottom = 300
            #screen.blit(player_surface,player_rect)(nếu dòng này trong vòng for sẽ làm player tàng hình)
        screen.blit(player_surface, player_rect)


        game_active = collision(player_rect, obstacle_rect_list)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # if snail_rect.colliderect(player_rect):
        #     game_active = False # do game ko update them bat cu hinh anh nao trong khoi lenh nay nen game stop

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
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

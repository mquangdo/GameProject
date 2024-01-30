import pygame
from tiles import Tile
from supports import import_folder
import math
from ui import UI

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.4
        # self.image = pygame.Surface((32, 64))#tao ra 1 surface 32*64, hiển nhiên tile_size của ta đang là 64 nên ta mới để là 32*64
        self.image = self.animations['idle'][self.frame_index]#value của key 'idle' là 1 list các frame idle
        # self.image.fill('red')#fill bằng màu đỏ
        self.rect = self.image.get_rect(topleft = pos)#khởi tạo rect và chọn "tâm" là topleft
        #Trong pygame, vector2 là 1 list chứa các giá trị x và y, ta có thể thêm vector vào vị trí của 1 rect: rect.center += pygame.math.Vector2(100,50)



        #player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -13


        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.on_air = False
        self.double_jump = False

        self.jumping = False
        self.double_jumping = False
        self.jump_count = 300


        #collisions
        self.invincible = False
        self.timer = 1000
        self.hurt_time = 0

        #ui setup
        self.max_health = 100
        self.current_health = 100

        #audio
        self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
        self.jump_sound.set_volume(0.1)
        self.hurt_sound = pygame.mixer.Sound('audio/effects/hurt.mp3')
        # self.game_sound = pygame.mixer.Sound('audio/y2mate.com - 2d game OST  Background Music.mp3')
        # self.game_sound.set_volume(0.07)
        self.running_sound = pygame.mixer.Sound('audio/y2mate.com - Running Sound Effect.mp3')

    def import_character_assets(self) -> None:
        character_path = 'pink_man/'
        self.animations = {'idle': [], 'run': [], 'double_jump': [], 'fall': []}


        for animation in self.animations.keys():
            full_path = character_path + animation  #1 cách hay để lấy được đường dẫn đủ cho từng folder bằng vòng for
            self.animations[animation] = import_folder(full_path) #gắn key bằng import_folder

    def animate(self) -> None:
        animation = self.animations[self.status] #animation là value tại key = self.status, trong đó status gồm idle, run, fall, jump, là một list gồm các frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)] #tạo ra 1 local variable là 1 list các frame
        if self.facing_right == True: #nếu facing_right = True thì bình thường
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False) #false thì dùng pyamge.transform.flip() để flip các frame
            self.image = flipped_image

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


        #điều chỉnh các rectangle, khối code này giúp các frame của ta không bị trôi nổi lềnh bềnh trên tile
        # if self.on_ground:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #     self.rect = self.image.get_rect(center = self.rect.center)

        #(CODE SAU KHI SỬA)
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)#đặt tọa độ origin của self.rect ở vị trí bottomright của rect
        elif self.on_ground and self.on_left:                                   #như thế khi chạy các frame thì rect của chúng không bị chèn vào tile ở bên phải
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)  #cách giải quyết vấn đề này giống cách xử lí để các frame không nổi lềnh bềnh trên tile, bằng cách đặt origin của rect vào vị trí tiếp xúc với các tile
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.bottomleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #     self.rect = self.image.get_rect(center = self.rect.center) #nếu ta thêm dòng này thì khi ta nhảy lên sát tường thì ta sẽ ko rơi được xuống
        #nguyên nhân là do khi ta áp mặt vào tường, ví dụ áp mặt vào tường ở bên trái, thì lúc này origin của rect của player sẽ ở vị trí bottomleft
        #khi ta nhảy lên, thì ta ko áp mặt vào tường nữa, thì lúc này origin của rect sẽ trở thành center, thì lúc này rect của chúng ta sẽ mở rộng thêm
        #1 chút sang bên trái, do đó va chạm với tile và ta ko rơi xuống được


    def get_damage(self):
        if not self.invincible:
            pygame.mixer.Channel(1).play(self.hurt_sound)
            self.current_health = self.current_health - self.max_health / 10
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincible_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.timer:
                self.invincible = False

    def wave_value(self):
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
    def get_status(self) -> None:#hàm để lấy trạng thái của player dựa vaào direction
        if self.direction.y < 0:
            self.status = 'double_jump'
        elif self.direction.y > self.gravity: #TH đặc biệt
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            elif self.direction.x == 0:
                self.status = 'idle'


    def apply_gravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self) -> None:
        self.direction.y = self.jump_speed


    def get_input(self) -> None:#hàm này sẽ nhận vào các tương tác từ bàn phím
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True  #neu x >0 thi nghia la ta di sang phai, nen facing_right = True

        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False

        else:
            self.direction.x = 0
        if keys[pygame.K_w] and self.on_ground:
            self.jump()
            pygame.mixer.Channel(2).play(self.jump_sound)



    def update(self) -> None:
        self.get_input()

        # self.rect.x += self.direction.x * self.speed #hàm này update vị trí sau khi có tương tác bàn phím
        # self.apply_gravity()      #đã dùng trong level khi tạo vertical_movement_collision()
        self.get_status()
        self.animate()
        self.invincible_timer()

        # self.game_sound.play()

        # self.double()
        # self.double_jump_timer()
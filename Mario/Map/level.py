import pygame
from supports import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm
from enemy import Enemy
from decoration import Sky
from player import Player
from settings import screen_width, screen_height

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        #terrain setup
        terrain_layout: list = import_csv_layout(level_data['terrain']) #level_data se truyen vao la level_0
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #grass setup
        grass_layout: list = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        #crates
        crate_layout: list = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crate_layout, 'crates')

        #coins
        coins_layout: list = import_csv_layout(level_data['coins'])
        self.coins_sprite = self.create_tile_group(coins_layout, 'coins')

        #foreground_palms
        fg_palm_layout: list = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprite = self.create_tile_group(fg_palm_layout, 'fg_palms')

        #background_palms
        bg_palm_layout: list = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprite = self.create_tile_group(bg_palm_layout, 'bg_palms')

        #enemies
        enemy_layout: list = import_csv_layout(level_data['enemies'])
        self.enemy_sprite = self.create_tile_group(enemy_layout, 'enemies')

        #constraints
        constraint_layout: list = import_csv_layout(level_data['constraints'])
        self.constraint_sprite = self.create_tile_group(constraint_layout, 'constraints')

        #decorations
        self.sky = Sky(8)

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)



    def create_tile_group(self, layout: list, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size


                    #terrain
                    if type == 'terrain':
                        terrain_tile_list: list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)] #value là các giá trị trong file csv
                        sprite: StaticTile = StaticTile(tile_size, x, y, tile_surface)#terrain_tile_list là một list gồm các bề mặt new_surface trong supports.py
                                                                          #mà đã được blit các phần ảnh nhỏ lên

                        #ở đây sprite là một đối tượng StaticTile có tham số là tile_surface, được gán bằng các phần tử của list(phần tử chính là cá bề mặt đã được blit)

                    #grass
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png.')
                        tile_surface = grass_tile_list[int(val)]
                        sprite: StaticTile = StaticTile(tile_size, x, y, tile_surface)


                    #crates sẽ có cách tiếp cận khác do grass và terrain có nhieu khối bé ở trong một ảnh, nhưng crate thì chỉ có một khối

                    #crate
                    if type == 'crates':
                        sprite: Crate = Crate(tile_size, x, y)

                    #coin
                    if type == 'coins':
                        if val == '0':
                            sprite: Coin = Coin(tile_size, x, y, "graphics/coins/gold")
                        if val == '1':
                            sprite: Coin = Coin(tile_size, x, y, "graphics/coins/silver")

                    #foreground_palms:
                    if type == 'fg_palms':
                        if val == '1':
                            sprite: Palm = Palm(tile_size, x, y, 'graphics/terrain/palm_small', 38)
                        if val == '2':
                            sprite: Palm = Palm(tile_size, x, y, 'graphics/terrain/palm_large', 64)

                    #background_palms:
                    if type == 'bg_palms':
                        sprite: Palm = Palm(tile_size, x, y, 'graphics/terrain/palm_bg', 38)

                    #enemies
                    if type == 'enemies':
                        sprite: Enemy = Enemy(tile_size, x, y)

                    #constrains
                    if type == 'constraints':
                        sprite: Tile = Tile(tile_size, x, y)


                    sprite_group.add(sprite)

        return sprite_group #tra ve mot Group gom toan cac instance cua class Tile, chinh vi vay ta co the goi cac phuong
                            #thuc cua class Tile nay, vi du self.terrain_sprites.draw(self.display_surface)

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1':
                    sprite = Player((x, y))
                    self.player.add(sprite)

    def collision(self):
        for enemies in self.enemy_sprite:#tham so gom 1 sprite va 1 group
            if pygame.sprite.spritecollide(enemies, self.constraint_sprite, False): #nếu là True thì nó sẽ kill(xóa) đi constraints
                enemies.reverse()

    def horizontal_movement_collision(self) -> None:#kiểm tra va chạm phải và trái
        #.sprite là cho GroupSingle
        #.sprite() là cho Group

        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed#tốc độ của player.rect.x, chính là tốc độ của nhân vật

        collidable_sprite = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palm_sprite.sprites()

        for sprite in collidable_sprite: #lay ra cac sprite trong tiles
            if sprite.rect.colliderect(player.rect):#kiem tra xem neu sprite nay va cham voi player.rect
                if player.direction.x < 0: #nếu đi sang trái
                    player.rect.left = sprite.rect.right#thì nếu va chạm thì ta sẽ chặn player.rect.left = sprite.rect.right
                    player.on_left = True#nếu ta sang trái thì ta đặt biến va chạm bên trái on_left = True
                    #sau dòng code trên, ta lại nảy sinh một vấn đề giống hệ vertical_movement ở dưới

                    #cụ thể ở đây nếu ta gán player.on_left bằng True, nghĩa là ta đang tiếp xúc với tile ở bên trái, vậy nếu
                    #ta nhảy lên rồi tiếp tục đi sang bên trái( nhảy qua tile đó) thì player.on_left vẫn là True

                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        #đoạn code để giải quyết vấn đề
        #cụ thể ở đây ta khởi tạo một thuộc tính là self.current_x , sẽ có giá trị là điểm tiếp xúc giữa player và tile
        #nếu biến player.on_left vẫn bằng True và player.rect.left(vị trí bên trái của player) < vị trí tiếp xúc, nghĩa là lúc này người chơi đã vượt qua điểm tiếp xúc current_x và tiếp tục đi về bên trái
        #thì lúc này không còn va chạm nữa nên ta gán lại player.on_left = False
        #còn 1 trường hợp nữa là player.direction >= 0 thì nghĩa là người chơi hoặc là dừng di chuyển hoặc là đi sang phải, nghĩa là ko tiếp tục đi sang trái và va chạm với bên trái nữa
        #thì ta cũng gán lại player.on_left = False
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0 ):
            player.on_left = False
        elif player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self) -> None:#kiểm tra va chạm trên và dưới
        player = self.player.sprite
        player.apply_gravity()

        collidable_sprite = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palm_sprite.sprites()

        for sprite in collidable_sprite: #lay ra cac sprite trong tiles
            if sprite.rect.colliderect(player.rect):#kiem tra xem neu sprite nay va cham voi player.rect
                if player.direction.y < 0: #nếu quay mặt về bên trái, nghĩa là đi sang trái
                    player.rect.top = sprite.rect.bottom#thì nếu va chạm thì ta sẽ chặn player.rect.left = sprite.rect.right
                    player.direction.y = 0
                    player.on_ceiling = True #player đang đập đầu vào trần nhà
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # nếu không có dòng này thì sau 1 lúc, player mới rơi xuống
                    player.on_ground = True #Do lúc này ta import Player nên ta ko thể dùng self với các thuộc tính cuủa player, do self ở đây chỉ thuộc tính của level
                                         #player.rect.bottom = sprite.rect.top nghĩa là player đang ở trên 1 tile nào đó
                #có một vấn đề là khi ta ở trên tile, thì ta đặt on_ground = True, nhưng nếu ta có nhảy lên thì on_ground vẫn bằng True
                #ta sẽ sửa bằng cách sau       (VẤN ĐỀ ĐÓ Ở ĐÂY)


        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity: #ta nhớ lại rằng nếu player.direction < 0 là đang nhảy
            player.on_ground = False                                                           #player.direction > player.gravity là đang rơi
        if player.on_ceiling and player.direction.y > player.gravity:  #on_ceiling = True và đang rơi do ta không thể nhảy được nữa neên chỉ xét đều kiện đang rơi
            player.on_ceiling = False

    def scroll_x(self) -> None:#to scroll the map
        player = self.player.sprite##.sprite attribute cua lop GroupSingle
        player_x = player.rect.centerx#Lay hoanh do x tai trung tam cua surface player_x
        direction_x = player.direction.x

        if player_x < screen_width / 2  and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - screen_width / 2 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8



    def run(self) -> None:


        self.sky.draw(self.display_surface)

        # bg_palms
        self.bg_palm_sprite.update(self.world_shift)
        self.bg_palm_sprite.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # crates
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        #coins
        self.coins_sprite.update(self.world_shift)
        self.coins_sprite.draw(self.display_surface)

        #fg_palms
        self.fg_palm_sprite.update(self.world_shift)
        self.fg_palm_sprite.draw(self.display_surface)

        #enemies
        self.enemy_sprite.update(self.world_shift)
        self.constraint_sprite.update(self.world_shift)
        # self.constraint_sprite.draw(self.display_surface)
        self.collision()
        self.enemy_sprite.draw(self.display_surface)

        #player
        self.player.update()
        self.scroll_x()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)









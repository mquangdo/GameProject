import pygame
from supports import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_width, screen_height
from tiles import StaticTile, Tree, Stone, Bush, Ladder
from player import Player


class Level:
    def __init__(self, level_data: dict, surface) -> None:
        self.display_surface = surface
        self.world_shift = -1

        #terrain_layout
        terrain_layout: list = import_csv_layout(level_data['terrain'])#level_data['terrain'] là 1 đường dẫn trong dictionary
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # tree_layout
        tree_layout: list = import_csv_layout(level_data['tree'])
        self.tree_sprites = self.create_tile_group(tree_layout, 'tree')

        #willow_layout
        willow_layout: list = import_csv_layout(level_data['willow'])
        self.willow_sprites = self.create_tile_group(willow_layout, 'willow')

        #stone_layout
        stone_layout: list = import_csv_layout(level_data['stone'])
        self.stone_sprites = self.create_tile_group(stone_layout, 'stone')

        #bush
        bush_layout: list = import_csv_layout(level_data['bush'])
        self.bush_sprites = self.create_tile_group(bush_layout, 'bush')


        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #ladder
        ladder: list = import_csv_layout(level_data['ladder'])
        self.ladder_sprites = self.create_tile_group(ladder, 'ladder')


    def create_tile_group(self, layout: list, type: str):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('graphics/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'tree':
                        if val == '0':
                            sprite = Tree(tile_size, x, y, 'graphics/tree/1.png', 46)
                        if val == '1':
                            sprite = Tree(tile_size, x, y, 'graphics/tree/2.png', 46)
                        if val == '2':
                            sprite = Tree(tile_size, x, y, 'graphics/tree/3.png', 46)

                    if type == 'willow':
                        if val == '0':
                            sprite = Tree(tile_size, x, y, 'graphics/willow/1.png', 46)
                        if val == '1':
                            sprite = Tree(tile_size, x, y, 'graphics/willow/2.png', 46)
                        if val == '2':
                            sprite = Tree(tile_size, x, y, 'graphics/willow/3.png', 46)

                    # if type == 'stone':
                    #     if val == '0':
                    #         sprite = Stone(tile_size, x, y, 'graphics/stone/1.png', 46)
                    #     if val == '1':
                    #         sprite = Stone(tile_size, x, y, 'graphics/stone/2.png', 46)
                    #     if val == '2':
                    #         sprite = Stone(tile_size, x, y, 'graphics/stone/3.png', 46)
                    #     if val == '3':
                    #         sprite = Stone(tile_size, x, y, 'graphics/stone/4.png', 46)
                    #     if val == '4':
                    #         sprite = Stone(tile_size, x, y, 'graphics/stone/5.png', 46)
                    if type == 'stone':
                        image_index_list = list(range(1, 6))
                        for index in image_index_list:
                            if val == str(index - 1):
                                full_path = 'graphics/stone/' + str(index) + '.png'
                                sprite = Stone(tile_size, x, y, full_path, 0, 46)

                    if type == 'bush':
                        image_index_list = list(range(1, 10))
                        for index in image_index_list:
                            if val == str(index - 1):
                                full_path = 'graphics/bush/' + str(index) + '.png'
                                sprite = Bush(tile_size, x, y, full_path, 46, 46)
                    if type == 'ladder':
                        if val == '0':
                            sprite = Ladder(tile_size, x, y, 'graphics/ladder/1.png' )

                    sprite_group.add(sprite)
        return sprite_group

    def collision(self):
        for fly_eye in self.fly_eye_sprites.sprites():
            if pygame.sprite.spritecollide(fly_eye, self.bound_sprites, False):
                fly_eye.reverse()

        for slime in self.slime_sprites.sprites():
            if pygame.sprite.spritecollide(slime, self.bound_sprites, False):
                slime.reverse()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1':
                    sprite = Player((x, y))
                    self.player.add(sprite)

    # def collision(self):
    #     for enemies in self.enemy_sprite:#tham so gom 1 sprite va 1 group
    #         if pygame.sprite.spritecollide(enemies, self.constraint_sprite, False): #nếu là True thì nó sẽ kill(xóa) đi constraints
    #             enemies.reverse()

    def horizontal_movement_collision(self) -> None:#kiểm tra va chạm phải và trái
        #.sprite là cho GroupSingle
        #.sprite() là cho Group

        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed / 1.8#tốc độ của player.rect.x, chính là tốc độ của nhân vật

        collidable_sprite = self.terrain_sprites.sprites()

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

        collidable_sprite = self.terrain_sprites.sprites()

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
            self.world_shift = 8 / 1.8
            player.speed = 0
        elif player_x > screen_width - screen_width / 2 and direction_x > 0:
            self.world_shift = -8 / 1.8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def climb(self):
        player = self.player.sprite
        for sprites in self.terrain_sprites.sprites():
            if sprites.rect.colliderect(player.rect):
                player.rect.y -= 1


    def run(self):

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # bush
        self.bush_sprites.draw(self.display_surface)
        self.bush_sprites.update(self.world_shift)


        #tree
        self.tree_sprites.draw(self.display_surface)
        self.tree_sprites.update(self.world_shift)

        #willow
        self.willow_sprites.draw(self.display_surface)
        self.willow_sprites.update(self.world_shift)

        #stone
        self.stone_sprites.draw(self.display_surface)
        self.stone_sprites.update(self.world_shift)

        # player
        self.player.update()
        self.scroll_x()
        # self.scroll_y()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.climb()

        #ladder
        self.ladder_sprites.draw(self.display_surface)
        self.ladder_sprites.update(self.world_shift)
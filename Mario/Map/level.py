import pygame
from supports import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin

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
        foreground_palms_layout: list = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprite = self.create_tile_group(coins_layout, 'fg_palms')

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
                            sprite: Coin  = Coin(tile_size, x, y, "graphics/coins/gold")
                        if val == '1':
                            sprite: Coin = Coin(tile_size, x, y, "graphics/coins/silver")

                    sprite_group.add(sprite)

        return sprite_group #tra ve mot Group gom toan cac instance cua class Tile, chinh vi vay ta co the goi cac phuong
                            #thuc cua class Tile nay, vi du self.terrain_sprites.draw(self.display_surface)
    def run(self):
        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #coins
        self.coins_sprite.update(self.world_shift)
        self.coins_sprite.draw(self.display_surface)

        #
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)





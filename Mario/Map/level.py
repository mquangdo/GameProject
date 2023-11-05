import pygame
from supports import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Crate

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = -4
        #terrain setup
        terrain_layout: list = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #grass setup
        grass_layout: list = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        #crates
        crate_layout: list = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crate_layout, 'crates')
    def create_tile_group(self, layout: list, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)


                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png.')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)


                    #crates sẽ có cách tiếp cận khác do grass và terrain có nhieu khối bé ở trong một ảnh, nhưng crate thì chỉ có một khối
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)



                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)




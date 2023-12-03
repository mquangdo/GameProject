from csv import reader
from settings import tile_size
from os import walk

import pygame.image


def import_csv_layout(path: str) -> list:
    terrain_map = []

    with open(path) as map: #nếu in ra từng dòng của map thì ta sẽ nhận được một file csv, gồm toàn các số
        level = reader(map, delimiter = ',')#level là một danh sách các list, nhưng lúc này các số ở trên sẽ biến thành kiểu str
        for row in level:
            terrain_map.append(list(row))
        return terrain_map #trả về một list các list, các list con này lại gồm các ID của các khối tile

def import_cut_graphic(path: str) -> list:
    cut_tiles = []

    surface = pygame.image.load(path).convert_alpha()

    tile_num_x = surface.get_size()[0] / tile_size
    tile_num_y = surface.get_size()[1] / tile_size

    for row in range(int(tile_num_x)):
        for col in range(int(tile_num_y)):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surface.blit(surface,(0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles


def import_folder(path: str) -> list:
    surface_list = []


    for folder_name, sub_folder, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image      #tạo một đường dẫn đầy đủ đến các file ảnh trong folder có đường dẫn là path
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list #một list chứa các ảnh đã được load
from os import walk

import pygame


#walk sẽ trả về 3 thứ, đường dẫn directory, tên directory, và tên các file trong folder

def import_folder(path: str) -> list:
    surface_list = []
    for _, __, img_files in walk(path):#_ là directory path, __ là directory name
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface) #1 list gồm toàn các frame lấy nhờ pygame.image.load
    return surface_list


# import_folder('5 - fixes/graphics/character/run')#('5 - fixes/graphics/character/run', [], ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png'])
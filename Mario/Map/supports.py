import csv
from csv import reader
from settings import tile_size
import pygame.image
import pygame
from os import walk


def import_csv_layout(path: str) -> list:
    terrain_map = []
    with open(path) as map:  #open path = map, luc nay file csv cua t se la map
        level = reader(map, delimiter = ',') #truyền vào reader() file csv và delimiter, là thứ ngăn cách các giá trị, ở đây là dấu phẩy
        for row in level:
            terrain_map.append(list(row))# ta duoc terrain_map la 1 list ma moi hang cua nó là 1 hàng ở trong map trong Tile
        return terrain_map

def import_cut_graphics(path: str) -> list:
    surface = pygame.image.load(path).convert_alpha() #ta sẽ truyền vào một ảnh terrain_tile.png trong graphic
    tile_num_x = int(surface.get_size()[0] / tile_size)  #surface.get_size() tra ve kich co cua surface [0] la chieu dai, [1] la chieu rong
    tile_num_y = int(surface.get_size()[1] / tile_size)

#việc làm ở trên là khi ta truyền vào một ảnh terrain_tile.png, thì ta sẽ lấy kích cỡ của ảnh đó rồi chia cho tile_size
#nghĩa là ta chia nhỏ ảnh ra thành các ô vuông nhỏ để xem ảnh này ta có thể chia thành bao ô vuông 64 * 64
#xong ta tiếp tục tạo ra một bề mặt có kích cỡ 64 x 64 rồi đặt các ô nhỏ vào, nhớ là phải lấy tọa độ của chúng nhân với tile_size để giãn đều cách ô, ko bị chèn lên nhau
#như ở phần làm map bằng list

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size))  #tao ra 1 surface 64 * 64 de ta co the blit hinh anh len
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))#pygame.Rect(top = x, left = y, width = tile_size, height = tile_size) se gay ra loi
            cut_tiles.append(new_surf) #dest(x,y) x, y càng lớn thì các ô tile sẽ càng rời rạc và ko khít
                                    #ở đây nếu ta không có tham số pygame.Rect là tham số thứ 3 thì nó sẽ blit cả surface(cả ảnh)
                                    #lên new_surface, pygame.Rect giúp ta chỉ blit một phần của surface(một phần của ảnh)
                                    #cụ thể phần nào sẽ được cắt thì sẽ phụ thuộc vào (x,y) ở trong
                                    #ta hình dung khi ảnh được chia thành các ô vuông nhỏ 64*64 thì trông ảnh như 1 cái lưới
                                    #lúc này do tham số thứ 3, ta sẽ không blit cả bức ảnh to đùng lên surface(64x64) mà chỉ blit
                                    #một phần ô vuông nhỏ của ảnh, tọa độ của phần vuông đó chính là (x,y) do ta đã nhân với tile_size để tìm tọa độ của các
                                    #ô vuông 64x64 trong cái lưới kia(lưới ở đây là ảnh vừa được chia)
    return cut_tiles #list này sẽ gồm các bề mặt new_surface đã được blit các ô vuông nhỏ như ở trên

def import_folder(path: str) -> list:
    surface_list = []


    for folder_name, sub_folder, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image      #tạo một đường dẫn đầy đủ đến các file ảnh trong folder có đường dẫn là path
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list #một list chứa các ảnh đã được load



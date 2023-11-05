import csv
from csv import reader
from settings import tile_size
import pygame.image
import pygame


def import_csv_layout(path: str) -> list:
    terrain_map = []
    with open(path) as map:  #open path = map, luc nay file csv cua t se la map
        level = reader(map, delimiter = ',') #truyền vào reader() file csv và delimiter, là thứ ngăn cách các giá trị, ở đây là dấu phẩy
        for row in level:
            terrain_map.append(list(row))# ta duoc terrain_map la 1 list ma moi hang cua nó là 1 hàng ở trong map trong Tile
        return terrain_map

def import_cut_graphics(path: str):
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
            new_surf.blit(surface, (0, 0), pygame.Rect( x,  y,  tile_size,  tile_size))#pygame.Rect(top = x, left = y, width = tile_size, height = tile_size) se gay ra loi
            cut_tiles.append(new_surf) #dest(x,y) x, y càng lớn thì các ô tile sẽ càng rời rạc và ko khít

    return cut_tiles





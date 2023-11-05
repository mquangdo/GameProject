import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player


class Level:
    def __init__(self, level_data: list, surface) -> None:#level_data se la level_map

        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self, layout: list) -> None:#layout o day cung dong vai tro la level_data
        self.tiles = pygame.sprite.Group()#Group se co cac phuong thuc la draw va update
        self.player = pygame.sprite.GroupSingle()#neu muon ve thi ta phai cho player vao 1 group

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell =='X':
                    x = col_index * tile_size #tại sao ta phải nhân với tile_size, do nếu không nhân với tile_size, thì lúc này khoảng cách giữa caác tiles sẽ rất nhỏ, chỉ cách nhau đơn vị pixel
                    y = row_index * tile_size #do đó thì các hình vuông tile sẽ bị chèn lên nhau và tạo thành 1 hình vuông ở góc trái bên trên màn hình
                                              #hơn nữa do kích cỡ các hình vuông là bằng tile_size nên ta mới phải nhân với tile_size để đảm bảm các hình được phân bố đều


                    tile = Tile((x, y), tile_size )#nếu có các vị trí tọa độ mà là X thì ta tạo ra 1 instance Tile có tọa độ x,y và tile_size
                    self.tiles.add(tile) #do tiles đã trong 1 group nên nếu muốn vẽ ra 1 tile thì ta phải dùng tiles.add(), sau đó ở dưới ta gọi draw() để vẽ

                elif cell == 'P':
                    x = col_index * tile_size
                    y = col_index * tile_size

                    player_sprite = Player((x, y))

                    self.player.add(player_sprite)

    def scroll_x(self) -> None:#to scroll the map
        player = self.player.sprite##.sprite attribute cua lop GroupSingle
        player_x = player.rect.centerx#Lay hoanh do x tai trung tam cua surface player_x
        direction_x = player.direction.x

        if player_x < screen_width / 4  and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - screen_width / 4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    def horizontal_movement_collision(self) -> None:#kiểm tra va chạm phải và trái
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed#tốc độ của player.rect.x, chính là tốc độ của nhân vật

        for sprite in self.tiles.sprites(): #lay ra cac sprite trong tiles
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

        for sprite in self.tiles.sprites(): #lay ra cac sprite trong tiles
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

    def run(self) -> None:
        #level tile
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)# ta se draw tren self.display_surface, dĩ nhiên để draw thì ta phải cho vào Group()
        self.scroll_x()
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)





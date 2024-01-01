import pygame

class UI:
    def __init__(self, surface):
        #set up
        self.display_surface = surface

        #health
        self.health_bar = pygame.image.load('graphics/ui/health_bar.png')
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4


        #coins
        self.coin = pygame.image.load('graphics/ui/coin.png')
        self.coin_rect = self.coin.get_rect(midleft = (50, 80))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 30)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

        #pygame.draw.rect dùng để vẽ rectangle
        #còn screen.blit là dùng để vẽ surface với "tâm" cài đặt ở rectangle

    def show_coin(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, 'black')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.x + 40, self.coin_rect.y + 15))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)




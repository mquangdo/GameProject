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

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

        #pygame.draw.rect dùng để vẽ rectangle
        #còn screen.blit là dùng để vẽ surface với "tâm" cài đặt ở rectangle






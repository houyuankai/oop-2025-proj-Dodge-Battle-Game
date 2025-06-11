import pygame

class Window:
    def __init__(self, start_x, start_y, target_x, target_y, width=50, height=100):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (start_x, start_y)
        self.target = (target_x, target_y)
        self.speed = 0.083  # 約 5 像素/幀 (60 FPS)
        self.scale = 1.0
        self.scale_speed = 0.05 # 每幀縮小 2%
        self.min_scale = 0.1  # 最小縮放比例
        self.color = (255, 255, 255)  # 白色
        self.alpha = 255
        

    def update(self, dt):
        # 移動向目標
        dx = self.target[0] - self.rect.centerx
        dy = self.target[1] - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 1:  # 避免過近時抖動
            move_x = dx * self.speed * dt
            move_y = dy * self.speed * dt
            self.rect.centerx += move_x
            self.rect.centery += move_y
        # 縮放
        self.scale = max(self.scale - self.scale_speed * dt, self.min_scale)
        self.rect.width = int(50 * self.scale)
        self.rect.height = int(100 * self.scale)
        if self.rect.width < 5 or self.rect.height < 5:
            return True  # 標記移除
        return False

    def draw(self, screen):
        # 繪製矩形窗戶
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        screen.blit(surface, self.rect.topleft)

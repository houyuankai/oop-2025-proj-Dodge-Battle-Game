import pygame

class Window:
    def __init__(self, start_x, start_y, target_x, target_y, width=100, height=160):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (start_x, start_y)
        self.target_x = target_x  # 僅需 x 目標
        self.speed = 0.042  # 約 5 像素/幀 (60 FPS)
        self.scale = 1.0
        self.scale_speed = 0.03  # 每幀縮小 5%
        self.min_scale = 0.01  # 最小縮放比例
        self.color = (255, 255, 255)  # 純白
        self.alpha = 255  # 完全不透明

    def update(self, dt):
        # 移動：僅沿 x 軸，y 鎖定為 150
        dx = self.target_x - self.rect.centerx
        if abs(dx) > 1:  # 避免過近時抖動
            move_x = dx * self.speed * dt
            self.rect.centerx += move_x
            self.rect.centery = 150  # 強制 y=150
        # 縮放
        self.scale = max(self.scale - self.scale_speed * dt, self.min_scale)
        old_center = self.rect.center  # 保存中心
        self.rect.width = int(50 * self.scale)
        self.rect.height = int(100 * self.scale)
        self.rect.center = old_center  # 恢復中心，確保 y=150
        if self.rect.width < 1 or self.rect.height < 1:
            return True  # 標記移除
        return False

    def draw(self, screen):
        # 繪製矩形窗戶
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        screen.blit(surface, self.rect.topleft)

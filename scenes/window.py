import pygame

class Window:
    def __init__(self, start_x, start_y, target_x, target_y, width=80, height=160):
        self.initial_width = width  # 儲存初始寬度
        self.initial_height = height  # 儲存初始高度
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (start_x, start_y)
        self.target_x = target_x  # 僅需 x 目標
        self.speed = 0.042  # 約 2.5 像素/幀 (60 FPS)
        self.scale = 1.0
        self.scale_speed = 0.025  # 每幀縮小 1%（延長存活時間）
        self.min_scale = 0.01  # 最小縮放比例（提高以確保可見）
        self.color = (255, 255, 255)  # 純白
        self.alpha = 255  # 完全不透明
        print(f"Window initialized with size: {width}x{height}")  # 除錯輸出

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
        self.rect.width = max(int(self.initial_width * self.scale), 1)  # 至少 1 像素
        self.rect.height = max(int(self.initial_height * self.scale), 1)  # 至少 1 像素
        self.rect.center = old_center  # 恢復中心，確保 y=150
        print(f"Window size updated: {self.rect.width}x{self.rect.height}")  # 除錯輸出
        if self.rect.width < 1 or self.rect.height < 1:
            return True  # 標記移除
        return False

    def draw(self, screen):
        # 繪製矩形窗戶
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        screen.blit(surface, self.rect.topleft)

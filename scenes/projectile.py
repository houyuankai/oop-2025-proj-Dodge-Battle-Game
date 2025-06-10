import pygame

class Projectile:
    def __init__(self, rect, vx, vy, angle=0):
        self.rect = rect
        self.vx = vx
        self.vy = vy
        self.angle = angle  # 旋轉角度
      
        # 根據方向和尺寸創建表面
        if vx == 0:  # 上下移動
            self.surface = pygame.Surface((200, 20), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
        elif vy == 0:  # 左右移動
            self.surface = pygame.Surface((20, 200), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
        else:  # 斜向移動
            self.surface = pygame.Surface((20, 200), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
            self.surface = pygame.transform.rotate(self.surface, angle)

import pygame

class Projectile:
    def __init__(self, rect, vx, vy, angle=0):
        self.rect = rect
        self.vx = vx
        self.vy = vy
        self.angle = angle
      
        if vx == 0:
            self.surface = pygame.Surface((200, 20), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
        elif vy == 0:
            self.surface = pygame.Surface((20, 200), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
        else:
            self.surface = pygame.Surface((20, 200), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255))
            self.surface = pygame.transform.rotate(self.surface, angle)

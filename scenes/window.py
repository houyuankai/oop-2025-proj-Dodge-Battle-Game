import pygame
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class Window:
    def __init__(self, start_x, start_y, target_x, target_y, width=20, height=160, scale=1.0):
        try:
            logging.info("Creating window")
            self.initial_width = width
            self.initial_height = height
            self.rect = pygame.Rect(0, 0, width, height)
            self.rect.center = (start_x, start_y)
            self.target_x = target_x
            self.speed = 0.042
            self.scale = 1.0
            self.scale_speed = 0.025
            self.min_scale = 0.01
            self.color = (255, 255, 255)
            self.alpha = 255
            logging.info("Window created")
        except Exception as e:
            logging.error(f"Window initialization failed: {str(e)}")
            print(f"Window initialization failed: {str(e)}")
            raise

    def update(self, dt):
        dx = self.target_x - self.rect.centerx
        if abs(dx) > 1:
            move_x = dx * self.speed * dt
            self.rect.centerx += move_x
            self.rect.centery = 150
        self.scale = max(self.scale - self.scale_speed * dt, self.min_scale)
        old_center = self.rect.center
        self.rect.width = max(int(self.initial_width * self.scale), 1)
        self.rect.height = max(int(self.initial_height * self.scale), 1)
        self.rect.center = old_center
        if self.rect.width < 1 or self.rect.height < 1:
            return True
        return False

    def draw(self, screen):
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        screen.blit(surface, self.rect.topleft)

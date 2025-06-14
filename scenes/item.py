import pygame
import os
from scenes.utils import load_image

class Item:
    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.item_type = item_type  # "item1", "item2", "item3", "item4"
        self.image = load_image(os.path.join("assets", "images", f"{item_type}.png"), size=(40, 40))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3 秒

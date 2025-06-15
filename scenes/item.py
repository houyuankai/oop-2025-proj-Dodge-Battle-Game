import pygame
import os
from scenes.utils import load_image

class Item:
    images = {}

    @classmethod
    def preload_images(cls, scale):
        for item_type in ["item1", "item2", "item3", "item4"]:
            path = os.path.join("assets", "images", f"{item_type}.png")
            try:
                image = pygame.image.load(path)
                image = image.convert_alpha()
                image = pygame.transform.scale(image, (int(50 * scale), int(50 * scale)))
                cls.images[item_type] = image
            except pygame.error as e:
                print(f"Failed to load {item_type}.png: {e}")
                cls.images[item_type] = pygame.Surface((int(40 * scale), int(40 * scale)))
                cls.images[item_type].fill((255, 0, 0))
        for i in range(1, 4):
            try:
                cls.images[f"key{i}"] = load_image(os.path.join("assets", "images", f"key{i}.png"), size=(int(50 * scale), int(50 * scale)))
            except pygame.error as e:
                print(f"Failed to load key{i}.png: {e}")
                cls.images[f"key{i}"] = pygame.Surface((int(40 * scale), int(40 * scale)))
                cls.images[f"key{i}"].fill((255, 0, 0))

    def __init__(self, x, y, item_type):
        self.item_type = item_type
        self.image = Item.images.get(item_type)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000

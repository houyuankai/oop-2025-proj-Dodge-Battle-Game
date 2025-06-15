import pygame
import os

class Item:
    images = {}  # 靜態圖片快取

    @classmethod
    def preload_images(cls):
        """預載入所有物件圖片"""
        for item_type in ["item1", "item2", "item3", "item4"]:
            path = os.path.join("assets", "images", f"{item_type}.png")
            try:
                image = pygame.image.load(path)
                image = image.convert_alpha()  # 優化表面
                image = pygame.transform.scale(image, (50, 50))
                cls.images[item_type] = image
                print(f"Loaded {item_type}.png successfully")
            except pygame.error as e:
                print(f"Failed to load {item_type}.png: {e}")
                cls.images[item_type] = pygame.Surface((40, 40))
                cls.images[item_type].fill((255, 0, 0))  # 預設紅色方塊
        for i in range(1, 4):
            cls.images[f"key{i}"] = load_image(os.path.join("assets", "images", f"key{i}.png"), size=(50, 50))

    def __init__(self, x, y, item_type):
        self.item_type = item_type
        self.image = Item.images.get(item_type, pygame.Surface((40, 40)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3 秒存活

import pygame
import sys
import os

def resource_path(relative_path):
    """獲取打包後或開發中的資源路徑"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 臨時目錄
        return os.path.join(sys._MEIPASS, relative_path)
    # 開發環境：相對專案根目錄
    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def load_image(path, size=None):
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image not found: {full_path}")
    image = pygame.image.load(full_path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

def load_images_from_folder(folder_path, scale=None):
    images = []
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            path = os.path.join(folder_path, filename)
            image = load_image(path, scale)
            images.append(image)
    return images

class Button:
    def __init__(self, image, pos, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

import pygame
import sys
import os

def resource_path(relative_path):
    """取得 PyInstaller 打包後或開發階段的正確資源路徑"""
    try:
        base_path = sys._MEIPASS  # PyInstaller 打包後
    except AttributeError:
        base_path = os.path.abspath(".")  # 開發中

    return os.path.join(base_path, relative_path)

def load_image(path, size=None):
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image not found: {full_path}")
    image = pygame.image.load(full_path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

def load_images_from_folder(folder_path, scale=None):
    full_folder_path = resource_path(folder_path)
    if not os.path.exists(full_folder_path):
        raise FileNotFoundError(f"Folder not found: {full_folder_path}")
    
    images = []
    for filename in sorted(os.listdir(full_folder_path)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            image = load_image(image_path, scale)
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

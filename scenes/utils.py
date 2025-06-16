import pygame
import sys
import os

def resource_path(relative_path):
    """獲取打包後或開發中的資源路徑"""
    if hasattr(sys, 'frozen'):  # PyInstaller 打包環境
        return os.path.join(sys._MEIPASS, relative_path)
    # 開發環境：相對專案根目錄
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # 回到專案根目錄
    return os.path.join(base_path, relative_path)

def load_image(path, size=None):
    """載入並調整圖片大小，適配 PyInstaller 環境"""
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image not found: {full_path}")
    try:
        # 僅載入圖片，不立即轉換
        image = pygame.image.load(full_path)
        if size:
            image = pygame.transform.scale(image, size)
        # 延遲 convert_alpha()，由調用方在顯示初始化後處理
        return image
    except pygame.error as e:
        print(f"Error loading image {full_path}: {e}")
        return pygame.Surface((1, 1))  # 佔位符

def load_images_from_folder(folder_path, scale=None):
    """從資料夾批量載入圖片"""
    images = []
    full_folder_path = resource_path(folder_path)
    if not os.path.exists(full_folder_path):
        raise FileNotFoundError(f"Folder not found: {full_folder_path}")
    for filename in sorted(os.listdir(full_folder_path)):
        if filename.endswith((".png", ".jpg")):
            path = os.path.join(folder_path, filename)  # 使用相對路徑
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

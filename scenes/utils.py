import pygame
import os

def load_image(path, size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, (int(size[0]), int(size[1])))
        return image
    except pygame.error as e:
        print(f"Failed to load image {path}: {e}")
        raise

def load_images_from_folder(folder_path, scale=None):
    images = []
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

import pygame
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def load_image(path, size=None):
    try:
        logging.info(f"Loading image: {path}")
        if not os.path.exists(path):
            logging.error(f"Image not found: {path}")
            raise FileNotFoundError(f"Image not found: {path}")
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, (int(size[0]), int(size[1])))
        logging.info(f"Image loaded: {path}")
        return image
    except Exception as e:
        logging.error(f"Failed to load image {path}: {str(e)}")
        print(f"Failed to load image {path}: {str(e)}")
        raise

def load_images_from_folder(folder_path, scale=None):
    images = []
    try:
        logging.info(f"Loading images from folder: {folder_path}")
        if not os.path.exists(folder_path):
            logging.error(f"Folder not found: {folder_path}")
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                path = os.path.join(folder_path, filename)
                image = load_image(path, scale)
                images.append(image)
                logging.info(f"Loaded image from folder: {path}")
        return images
    except Exception as e:
        logging.error(f"Failed to load images from {folder_path}: {str(e)}")
        print(f"Failed to load images from {folder_path}: {str(e)}")
        raise

class Button:
    def __init__(self, image, pos, scale=1):
        try:
            logging.info("Creating button")
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect(center=pos)
            logging.info("Button created")
        except Exception as e:
            logging.error(f"Button initialization failed: {str(e)}")
            print(f"Button initialization failed: {str(e)}")
            raise

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

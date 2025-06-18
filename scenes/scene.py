import pygame
from scenes.utils import resource_path, load_image

class Scene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.scale = game.scale

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

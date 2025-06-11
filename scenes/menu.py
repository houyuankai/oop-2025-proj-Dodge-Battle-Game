import pygame
import os
from scenes.battle import BattleScene
from scenes.utils import load_image 

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        self.background = load_image(os.path.join("assets", "images", "menu_background.png"), size=(600, 900))
        self.start_button = load_image(os.path.join("assets", "images", "start_button.png"), size=(100, 50))
        self.start_button_rect = self.start_button.get_rect(center=(300, 600))
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.title_surface = self.title_font.render("Dungeon Boss Fight", True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(300, 200))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.game.change_scene(BattleScene(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title_surface, self.title_rect)
        screen.blit(self.start_button, self.start_button_rect)

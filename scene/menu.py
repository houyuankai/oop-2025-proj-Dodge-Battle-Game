import pygame
import os
from scenes.battle import BattleScene

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.background = pygame.image.load(os.path.join("assets", "images", "menu_background.png"))
        self.start_button = pygame.image.load(os.path.join("assets", "images", "start_button.png"))
        self.start_button_rect = self.start_button.get_rect(center=(300, 600))

        self.title_font = pygame.font.SysFont("Arial", 64)
        self.title_surface = self.title_font.render("Dungeon Boss Fight", True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(300, 200))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.game.change_scene(BattleScene(self.game))

    def update(self):
        pass  # Menu doesn't have updates yet

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title_surface, self.title_rect)
        screen.blit(self.start_button, self.start_button_rect)

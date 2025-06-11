import pygame
import os

class ButtonManager:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        # Load button images
        self.play_again_image = pygame.image.load(os.path.join("assets", "images", "play_again.png"))
        self.to_menu_image = pygame.image.load(os.path.join("assets", "images", "to_menu.png"))
        # Define button rects
        self.play_again_rect = self.play_again_image.get_rect(topleft=(150, 600))
        self.to_menu_rect = self.to_menu_image.get_rect(topleft=(350, 600))

    def handle_event(self, event, battle_scene):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.play_again_rect.collidepoint(mouse_pos):
                battle_scene.reset_game()
            elif self.to_menu_rect.collidepoint(mouse_pos):
                self.game.set_scene("menu")

    def draw(self, screen):
        screen.blit(self.play_again_image, self.play_again_rect)
        screen.blit(self.to_menu_image, self.to_menu_rect)

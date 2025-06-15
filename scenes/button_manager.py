import pygame
import os
import logging
from scenes.utils import load_image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class ButtonManager:
    def __init__(self, game):
        try:
            logging.info("Initializing ButtonManager")
            self.game = game
            self.screen = game.screen
            self.scale = game.scale
            self.play_again_image = load_image(os.path.join("assets", "images", "play_again.png"), size=(120, 60))
            self.to_menu_image = load_image(os.path.join("assets", "images", "to_menu.png"), size=(120, 60))
            self.play_again_rect = self.play_again_image.get_rect(topleft=(120, 700))
            self.to_menu_rect = self.to_menu_image.get_rect(topleft=(380, 700))
            logging.info("ButtonManager initialized")
        except Exception as e:
            logging.error(f"ButtonManager initialization failed: {str(e)}")
            print(f"ButtonManager initialization failed: {str(e)}")
            raise

    def handle_event(self, event, battle_scene):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.play_again_rect.collidepoint(mouse_pos):
                battle_scene.reset_game()
                logging.info("Play again button clicked")
            elif self.to_menu_rect.collidepoint(mouse_pos):
                pygame.mixer.music.stop()
                self.game.current_music = None
                self.game.change_scene("menu")
                logging.info("To menu button clicked")

    def draw(self, screen):
        screen.blit(self.play_again_image, self.play_again_rect)
        screen.blit(self.to_menu_image, self.to_menu_rect)

import pygame
import os
from scenes.utils import load_image  # 新增：匯入 load_image

class ButtonManager:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # 更新：使用 load_image 載入按鈕圖片，統一 100x50
        self.play_again_image = load_image(os.path.join("assets", "images", "play_again.png"), size=(100, 50))
        self.to_menu_image = load_image(os.path.join("assets", "images", "to_menu.png"), size=(100, 50))
        self.play_again_rect = self.play_again_image.get_rect(topleft=(150, 600))
        self.to_menu_rect = self.to_menu_image.get_rect(topleft=(350, 600))

    def handle_event(self, event, battle_scene):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.play_again_rect.collidepoint(mouse_pos):
                print("Play Again button clicked") 
                battle_scene.reset_game()
            
            elif self.to_menu_rect.collidepoint(mouse_pos):
                print("Menu button clicked")  # 除錯
                self.game.change_scene("menu")

    def draw(self, screen):
        screen.blit(self.play_again_image, self.play_again_rect)
        screen.blit(self.to_menu_image, self.to_menu_rect)

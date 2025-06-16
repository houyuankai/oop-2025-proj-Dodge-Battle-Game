import pygame
import os
from scenes.battle import BattleScene
from scenes.utils import load_image, resource_path

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen  # 確保 screen 已通過 pygame.display.set_mode 初始化
        self.scale = game.scale
        bg_path = os.path.join("assets", "images", "menu_background.png")
        start_path = os.path.join("assets", "images", "start_button.png")
        if not os.path.exists(resource_path(bg_path)):
            raise FileNotFoundError(f"Image not found: {bg_path}")
        if not os.path.exists(resource_path(start_path)):
            raise FileNotFoundError(f"Image not found: {start_path}")
        self.background = load_image(bg_path, size=(600, 900))
        if pygame.display.get_init():  # 確保顯示初始化
            self.background = self.background.convert_alpha()
        self.start_button = load_image(start_path, size=(150, 75))
        if pygame.display.get_init():
            self.start_button = self.start_button.convert_alpha()
        self.start_button_rect = self.start_button.get_rect(center=(300, 750))
        self.music_path = os.path.join("assets", "sounds", "music_1.mp3")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                pygame.mixer.music.stop()
                self.game.current_music = None
                self.game.change_scene(BattleScene(self.game))

    def update(self):
        if self.game.current_music != "music_1.mp3":
            pygame.mixer.music.stop()
            if os.path.exists(resource_path(self.music_path)):
                pygame.mixer.music.load(resource_path(self.music_path))
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.game.current_music = "music_1.mp3"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.start_button, self.start_button_rect)

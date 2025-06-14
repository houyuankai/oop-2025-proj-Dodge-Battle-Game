import pygame
import os
from scenes.battle import BattleScene
from scenes.utils import load_image 

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        self.background = load_image(os.path.join("assets", "images", "menu_background.png"), size=(600, 900))
        self.start_button = load_image(os.path.join("assets", "images", "start_button.png"), size=(150, 75))
        self.start_button_rect = self.start_button.get_rect(center=(300, 750))
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.title_surface = self.title_font.render("Dungeon Boss Fight", True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(300, 200))
        self.music_path = os.path.join("assets", "sounds", "music_1.mp3")  # 音樂路徑

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                pygame.mixer.music.stop()  # 停止音樂
                self.game.current_music = None
                self.game.change_scene(BattleScene(self.game))

    def update(self):
        if self.game.current_music != "music_1.mp3": # 播放選單音樂
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # 迴圈播放
            self.game.current_music = "music_1.mp3"
            
    def draw(self, screen):
        # 繪製背景
        screen.blit(self.background, (0, 0))
        # 繪製開始按鍵
        screen.blit(self.start_button, self.start_button_rect)

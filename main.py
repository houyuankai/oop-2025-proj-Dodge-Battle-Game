import pygame
import sys
import os
from scenes.menu import MenuScene
from scenes.battle import BattleScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # 動態獲取螢幕高度
        info = pygame.display.Info()
        screen_height = info.current_h
        # 保持 2:3 比例
        self.screen_height = screen_height
        self.screen_width = int(screen_height * 2 / 3)
        self.scale = screen_height / 900  # 縮放比例
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Cuddle Time!")
        # 置中視窗
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = MenuScene(self)
        self.current_music = None

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                self.current_scene.handle_event(event)

    def change_scene(self, new_scene):
        pygame.mixer.music.stop()
        self.current_music = None
        if isinstance(new_scene, str):
            if new_scene == "menu":
                self.current_scene = MenuScene(self)
            elif new_scene == "battle":
                self.current_scene = BattleScene(self)
            else:
                raise ValueError(f"Unknown scene name: {new_scene}")
        else:
            self.current_scene = new_scene

import pygame
import sys
from scenes.menu import MenuScene
from scenes.battle import BattleScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeon Boss Fight")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = MenuScene(self)

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
        if isinstance(new_scene, str):
            if new_scene == "menu":
                self.current_scene = MenuScene(self)
            elif new_scene == "battle":
                self.current_scene = BattleScene(self)
            else:
                raise ValueError(f"Unknown scene name: {new_scene}")
        else:
            self.current_scene = new_scene

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

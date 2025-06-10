import pygame
import sys
from scenes.menu import MenuScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeon Boss Fight")
        self.clock = pygame.time.Clock()
        self.running = True

        # 場景控制
        self.current_scene = MenuScene(self)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.current_scene.handle_event(event)

    def change_scene(self, new_scene):
        self.current_scene = new_scene

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
  

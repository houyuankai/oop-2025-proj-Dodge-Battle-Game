import pygame
import sys
from scenes.menu import MenuScene
from scenes.battle import BattleScene  # 新增：BattleScene

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
            print(f"Current scene: {type(self.current_scene).__name__}")  # 除錯
            self.handle_events()
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.update()  # 改用 update 代替 flip，確保刷新
            
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Handling event: {event.key}")
                self.current_scene.handle_event(event)
        pygame.event.clear(pygame.KEYDOWN)  # 清空鍵盤事件，防止重複


    def change_scene(self, new_scene):
        print(f"Changing scene to: {new_scene}")  # 除錯
        if isinstance(new_scene, str):
            if new_scene == "menu":
                self.current_scene = MenuScene(self)
            elif new_scene == "battle":
                self.current_scene = BattleScene(self)
            else:
                raise ValueError(f"Unknown scene name: {new_scene}")
        else:
            self.current_scene = new_scene
        print(f"New scene: {type(self.current_scene).__name__}")  # 除錯


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
  

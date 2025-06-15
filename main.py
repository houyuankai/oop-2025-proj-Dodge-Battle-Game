import pygame
import sys
import os
import logging
from scenes.menu import MenuScene
from scenes.battle import BattleScene

# 設置日誌
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class Game:
    def __init__(self):
        try:
            logging.info("Starting Game initialization...")
            print("Starting Game initialization...")
            pygame.init()
            logging.info("pygame initialized")
            pygame.mixer.init()
            logging.info("pygame.mixer initialized")
            self.screen_width = 600
            self.screen_height = 900
            self.scale = 1.0
            logging.info(f"Screen size: {self.screen_width}x{self.screen_height}, Scale: {self.scale}")
            os.environ['SDL_VIDEO_CENTERED'] = '1'
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            logging.info("Display mode set")
            pygame.display.set_caption("Cuddle Time!")
            self.clock = pygame.time.Clock()
            self.running = True
            self.current_scene = MenuScene(self)
            logging.info("MenuScene initialized")
            self.current_music = None
        except Exception as e:
            logging.error(f"Initialization failed: {str(e)}")
            print(f"Initialization failed: {str(e)}")
            sys.exit(1)

    def run(self):
        try:
            logging.info("Starting game loop")
            while self.running:
                self.clock.tick(60)
                self.handle_events()
                self.current_scene.update()
                self.current_scene.draw(self.screen)
                pygame.display.update()
        except Exception as e:
            logging.error(f"Runtime error: {str(e)}")
            print(f"Runtime error: {str(e)}")
            pygame.quit()
            sys.exit(1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logging.info("Quit event received")
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                self.current_scene.handle_event(event)

    def change_scene(self, new_scene):
        try:
            pygame.mixer.music.stop()
            self.current_music = None
            if isinstance(new_scene, str):
                if new_scene == "menu":
                    self.current_scene = MenuScene(self)
                    logging.info("Changed to MenuScene")
                elif new_scene == "battle":
                    self.current_scene = BattleScene(self)
                    logging.info("Changed to BattleScene")
                else:
                    raise ValueError(f"Unknown scene name: {new_scene}")
            else:
                self.current_scene = new_scene
                logging.info("Changed to custom scene")
        except Exception as e:
            logging.error(f"Scene change failed: {str(e)}")
            print(f"Scene change failed: {str(e)}")

if __name__ == "__main__":
    try:
        logging.info("Starting main execution")
        game = Game()
        game.run()
    except Exception as e:
        logging.error(f"Main execution failed: {str(e)}")
        print(f"Main execution failed: {str(e)}")
        sys.exit(1)

import pygame
import os
import logging
from scenes.utils import load_image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class InstructionScene:
    def __init__(self, game, image_paths, next_state, battle_scene):
        try:
            logging.info("Initializing InstructionScene")
            self.game = game
            self.screen = game.screen
            self.scale = game.scale
            self.image_paths = image_paths
            self.next_state = next_state
            self.battle_scene = battle_scene
            self.current_page = 0
            self.done = False
            self.images = []
            for path in image_paths:
                if not os.path.exists(path):
                    logging.error(f"Image not found: {path}")
                    raise FileNotFoundError(f"Image not found: {path}")
                self.images.append(load_image(path, size=(600, 900)))
            self.sound = None
            sound_path = os.path.join("assets", "sounds", "music_5.mp3")
            if os.path.exists(sound_path):
                self.sound = pygame.mixer.Sound(sound_path)
                self.sound.set_volume(0.5)
                self.sound.play(0)
                logging.info("Playing instruction sound")
            else:
                logging.error(f"Sound not found: {sound_path}")
            logging.info("InstructionScene initialized")
        except Exception as e:
            logging.error(f"InstructionScene initialization failed: {str(e)}")
            print(f"InstructionScene initialization failed: {str(e)}")
            raise

    def handle_event(self, event):
        if self.done:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.sound:
                self.sound.stop()
            self.current_page += 1
            if self.current_page >= len(self.image_paths):
                self.battle_scene.state = self.next_state
                if self.next_state == "dodge_countdown":
                    self.battle_scene.dodge_countdown_timer = pygame.time.get_ticks()
                elif self.next_state == "attack":
                    self.battle_scene.attack_start_time = pygame.time.get_ticks()
                    self.battle_scene.attack_active = False
                self.game.change_scene(self.battle_scene)
                self.done = True
                logging.info("Instruction completed")
            else:
                if self.sound:
                    self.sound.play(0)
                    logging.info("Next instruction page")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((240, 205, 0))
        if self.current_page < len(self.images):
            screen.blit(self.images[self.current_page], (0, 0))

import pygame
from scenes.utils import load_image

class InstructionScene:
    def __init__(self, game, image_paths, next_state, battle_scene):
        self.game = game
        self.screen = game.screen
        self.image_paths = image_paths
        self.next_state = next_state
        self.battle_scene = battle_scene
        self.current_page = 0
        self.done = False
        try:
            self.images = [load_image(path, size=(600, 900)) for path in image_paths]
        except Exception as e:
            print(f"Image load error: {e}")
            raise

    def handle_event(self, event):
        if self.done:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((240, 205, 50))
        if self.current_page < len(self.images):
            screen.blit(self.images[self.current_page], (0, 0))
        else:
            print(f"Warning: current_page {self.current_page} out of range, skipping draw")

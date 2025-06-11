import pygame
from scenes.utils import load_image

class InstructionScene:
    def __init__(self, game, image_paths, next_state, battle_scene):
        self.game = game
        self.screen = game.screen
        self.image_paths = image_paths
        self.next_state = next_state
        self.battle_scene = battle_scene  # 保存 BattleScene 實例
        self.current_page = 0
        try:
            self.images = [load_image(path, size=(600, 900)) for path in image_paths]
            print(f"Loaded {len(self.images)} images: {image_paths}")
        except Exception as e:
            print(f"Image load error: {e}")
            raise

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.current_page += 1
            print(f"Space pressed, current_page: {self.current_page}")
            if self.current_page >= len(self.image_paths):
                print(f"Switching to {self.next_state}")
                self.battle_scene.state = self.next_state
                if self.next_state == "dodge_countdown":
                    self.battle_scene.dodge_countdown_timer = pygame.time.get_ticks()
                    print(f"Reset dodge_countdown_timer: {self.battle_scene.dodge_countdown_timer}")
                elif self.next_state == "attack":
                    self.battle_scene.attack_start_time = pygame.time.get_ticks()
                    self.battle_scene.attack_active = False
                    print(f"Reset attack_start_time: {self.battle_scene.attack_start_time}")
                self.game.current_scene = self.battle_scene
                print(f"Switched to BattleScene, state: {self.battle_scene.state}")
            else:
                print(f"Showing page {self.current_page + 1}/{len(self.image_paths)}")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((240, 205, 0))
        if self.current_page < len(self.images):
            screen.blit(self.images[self.current_page], (0, 0))
        else:
            print(f"Warning: current_page {self.current_page} out of range, skipping draw")

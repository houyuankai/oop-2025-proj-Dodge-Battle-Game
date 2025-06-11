import pygame
from scenes.utils import load_image

class InstructionScene:
    def __init__(self, game, image_paths, next_state):
        self.game = game
        self.screen = game.screen
        self.image_paths = image_paths  # 圖片路徑清單
        self.next_state = next_state  # 下個階段（"dodge_countdown" 或 "attack"）
        self.current_page = 0
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        # 載入圖片，縮放至 600x900
        try:
            self.images = [load_image(path, size=(600, 900)) for path in image_paths]
            print(f"Loaded {len(self.images)} images: {image_paths}")  # 除錯
        except Exception as e:
            print(f"Image load error: {e}")
            raise

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.current_page += 1
            print(f"Space pressed, current_page: {self.current_page}")  # 除錯
            if self.current_page >= len(self.image_paths):
                print(f"Switching to {self.next_state}")  # 除錯
                self.game.current_scene.state = self.next_state
                if self.next_state == "dodge_countdown":
                    self.game.current_scene.dodge_countdown_timer = pygame.time.get_ticks()
                elif self.next_state == "attack":
                    self.game.current_scene.attack_start_time = pygame.time.get_ticks()
                    self.game.current_scene.attack_active = False
                self.game.current_scene = self.game.current_scene  # 回到 BattleScene
            else:
                print(f"Showing page {self.current_page + 1}/{len(self.image_paths)}")  # 除錯

    def update(self):
        pass  # 無更新邏輯

    def draw(self, screen):
        screen.fill((240, 205, 0))
        if self.current_page < len(self.images):
            screen.blit(self.images[self.current_page], (0, 0))
            page_text = self.font.render(f"Page {self.current_page + 1}/{len(self.image_paths)}", True, (255, 255, 255))
            screen.blit(page_text, (500, 850))
        else:
            print(f"Warning: current_page {self.current_page} out of range, skipping draw")  # 除錯

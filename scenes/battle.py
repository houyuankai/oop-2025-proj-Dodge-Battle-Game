import pygame
import random
import os

class BattleScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()
        self.dodge_start_time = pygame.time.get_ticks()

        self.player_hp = 3
        self.boss_hp = 5

        self.state = "dodge"  # "dodge", "attack", "transition", "win", "lose"
        
        self.transition_timer = 0
        self.attack_timer = 0

        self.player = pygame.Rect(300, 800, 20, 20)
        self.player_speed = 5

        self.projectiles = []
        self.spawn_delay = 500
        self.last_spawn = pygame.time.get_ticks()

        self.boss_images = [
            pygame.image.load(os.path.join("assets", "images", f"boss_{i}.png")) for i in range(1, 4)
        ]
        self.boss_hit_image = pygame.image.load(os.path.join("assets", "images", "boss_hit.png"))
        self.boss_anim_index = 0
        self.boss_anim_timer = 0

        self.font = pygame.font.SysFont("Arial", 24)
        self.large_font = pygame.font.SysFont("Arial", 72)

        self.previous_state = None

        self.attack_start_time = 0
        self.attack_delay = 2000  # 2 秒
        
        self.attack_bar = pygame.Rect(150, 750, 300, 10)
        self.attack_zone = pygame.Rect(275, 745, 50, 20)
        self.attack_cursor = pygame.Rect(150, 745, 10, 20)
        self.attack_speed = 4
        self.attack_active = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "attack" and event.key == pygame.K_SPACE and self.attack_active:
                self.attack_active = False
                if self.attack_zone.colliderect(self.attack_cursor):
                    self.boss_hp -= 1
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
            
    def update(self):
        if self.state == "dodge":
            self.update_dodge()
        elif self.state == "attack":
            self.update_attack()
        elif self.state == "transition":
            self.transition_timer -= self.clock.get_time()
            if self.transition_timer <= 0:
                if self.boss_hp <= 0:
                    self.state = "win"
                elif self.player_hp <= 0:
                    self.state = "lose"
                else:
                    if self.previous_state == "dodge":
                        self.state = "attack"
                        self.attack_cursor.x = 150
                        self.attack_start_time = pygame.time.get_ticks()
                        self.attack_active = False  # 延遲後才開始動
                    else:
                        self.state = "dodge"
                        self.dodge_start_time = pygame.time.get_ticks()

    def update_dodge(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.player.x -= self.player_speed
        if keys[pygame.K_d]: self.player.x += self.player_speed
        if keys[pygame.K_w]: self.player.y -= self.player_speed
        if keys[pygame.K_s]: self.player.y += self.player_speed

        self.player.clamp_ip(pygame.Rect(0, 300, 600, 600))


        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.spawn_delay:
            self.spawn_projectiles()
            self.last_spawn = now

        for proj in self.projectiles[:]:
            proj["rect"].x += proj["vx"]
            proj["rect"].y += proj["vy"]
            if not pygame.Rect(0, 300, 600, 600).colliderect(proj["rect"]):
                self.projectiles.remove(proj)
            elif self.player.colliderect(proj["rect"]):
                self.player_hp -= 1
                self.projectiles.remove(proj)
                self.state = "transition"
                self.transition_timer = 1000
                return
                
        if pygame.time.get_ticks() - self.dodge_start_time >= 15000:
            self.state = "attack"
            self.attack_cursor.x = 150
            self.attack_active = True
        if pygame.time.get_ticks() - self.dodge_start_time >= 15000:
            self.state = "transition"
            self.transition_timer = 1000
            self.previous_state = "dodge"


    def update_attack(self):
        if not self.attack_active:
            if pygame.time.get_ticks() - self.attack_start_time >= self.attack_delay:
                self.attack_active = True
        else:
            self.attack_cursor.x += self.attack_speed
            if self.attack_cursor.x > 440:
                self.attack_active = False
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
               
    def draw(self, screen):
        screen.fill((100, 100, 100))
        pygame.draw.rect(screen, (0, 0, 0), (0, 300, 600, 600))

        # 顯示血量
        hp_text = self.font.render(f"Your HP: {'❤'*self.player_hp}", True, (255, 255, 255))
        boss_text = self.font.render(f"Boss HP: {'❤'*self.boss_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (20, 20))
        screen.blit(boss_text, (400, 20))

        # 顯示 boss
        if self.state == "transition" and self.boss_hp < 5:
            screen.blit(self.boss_hit_image, (200, 100))
        else:
            if pygame.time.get_ticks() - self.boss_anim_timer > 300:
                self.boss_anim_index = (self.boss_anim_index + 1) % len(self.boss_images)
                self.boss_anim_timer = pygame.time.get_ticks()
            screen.blit(self.boss_images[self.boss_anim_index], (200, 100))

        if self.state == "dodge":
            pygame.draw.ellipse(screen, (255, 200, 0), self.player)
            for proj in self.projectiles:
                pygame.draw.rect(screen, (255, 255, 255), proj["rect"])

        elif self.state == "attack":
            pygame.draw.rect(screen, (255, 255, 255), self.attack_bar)
            pygame.draw.rect(screen, (255, 255, 255), self.attack_zone, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.attack_cursor)

            if not self.attack_active:
                # 顯示倒數秒數
                countdown = max(0, (self.attack_delay - (pygame.time.get_ticks() - self.attack_start_time)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 0))
                screen.blit(countdown_text, (240, 780))
            else:
                press_text = self.font.render("Press SPACE", True, (255, 255, 255))
                screen.blit(press_text, (230, 780))

        elif self.state in ["win", "lose"]:
            result_img = pygame.image.load(os.path.join("assets", "images", f"{self.state}.png"))
            screen.blit(result_img, (0, 0))

    def spawn_projectiles(self):
        dirs = [
            (0, 5), (0, -5), (5, 0), (-5, 0), (5, 5), (-5, -5), (-5, 5), (5, -5)
        ]
        types = random.sample(range(8), 3)
        for t in types:
            vx, vy = dirs[t]
            if vx == 0:
                x = random.choice([100, 300, 500])
                y = 300 if vy > 0 else 880
            elif vy == 0:
                x = 0 if vx > 0 else 580
                y = random.choice([400, 600, 800])
            else:
                x = 0 if vx > 0 else 580
                y = 300 if vy > 0 else 880
            rect = pygame.Rect(x, y, 20, 60)
            self.projectiles.append({"rect": rect, "vx": vx, "vy": vy})

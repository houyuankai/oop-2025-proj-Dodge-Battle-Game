import pygame
import random
import os
import math
from scenes.projectile import Projectile
from scenes.button_manager import ButtonManager

class BattleScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()
        self.dodge_start_time = pygame.time.get_ticks()

        self.player_hp = 3
        self.boss_hp = 5

        self.state = "dodge_countdown"  # "dodge_countdown", "dodge", "attack", "transition", "win", "lose"
        self.dodge_countdown_timer = pygame.time.get_ticks()  # Initialize countdown timer  
        
        self.transition_timer = 0
        self.attack_timer = 0
        self.dodge_countdown_duration = 2000  # 2秒倒數
        
        self.invincible = False  # 新增：無敵狀態標誌
        self.invincible_timer = 0  # 新增：無敵計時器
        self.invincible_duration = 1000  # 新增：無敵0.5秒

        self.player = pygame.Rect(300, 600, 20, 20) # 初始化玩家位置在中央
        self.player_speed = 7

        self.projectiles = []
        self.spawn_delay = 1100
        self.projectile_speed = 4
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
        
        self.attack_bar = pygame.Rect(75, 590, 450, 20)
        self.attack_zone = pygame.Rect(265, 580, 70, 40)
        self.attack_cursor = pygame.Rect(75, 580, 20, 40)
        self.attack_speed = 6
        self.attack_active = False
        
        self.button_manager = ButtonManager(game)

        self.reset_player_position()
        self.projectiles.clear()
        
    def reset_player_position(self):
        # 重置玩家圓球到操作區中央 (300, 600)
        self.player.x = 300
        self.player.y = 600
        
    def reset_game(self):
        self.player_hp = 3
        self.boss_hp = 5
        self.state = "dodge_countdown"
        self.dodge_countdown_timer = pygame.time.get_ticks()
        self.invincible = False
        self.invincible_timer = 0
        self.projectiles.clear()
        self.reset_player_position()
        self.dodge_start_time = pygame.time.get_ticks()
        self.last_spawn = pygame.time.get_ticks()
        self.transition_timer = 0
        self.attack_timer = 0
        self.attack_start_time = 0
        self.attack_active = False
        self.attack_cursor.x = 75
        self.previous_state = None


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "attack" and event.key == pygame.K_SPACE and self.attack_active:
                self.attack_active = False
                if self.attack_zone.colliderect(self.attack_cursor):
                    self.boss_hp -= 1
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
        elif self.state in ["win", "lose"]:
            self.button_manager.handle_event(event, self)
            
    def update(self):
        self.clock.tick(60)
        if self.state == "dodge":
            self.update_dodge()
        elif self.state == "dodge_countdown":  # 確保倒數狀態被處理
            self.update_dodge_countdown()
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
                        self.attack_cursor.x = 75
                        self.attack_start_time = pygame.time.get_ticks()
                        self.attack_active = False  # 延遲後才開始動
                    else:
                        self.state = "dodge_countdown"  # 改為進入倒數狀態
                        self.dodge_countdown_timer = pygame.time.get_ticks()
                        self.reset_player_position()  # 重置玩家位置
                        self.projectiles.clear()  # 清除現有障礙物
    def update_dodge_countdown(self):
        # 倒數計時邏輯
        elapsed = pygame.time.get_ticks() - self.dodge_countdown_timer
        if elapsed >= self.dodge_countdown_duration:
            self.state = "dodge"
            self.dodge_start_time = pygame.time.get_ticks()
            self.last_spawn = pygame.time.get_ticks()

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

        # 檢查無敵狀態
        if self.invincible:
            if now - self.invincible_timer > self.invincible_duration:
                self.invincible = False  # 結束無敵狀態

        for proj in self.projectiles[:]:
            proj.rect.x += proj.vx
            proj.rect.y += proj.vy
            if not pygame.Rect(0, 300, 600, 600).colliderect(proj.rect):
                self.projectiles.remove(proj)
            elif self.player.colliderect(proj.rect) and not self.invincible:  # 修改：僅在非無敵時受傷
                self.player_hp -= 1
                self.projectiles.remove(proj)
                self.invincible = True  # 進入無敵狀態
                self.invincible_timer = now  # 記錄無敵開始時間
                if self.player_hp <= 0:  # 新增：檢查血量是否為0
                    self.state = "transition"
                    self.transition_timer = 1000
                    self.previous_state = "dodge"
                    return
                
        if pygame.time.get_ticks() - self.dodge_start_time >= 10000:
            self.state = "transition"
            self.transition_timer = 1000
            self.previous_state = "dodge"
            


    def update_attack(self):
        if not self.attack_active:
            if pygame.time.get_ticks() - self.attack_start_time >= self.attack_delay:
                self.attack_active = True
        else:
            self.attack_cursor.x += self.attack_speed
            if self.attack_cursor.x > 505:
                self.attack_active = False
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
               
    def draw(self, screen):
        screen.fill((240, 205, 0))
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

        if self.state == "dodge" or self.state == "dodge_countdown":
            player_color = (0, 255, 255) if self.invincible else (255, 200, 0)
            pygame.draw.ellipse(screen, player_color, self.player)
            for proj in self.projectiles:
                rotated_rect = proj.surface.get_rect(center=proj.rect.center)
                screen.blit(proj.surface, rotated_rect)
            if self.state == "dodge_countdown":
                # 顯示倒數秒數
                countdown = max(0, (self.dodge_countdown_duration - (pygame.time.get_ticks() - self.dodge_countdown_timer)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 0))
                screen.blit(countdown_text, (240, 680))


        elif self.state == "attack":
            pygame.draw.rect(screen, (255, 255, 255), self.attack_bar)
            pygame.draw.rect(screen, (255, 255, 255), self.attack_zone, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.attack_cursor)

            if not self.attack_active:
                # 顯示倒數秒數
                countdown = max(0, (self.attack_delay - (pygame.time.get_ticks() - self.attack_start_time)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 0))
                screen.blit(countdown_text, (240, 680))
            else:
                press_text = self.font.render("Press SPACE", True, (255, 255, 255))
                screen.blit(press_text, (230, 680))

        elif self.state in ["win", "lose"]:
            result_img = pygame.image.load(os.path.join("assets", "images", f"{self.state}.png"))
            screen.blit(result_img, (0, 0))
            self.button_manager.draw(screen)

    def spawn_projectiles(self):
        dirs = [
            (0, self.projectile_speed), (0, -self.projectile_speed),
            (self.projectile_speed, 0), (-self.projectile_speed, 0),
            (self.projectile_speed/1.4, self.projectile_speed/1.4), (-self.projectile_speed/1.4, -self.projectile_speed/1.4),
            (-self.projectile_speed/1.4, self.projectile_speed/1.4), (self.projectile_speed/1.4, -self.projectile_speed/1.4)
        ]
        angles = [0, 0, 0, 0, -45, -45, 45, 45]
        types = random.sample(range(8), random.randint(1, 3))
        for t in types:
            vx, vy = dirs[t]
            angle = angles[t]
            if vx == 0:
                x = random.choice([100, 300, 500])
                y = 300 if vy > 0 else 880
                rect = pygame.Rect(x-100, y, 200, 20)
            elif vy == 0:
                x = 0 if vx > 0 else 580
                y = random.choice([400, 600, 800])
                rect = pygame.Rect(x, y-100, 20, 200)
            else:
                x = 0 if vx > 0 else 580
                y = 300 if vy > 0 else 880
                rect = pygame.Rect(x, y, 20, 200)
            self.projectiles.append(Projectile(rect, vx, vy, angle))

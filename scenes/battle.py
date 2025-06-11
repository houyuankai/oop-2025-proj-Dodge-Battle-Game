import pygame
import random
import os
import math
from scenes.projectile import Projectile
from scenes.button_manager import ButtonManager
from scenes.utils import load_image

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
        self.spawn_delay = 1000
        self.projectile_speed = 5
        self.last_spawn = pygame.time.get_ticks()
        

        self.boss_images = [
            load_image(os.path.join("assets", "images", f"boss_{i}.png"), size=(200, 200)) for i in range(1, 4)
        ]
        self.boss_hit_image = load_image(os.path.join("assets", "images", "boss_hit.png"), size=(200, 200))
        self.boss_anim_index = 0
        self.boss_anim_timer = 0
        self.boss_hit = False
        
         # 新增：載入愛心圖片
        self.heart_image = load_image(os.path.join("assets", "images", "heart.png"), size=(25, 25))
        
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.miss_font = pygame.font.SysFont("Arial", 30, bold=True)  # 為 Miss 設置粗體


        self.previous_state = None

        self.attack_start_time = 0
        self.attack_delay = 2000  # 2 秒
        
        self.attack_bar = pygame.Rect(75, 590, 450, 20)
        self.attack_zone = pygame.Rect(265, 580, 70, 40)
        self.attack_cursor = pygame.Rect(75, 580, 20, 40)
        self.attack_speed = 8
        self.attack_active = False

        # 新增：Miss 文字顯示控制
        self.miss_display = False
        self.miss_timer = 0
        self.miss_duration = 1500  # 1.5 秒
        
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
        self.boss_hit = False
        self.miss_display = False
        self.miss_timer = 0


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "attack" and event.key == pygame.K_SPACE and self.attack_active:
                self.attack_active = False
                if self.attack_zone.colliderect(self.attack_cursor):
                    self.boss_hp -= 1
                    self.boss_hit = True
                    self.miss_display = False
                else:
                    self.boss_hit = False
                    self.miss_display = True
                    self.miss_timer = pygame.time.get_ticks()  # 新增：記錄 Miss 時間
                    print("Miss due to space press outside attack zone")  # 除錯
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
                        if self.previous_state == "dodge":
                            self.state = "attack"
                            self.attack_cursor.x = 75
                            self.attack_start_time = pygame.time.get_ticks()
                            self.attack_active = False
                        else:
                            self.state = "dodge_countdown"
                            self.boss_hit = False
                            self.miss_display = False
                            self.miss_timer = 0
                            self.dodge_countdown_timer = pygame.time.get_ticks()
                            self.reset_player_position()
                            self.projectiles.clear()
            # 更新 Miss 顯示
        if self.miss_display:
            print(f"Miss display active, time left: {self.miss_duration - (pygame.time.get_ticks() - self.miss_timer)}")
            if pygame.time.get_ticks() - self.miss_timer > self.miss_duration:
                self.miss_display = False

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
                self.boss_hit = False
                self.miss_display = True
                self.miss_timer = pygame.time.get_ticks()  # 新增：記錄 Miss 時間
                self.attack_active = False
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
                print("Miss due to cursor overshoot") 
               
    def draw(self, screen):
        screen.fill((240, 205, 0))
        
        # 顯示血量
        # 修改：使用愛心圖片表示生命值
        hp_text = self.font.render("Your HP :", True, (255, 255, 255))
        boss_text = self.font.render("Boss HP :", True, (255, 255, 255))
        
        screen.blit(hp_text, (20, 20))
        screen.blit(boss_text, (350, 20))
        for i in range(self.player_hp):
            screen.blit(self.heart_image, (140 + i * 25, 20))  # 間距 5 像素
        for i in range(self.boss_hp):
            screen.blit(self.heart_image, (460 + i * 25, 20))  # 間距 5 像素

        if self.state == "transition" and self.boss_hit:
            screen.blit(self.boss_hit_image, (200, 100))
        else:
            if pygame.time.get_ticks() - self.boss_anim_timer > 300:
                self.boss_anim_index = (self.boss_anim_index + 1) % len(self.boss_images)
                self.boss_anim_timer = pygame.time.get_ticks()
            screen.blit(self.boss_images[self.boss_anim_index], (200, 100))
        # 顯示 boss
        
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
            # 新增：顯示 Miss 文字

        elif self.state in ["win", "lose"]:
            result_img = load_image(os.path.join("assets", "images", f"{self.state}.png"), size=(600, 900))
            screen.blit(result_img, (0, 0))
            self.button_manager.draw(screen)
            
        pygame.draw.rect(screen, (0, 0, 0), (0, 300, 600, 600))
        # 最後繪製 Miss 文字，確保不被覆蓋
        if self.miss_display:
            print("Drawing Miss text")  # 除錯
            miss_rect = self.miss_font.render("Miss", True, (255, 0, 0)).get_rect(center=(300, 500))
            pygame.draw.rect(screen, (0, 0, 255), miss_rect.inflate(10, 10))  # 放大藍色背景
            miss_text = self.miss_font.render("Miss", True, (255, 0, 0))
            screen.blit(miss_text, miss_rect)
            print(f"Miss text rect: {miss_rect}")  # 除錯

    def spawn_projectiles(self):
        dirs = [
            (0, self.projectile_speed), (0, -self.projectile_speed),
            (self.projectile_speed, 0), (-self.projectile_speed, 0),
            (self.projectile_speed/1.4, self.projectile_speed/1.4), (-self.projectile_speed/1.4, -self.projectile_speed/1.4),
            (-self.projectile_speed/1.4, self.projectile_speed/1.4), (self.projectile_speed/1.4, -self.projectile_speed/1.4)
        ]
        angles = [0, 0, 0, 0, -45, -45, 45, 45]
        types = random.sample(range(8), random.randint(1, 2))
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

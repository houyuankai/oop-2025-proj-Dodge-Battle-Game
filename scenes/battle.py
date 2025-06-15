import pygame
import random
import os
import math
from scenes.projectile import Projectile
from scenes.button_manager import ButtonManager
from scenes.utils import load_image
from scenes.instruction import InstructionScene
from scenes.window import Window
from scenes.item import Item

class BattleScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()
        self.dodge_start_time = pygame.time.get_ticks()

        # 預載入物件圖片
        Item.preload_images()

        self.player_hp = 3
        self.boss_hp = 5

        self.state = "instruction"
        self.dodge_countdown_timer = pygame.time.get_ticks()
        
        self.transition_timer = 0
        self.attack_timer = 0
        self.dodge_countdown_duration = 2000
        
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1700  # 1.7 秒

        self.player = pygame.Rect(300, 600, 20, 20)
        self.player_speed = 7

        self.projectiles = []
        self.spawn_delay = 1000
        self.projectile_speed = 5
        self.last_spawn = pygame.time.get_ticks()
        
        self.boss_images = [
            load_image(os.path.join("assets", "images", f"boss_{i}.png"), size=(180, 270)) for i in range(1, 9)
        ]
        self.boss_hit_image = load_image(os.path.join("assets", "images", "boss_hit.png"), size=(600, 250))
        self.boss_anim_index = 0
        self.boss_anim_timer = 0
        self.boss_hit = False
        
        self.heart_image = load_image(os.path.join("assets", "images", "heart.png"), size=(25, 25))
        
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 72, bold=True)

        self.previous_state = None

        self.attack_start_time = 0
        self.attack_delay = 2000
        
        self.attack_bar = pygame.Rect(75, 590, 450, 20)
        self.attack_zone = pygame.Rect(265, 580, 70, 40)
        self.attack_cursor = pygame.Rect(75, 580, 20, 40)
        self.attack_speed = 8
        self.attack_active = False
        
        self.button_manager = ButtonManager(game)

        self.first_dodge = True
        self.first_attack = True

        self.dodge_pages = [
            os.path.join("assets", "images", "instruction_dodge1.png"),
            os.path.join("assets", "images", "instruction_dodge2.png"),
            os.path.join("assets", "images", "instruction_dodge3.png")
        ]
        self.attack_pages = [
            os.path.join("assets", "images", "instruction_attack1.png"),
            os.path.join("assets", "images", "instruction_attack2.png")
        ]

        self.windows = []
        self.window_spawn_timer = 0
        self.window_spawn_interval = 300

        self.items = []
        self.item_spawn_timer = 0
        self.item_spawn_interval = 1500
        self.item3_count = 0
        self.item4_count = 0

        self.ending_images = {
            "win": load_image(os.path.join("assets", "images", "win.png"), size=(600, 900)),
            "lose": load_image(os.path.join("assets", "images", "lose.png"), size=(600, 900)),
            "ending3": load_image(os.path.join("assets", "images", "ending3.png"), size=(600, 900)),
            "ending4": load_image(os.path.join("assets", "images", "ending4.png"), size=(600, 900))
        }

        self.reset_player_position()
        self.projectiles.clear()
        self.items.clear()
        
        self.current_music = None
        self.music_paths = {
            "dodge": os.path.join("assets", "sounds", "music_2.mp3"),
            "win": os.path.join("assets", "sounds", "music_4.mp3"),
            "lose": os.path.join("assets", "sounds", "music_3.mp3"),
            "ending3": os.path.join("assets", "sounds", "music_e3.mp3"),
            "ending4": os.path.join("assets", "sounds", "music_e4.mp3")
        }
        pygame.mixer.music.set_volume(1.0)

    def reset_player_position(self):
        self.player.x = 300
        self.player.y = 600
        
    def reset_game(self):
        self.player_hp = 3
        self.boss_hp = 5
        self.state = "instruction"
        self.dodge_countdown_timer = pygame.time.get_ticks()
        self.invincible = False
        self.invincible_timer = 0
        self.projectiles.clear()
        self.items.clear()
        self.windows.clear()
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
        self.first_dodge = True
        self.first_attack = True
        self.window_spawn_timer = 0
        self.item_spawn_timer = 0
        self.item3_count = 0
        self.item4_count = 0
        pygame.mixer.music.stop()
        self.current_music = None
        self.game.current_music = None

    def handle_event(self, event):
        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            if event.type == pygame.KEYDOWN:
                if self.state == "attack" and event.key == pygame.K_SPACE and self.attack_active:
                    self.attack_active = False
                    if self.attack_zone.colliderect(self.attack_cursor):
                        self.boss_hp -= 1
                        self.boss_hit = True
                    else:
                        self.boss_hit = False
                    self.state = "transition"
                    self.transition_timer = 1000
                    self.previous_state = "attack"
        elif self.state in ["win", "lose", "ending3", "ending4"]:
            self.button_manager.handle_event(event, self)

    def update_music(self):
        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            if self.current_music != self.music_paths["dodge"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["dodge"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["dodge"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_2.mp3: {e}")
        elif self.state == "instruction":
            if self.current_music is not None:
                pygame.mixer.music.stop()
                self.current_music = None
                self.game.current_music = None
        elif self.state == "win":
            if self.current_music != self.music_paths["win"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["win"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["win"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_4.mp3: {e}")
        elif self.state == "lose":
            if self.current_music != self.music_paths["lose"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["lose"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["lose"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_3.mp3: {e}")
        elif self.state == "ending3":
            if self.current_music != self.music_paths["ending3"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["ending3"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["ending3"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_e3.mp3: {e}")
        elif self.state == "ending4":
            if self.current_music != self.music_paths["ending4"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["ending4"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["ending4"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_e4.mp3: {e}")

    def update(self):
        dt = self.clock.tick(60) / 16.67
        self.update_music()

        if self.state == "instruction":
            if self.first_dodge:
                self.game.change_scene(InstructionScene(self.game, self.dodge_pages, "dodge_countdown", self))
                self.first_dodge = False
            elif self.first_attack:
                self.game.change_scene(InstructionScene(self.game, self.attack_pages, "attack", self))
                self.first_attack = False
        elif self.state == "dodge":
            self.update_dodge()
        elif self.state == "dodge_countdown":
            self.update_dodge_countdown()
        elif self.state == "attack":
            self.update_attack()
        elif self.state == "transition":
            self.transition_timer -= self.clock.get_time()
            if self.transition_timer <= 0:
                self.items.clear()
                if self.boss_hp <= 0:
                    self.state = "win"
                elif self.player_hp <= 0:
                    self.state = "lose"
                else:
                    if self.previous_state == "dodge":
                        self.state = "instruction" if self.first_attack else "attack"
                        self.attack_cursor.x = 75
                        self.attack_start_time = pygame.time.get_ticks()
                        self.attack_active = False
                    else:
                        self.state = "dodge_countdown"
                        self.boss_hit = False
                        self.dodge_countdown_timer = pygame.time.get_ticks()
                        self.reset_player_position()
                        self.projectiles.clear()

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            self.window_spawn_timer += self.clock.get_time()
            if self.window_spawn_timer >= self.window_spawn_interval:
                self.windows.append(Window(0, 150, 300, 150, width=20, height=160))
                self.windows.append(Window(600, 150, 300, 150, width=20, height=160))
                self.window_spawn_timer = 0
            for window in self.windows[:]:
                if window.update(dt):
                    self.windows.remove(window)

    def update_dodge_countdown(self):
        current_ticks = pygame.time.get_ticks()
        elapsed = current_ticks - self.dodge_countdown_timer
        if elapsed >= self.dodge_countdown_duration:
            self.state = "dodge"
            self.dodge_start_time = current_ticks
            self.last_spawn = current_ticks
            self.item_spawn_timer = current_ticks
        if self.current_music != self.music_paths["dodge"]:
            self.update_music()

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

        if now - self.item_spawn_timer >= self.item_spawn_interval:
            if len(self.items) < 2:
                r = random.random()
                x = random.randint(50, 550)
                y = random.randint(350, 850)
                if r < 0.18:  # 18% item1
                    self.items.append(Item(x, y, "item1"))
                elif r < 0.38:  # 20% item2
                    self.items.append(Item(x, y, "item2"))
                elif r < 0.54:  # 16% item3
                    self.items.append(Item(x, y, "item3"))
                elif r < 0.68:  # 10% item4
                    self.items.append(Item(x, y, "item4"))
            self.item_spawn_timer = now

        for item in self.items[:]:
            if now - item.spawn_time > item.lifetime:
                self.items.remove(item)
                continue
            if self.player.colliderect(item.rect):
                self.items.remove(item)
                if item.item_type == "item1":
                    if self.player_hp < 3:
                        self.player_hp += 1
                elif item.item_type == "item2":
                    self.invincible = True
                    self.invincible_timer = now
                elif item.item_type == "item3":
                    if self.boss_hp < 5:
                        self.boss_hp += 1
                    self.item3_count += 1
                    if self.item3_count >= 7:  # 結局三
                        self.state = "ending3"
                        self.items.clear()
                        self.update_music()
                        break
                elif item.item_type == "item4":
                    self.item4_count += 1
                    if self.item4_count >= 5:  # 結局四
                        self.state = "ending4"
                        self.items.clear()
                        self.update_music()
                        break
                continue

        if self.invincible:
            if now - self.invincible_timer > self.invincible_duration:
                self.invincible = False

        for proj in self.projectiles[:]:
            proj.rect.x += proj.vx
            proj.rect.y += proj.vy
            if not pygame.Rect(0, 300, 600, 600).colliderect(proj.rect):
                self.projectiles.remove(proj)
            elif self.player.colliderect(proj.rect) and not self.invincible:
                self.player_hp -= 1
                self.projectiles.remove(proj)
                self.invincible = True
                self.invincible_timer = now
                if self.player_hp <= 0:
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
                self.attack_active = False
                self.state = "transition"
                self.transition_timer = 1000
                self.previous_state = "attack"
        if self.current_music != self.music_paths["dodge"]:
            self.update_music()

    def draw(self, screen):
        if self.boss_hp <= 2:
            screen.fill((255, 0, 0))
        else:
            screen.fill((240, 205, 0))
        
        pygame.draw.rect(screen, (0, 0, 0), (0, 300, 600, 600))

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            pygame.draw.line(screen, (100, 100, 100), (0, 0), (600, 300), 2)
            pygame.draw.line(screen, (100, 100, 100), (600, 0), (0, 300), 2)

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            for window in self.windows:
                window.draw(screen)

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 600, 50))

        if self.boss_hit and self.state == "transition":
            screen.blit(self.boss_hit_image, (0, 50))
        else:
            if pygame.time.get_ticks() - self.boss_anim_timer > 300:
                self.boss_anim_index = (self.boss_anim_index + 1) % len(self.boss_images)
                self.boss_anim_timer = pygame.time.get_ticks()
            screen.blit(self.boss_images[self.boss_anim_index], (210, 30))

        hp_text = self.font.render("Your HP :", True, (255, 255, 255))
        boss_text = self.font.render("Boss HP :", True, (255, 255, 255))
        screen.blit(hp_text, (20, 10))
        screen.blit(boss_text, (350, 10))
        for i in range(self.player_hp):
            screen.blit(self.heart_image, (140 + i * 25, 10))
        for i in range(self.boss_hp):
            screen.blit(self.heart_image, (460 + i * 25, 10))

        if self.state in ["dodge", "dodge_countdown"]:
            player_color = (0, 255, 255) if self.invincible else (255, 200, 0)
            pygame.draw.ellipse(screen, player_color, self.player)
            for proj in self.projectiles:
                rotated_rect = proj.surface.get_rect(center=proj.rect.center)
                screen.blit(proj.surface, rotated_rect)
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            if self.state == "dodge_countdown":
                countdown = max(0, (self.dodge_countdown_duration - (pygame.time.get_ticks() - self.dodge_countdown_timer)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 255))
                screen.blit(countdown_text, (240, 680))

        elif self.state == "attack":
            pygame.draw.rect(screen, (255, 255, 255), self.attack_bar)
            pygame.draw.rect(screen, (255, 255, 255), self.attack_zone, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.attack_cursor)
            if not self.attack_active:
                countdown = max(0, (self.attack_delay - (pygame.time.get_ticks() - self.attack_start_time)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 255))
                screen.blit(countdown_text, (240, 680))
            else:
                press_text = self.font.render("Press SPACE", True, (255, 255, 255))
                screen.blit(press_text, (230, 680))

        elif self.state in ["win", "lose", "ending3", "ending4"]:
            screen.blit(self.ending_images[self.state], (0, 0))
            self.button_manager.draw(screen)

    def spawn_projectiles(self):
        dirs = [
            (0, self.projectile_speed), (0, -self.projectile_speed),
            (self.projectile_speed, 0), (-self.projectile_speed, 0),
            (self.projectile_speed/1.4, self.projectile_speed/1.4),
            (-self.projectile_speed/1.4, -self.projectile_speed/1.4),
            (-self.projectile_speed/1.4, self.projectile_speed/1.4),
            (self.projectile_speed/1.4, -self.projectile_speed/1.4)
        ]
        angles = [0, 180, 90, -90, 45, -135, 135, -45]
        count = random.randint(2, 3) if self.boss_hp <= 2 else random.randint(1, 2)
        types = random.sample(range(8), count)
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

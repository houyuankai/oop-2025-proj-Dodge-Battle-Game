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
        self.scale = game.scale  # 從 Game 獲取縮放比例

        Item.preload_images(self.scale)

        self.player_hp = 3
        self.boss_hp = 5

        self.state = "instruction"
        self.dodge_countdown_timer = pygame.time.get_ticks()
        
        self.transition_timer = 0
        self.attack_timer = 0
        self.dodge_countdown_duration = 2000
        
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1700

        # 縮放玩家
        self.player = pygame.Rect(300 * self.scale, 600 * self.scale, 20 * self.scale, 20 * self.scale)
        self.player_speed = 7 * self.scale

        self.projectiles = []
        self.spawn_delay = 1000
        self.projectile_speed = 5 * self.scale
        self.last_spawn = pygame.time.get_ticks()
        
        # 縮放 Boss 圖片
        self.boss_images = [
            load_image(os.path.join("assets", "images", f"boss_{i}.png"), size=(180 * self.scale, 270 * self.scale)) for i in range(1, 9)
        ]
        self.boss_hit_image = load_image(os.path.join("assets", "images", "boss_hit.png"), size=(600 * self.scale, 250 * self.scale))
        self.boss_anim_index = 0
        self.boss_anim_timer = 0
        self.boss_hit = False
        
        self.heart_image = load_image(os.path.join("assets", "images", "heart.png"), size=(25 * self.scale, 25 * self.scale))
        
        self.font = pygame.font.SysFont("Arial", int(24 * self.scale), bold=True)
        self.large_font = pygame.font.SysFont("Arial", int(72 * self.scale), bold=True)

        self.previous_state = None

        self.attack_start_time = 0
        self.attack_delay = 2000
        
        # 縮放攻擊條
        self.attack_bar = pygame.Rect(75 * self.scale, 590 * self.scale, 450 * self.scale, 20 * self.scale)
        self.attack_zone = pygame.Rect(265 * self.scale, 580 * self.scale, 70 * self.scale, 40 * self.scale)
        self.attack_cursor = pygame.Rect(75 * self.scale, 580 * self.scale, 20 * self.scale, 40 * self.scale)
        self.attack_speed = 8 * self.scale
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
        self.key1_count = 0
        self.key2_count = 0
        self.key3_count = 0

        # 縮放結局圖片
        self.ending_images = {
            "win": load_image(os.path.join("assets", "images", "win.png"), size=(600 * self.scale, 900 * self.scale)),
            "lose": load_image(os.path.join("assets", "images", "lose.png"), size=(600 * self.scale, 900 * self.scale)),
            "ending3": load_image(os.path.join("assets", "images", "ending3.png"), size=(600 * self.scale, 900 * self.scale)),
            "ending4": load_image(os.path.join("assets", "images", "ending4.png"), size=(600 * self.scale, 900 * self.scale)),
            "ending5": load_image(os.path.join("assets", "images", "ending5.png"), size=(600 * self.scale, 900 * self.scale))
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
            "ending4": os.path.join("assets", "sounds", "music_e4.mp3"),
            "ending5": os.path.join("assets", "sounds", "music_e5.mp3")
        }
        pygame.mixer.music.set_volume(1.0)

    def reset_player_position(self):
        self.player.x = 300 * self.scale
        self.player.y = 600 * self.scale
        
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
        self.attack_cursor.x = 75 * self.scale
        self.previous_state = None
        self.boss_hit = False
        self.first_dodge = True
        self.first_attack = True
        self.window_spawn_timer = 0
        self.item_spawn_timer = 0
        self.item3_count = 0
        self.item4_count = 0
        self.key1_count = 0
        self.key2_count = 0
        self.key3_count = 0
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
        elif self.state in ["win", "lose", "ending3", "ending4", "ending5"]:
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
        elif self.state == "ending5":
            if self.current_music != self.music_paths["ending5"]:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(self.music_paths["ending5"])
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                    self.current_music = self.music_paths["ending5"]
                    self.game.current_music = self.current_music
                except pygame.error as e:
                    print(f"Failed to load music_e5.mp3: {e}")

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
                        self.attack_cursor.x = 75 * self.scale
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
                self.windows.append(Window(0, 150 * self.scale, 300 * self.scale, 150 * self.scale, width=20 * self.scale, height=160 * self.scale, scale=self.scale))
                self.windows.append(Window(600 * self.scale, 150 * self.scale, 300 * self.scale, 150 * self.scale, width=20 * self.scale, height=160 * self.scale, scale=self.scale))
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

        self.player.clamp_ip(pygame.Rect(0, 300 * self.scale, 600 * self.scale, 600 * self.scale))

        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.spawn_delay:
            self.spawn_projectiles()
            self.last_spawn = now

        if now - self.item_spawn_timer >= self.item_spawn_interval:
            if len(self.items) < 3:
                r = random.random()
                x1 = random.randint(50 * self.scale, 550 * self.scale)
                y1 = random.randint(350 * self.scale, 850 * self.scale)
                if r < 0.18:  # 18% item1
                    self.items.append(Item(x1, y1, "item1"))
                elif r < 0.38:  # 20% item2
                    self.items.append(Item(x1, y1, "item2"))
                elif r < 0.52:  # 14% item3
                    self.items.append(Item(x1, y1, "item3"))
                elif r < 0.62:  # 10% item4
                    self.items.append(Item(x1, y1, "item4"))
                if self.boss_hp in [1, 2]:
                    r2 = random.random()
                    x2 = random.randint(50 * self.scale, 550 * self.scale)
                    y2 = random.randint(350 * self.scale, 850 * self.scale)
                    while len(self.items) > 0 and math.hypot(x2 - x1, y2 - y1) < 50 * self.scale:
                        x2 = random.randint(50 * self.scale, 550 * self.scale)
                        y2 = random.randint(350 * self.scale, 850 * self.scale)
                    if r2 < 0.08:  # 8% key1
                        self.items.append(Item(x2, y2, "key1"))
                    elif r2 < 0.16:  # 8% key2
                        self.items.append(Item(x2, y2, "key2"))
                    elif r2 < 0.24:  # 8% key3
                        self.items.append(Item(x2, y2, "key3"))
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
                    if self.item4_count >= 4:  # 結局四
                        self.state = "ending4"
                        self.items.clear()
                        self.update_music()
                        break
                elif item.item_type == "key1":
                    self.key1_count += 1
                elif item.item_type == "key2":
                    self.key2_count += 1
                elif item.item_type == "key3":
                    self.key3_count += 1
                if self.key1_count >= 1 and self.key2_count >= 1 and self.key3_count >= 1:  # 結局五
                    self.state = "ending5"
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
            if not pygame.Rect(0, 300 * self.scale, 600 * self.scale, 600 * self.scale).colliderect(proj.rect):
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
            if self.attack_cursor.x > 505 * self.scale:
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
        
        pygame.draw.rect(screen, (0, 0, 0), (0, 300 * self.scale, 600 * self.scale, 600 * self.scale))

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            pygame.draw.line(screen, (100, 100, 100), (0, 0), (600 * self.scale, 300 * self.scale), 2)
            pygame.draw.line(screen, (100, 100, 100), (600 * self.scale, 0), (0, 300 * self.scale), 2)

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            for window in self.windows:
                window.draw(screen)

        if self.state in ["dodge", "dodge_countdown", "attack", "transition"]:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 600 * self.scale, 50 * self.scale))

        if self.boss_hit and self.state == "transition":
            screen.blit(self.boss_hit_image, (0, 50 * self.scale))
        else:
            if pygame.time.get_ticks() - self.boss_anim_timer > 300:
                self.boss_anim_index = (self.boss_anim_index + 1) % len(self.boss_images)
                self.boss_anim_timer = pygame.time.get_ticks()
            screen.blit(self.boss_images[self.boss_anim_index], (210 * self.scale, 30 * self.scale))

        hp_text = self.font.render("Your HP :", True, (255, 255, 255))
        boss_text = self.font.render("Boss HP :", True, (255, 255, 255))
        screen.blit(hp_text, (20 * self.scale, 10 * self.scale))
        screen.blit(boss_text, (350 * self.scale, 10 * self.scale))
        for i in range(self.player_hp):
            screen.blit(self.heart_image, (140 * self.scale + i * 25 * self.scale, 10 * self.scale))
        for i in range(self.boss_hp):
            screen.blit(self.heart_image, (460 * self.scale + i * 25 * self.scale, 10 * self.scale))

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
                screen.blit(countdown_text, (240 * self.scale, 680 * self.scale))

        elif self.state == "attack":
            pygame.draw.rect(screen, (255, 255, 255), self.attack_bar)
            pygame.draw.rect(screen, (255, 255, 255), self.attack_zone, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.attack_cursor)
            if not self.attack_active:
                countdown = max(0, (self.attack_delay - (pygame.time.get_ticks() - self.attack_start_time)) // 1000 + 1)
                countdown_text = self.font.render(f"Ready in: {countdown}", True, (255, 255, 255))
                screen.blit(countdown_text, (240 * self.scale, 680 * self.scale))
            else:
                press_text = self.font.render("Press SPACE", True, (255, 255, 255))
                screen.blit(press_text, (230 * self.scale, 680 * self.scale))

        elif self.state in ["win", "lose", "ending3", "ending4", "ending5"]:
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
                x = random.choice([100 * self.scale, 300 * self.scale, 500 * self.scale])
                y = 300 * self.scale if vy > 0 else 880 * self.scale
                rect = pygame.Rect(x - 100 * self.scale, y, 200 * self.scale, 20 * self.scale)
            elif vy == 0:
                x = 0 if vx > 0 else 580 * self.scale
                y = random.choice([400 * self.scale, 600 * self.scale, 800 * self.scale])
                rect = pygame.Rect(x, y - 100 * self.scale, 20 * self.scale, 200 * self.scale)
            else:
                x = 0 if vx > 0 else 580 * self.scale
                y = 300 * self.scale if vy > 0 else 880 * self.scale
                rect = pygame.Rect(x, y, 20 * self.scale, 200 * self.scale)
            self.projectiles.append(Projectile(rect, vx, vy, angle))

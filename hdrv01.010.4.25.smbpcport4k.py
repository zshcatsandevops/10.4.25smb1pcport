import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
RUN_SPEED = 7

# SMB3 Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MARIO_RED = (228, 0, 88)
MARIO_BLUE = (0, 88, 248)
DARK_ORANGE = (216, 40, 0)
LIGHT_ORANGE = (248, 148, 88)
BROWN = (136, 20, 0)
BRICK_ORANGE = (248, 88, 0)
COIN_GOLD = (252, 188, 0)
PIPE_GREEN = (0, 168, 0)
DARK_GREEN = (0, 120, 0)
SKY_BLUE = (92, 148, 252)
CLOUD_WHITE = (248, 248, 248)
GROUND_BROWN = (188, 116, 56)
UNDERGROUND_BLUE = (0, 0, 168)
MUSHROOM_RED = (248, 56, 0)
SHELL_GREEN = (0, 184, 0)

# Power-up Types
POWERUP_MUSHROOM = 0
POWERUP_FIRE_FLOWER = 1
POWERUP_LEAF = 2

# Game States
TITLE_SCREEN = 0
WORLD_MAP = 1
PLAYING = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4
GAME_WIN = 5

# Player States
SMALL_MARIO = 0
SUPER_MARIO = 1
FIRE_MARIO = 2
RACCOON_MARIO = 3

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = random.randint(-3, 3)
        self.vel_y = random.randint(-8, -3)
        self.lifetime = 30
        
    def update(self):
        self.vel_y += 0.5
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((12, 12))
        pygame.draw.circle(self.image, BRICK_ORANGE, (6, 6), 6)
        pygame.draw.circle(self.image, COIN_GOLD, (6, 6), 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 8 * direction
        self.vel_y = 0
        self.bounces = 0
        
    def update(self, platforms):
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Check platform collision for bouncing
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = -8
                self.bounces += 1
                
        if self.bounces > 4 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.state = SMALL_MARIO
        self.image = pygame.Surface((32, 32))
        self.update_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.lives = 5
        self.score = 0
        self.coins = 0
        self.running = False
        self.facing_right = True
        self.invincible_timer = 0
        self.fly_timer = 0
        self.p_meter = 0  # SMB3 P-Meter for flying
        self.can_shoot = False
        
    def update_sprite(self):
        """Update sprite based on power-up state (SMB3 style)"""
        self.image.fill((0, 0, 0, 0))
        
        if self.state == SMALL_MARIO:
            # Small Mario - simple red/blue sprite
            pygame.draw.rect(self.image, MARIO_RED, (8, 12, 16, 12))  # Body
            pygame.draw.rect(self.image, MARIO_BLUE, (10, 8, 12, 8))  # Overalls
            pygame.draw.circle(self.image, (255, 200, 150), (16, 8), 6)  # Head
        elif self.state == SUPER_MARIO:
            # Super Mario - taller sprite
            pygame.draw.rect(self.image, MARIO_RED, (8, 8, 16, 16))  # Body
            pygame.draw.rect(self.image, MARIO_BLUE, (10, 4, 12, 12))  # Overalls
            pygame.draw.circle(self.image, (255, 200, 150), (16, 6), 6)  # Head
        elif self.state == FIRE_MARIO:
            # Fire Mario - white/red colors
            pygame.draw.rect(self.image, WHITE, (8, 8, 16, 16))  # White body
            pygame.draw.rect(self.image, MARIO_RED, (10, 4, 12, 12))  # Red overalls
            pygame.draw.circle(self.image, (255, 200, 150), (16, 6), 6)  # Head
            # Fire effect
            pygame.draw.circle(self.image, BRICK_ORANGE, (24, 20), 4)
        elif self.state == RACCOON_MARIO:
            # Raccoon Mario - with tail and ears
            pygame.draw.rect(self.image, BROWN, (8, 8, 16, 16))  # Brown body
            pygame.draw.rect(self.image, MARIO_BLUE, (10, 4, 12, 12))  # Overalls
            pygame.draw.circle(self.image, (255, 200, 150), (16, 6), 6)  # Head
            # Raccoon tail
            pygame.draw.circle(self.image, BROWN, (4, 24), 6)
            pygame.draw.circle(self.image, BLACK, (4, 24), 3)
            # Ears
            pygame.draw.circle(self.image, BROWN, (12, 2), 3)
            pygame.draw.circle(self.image, BROWN, (20, 2), 3)
        
    def shoot_fireball(self, fireballs):
        if self.state == FIRE_MARIO and self.can_shoot:
            direction = 1 if self.facing_right else -1
            fireball = Fireball(self.rect.centerx, self.rect.centery, direction)
            fireballs.add(fireball)
            self.can_shoot = False
            
    def update(self, platforms, enemies, coins, powerups, question_blocks, fireballs, particles):
        keys = pygame.key.get_pressed()
        
        # Running (hold shift)
        self.running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        speed = RUN_SPEED if self.running else PLAYER_SPEED
        
        # Horizontal movement
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -speed
            self.facing_right = False
            if self.on_ground and self.running:
                self.p_meter = min(self.p_meter + 1, 100)
        if keys[pygame.K_RIGHT]:
            self.vel_x = speed
            self.facing_right = True
            if self.on_ground and self.running:
                self.p_meter = min(self.p_meter + 1, 100)
                
        # Decrease P-meter when not running
        if not self.running or not self.on_ground:
            self.p_meter = max(self.p_meter - 2, 0)
            
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Jump / Fly
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            if self.p_meter >= 100 and self.state == RACCOON_MARIO:
                self.fly_timer = 100
        
        # Flying with Raccoon Mario
        if self.state == RACCOON_MARIO and self.fly_timer > 0 and keys[pygame.K_SPACE]:
            self.vel_y = -3
            self.fly_timer -= 1
        
        # Fireball shooting
        if keys[pygame.K_z] and not hasattr(self, 'z_pressed'):
            self.shoot_fireball(fireballs)
            self.z_pressed = True
        elif not keys[pygame.K_z]:
            self.z_pressed = False
            self.can_shoot = True
            
        # Update position
        self.rect.x += self.vel_x
        self.check_collision_x(platforms)
        
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision_y(platforms)
        
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Check enemy collision
        if self.invincible_timer == 0:
            enemy_hit = pygame.sprite.spritecollide(self, enemies, False)
            for enemy in enemy_hit:
                if self.vel_y > 0 and self.rect.bottom <= enemy.rect.centery:
                    enemy.kill()
                    self.vel_y = -10
                    self.score += 100
                    # Particles
                    for _ in range(8):
                        particles.add(Particle(enemy.rect.centerx, enemy.rect.centery, DARK_ORANGE))
                else:
                    self.take_damage()
                    
        # Check coin collision
        coin_hit = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hit:
            self.coins += 1
            self.score += 10
            for _ in range(5):
                particles.add(Particle(coin.rect.centerx, coin.rect.centery, COIN_GOLD))
            
        # Check powerup collision
        powerup_hit = pygame.sprite.spritecollide(self, powerups, True)
        for powerup in powerup_hit:
            self.collect_powerup(powerup)
            for _ in range(10):
                particles.add(Particle(powerup.rect.centerx, powerup.rect.centery, powerup.color))
            
        # Check question block collision
        for block in question_blocks:
            if self.rect.colliderect(block.rect) and self.vel_y < 0:
                if self.rect.top <= block.rect.bottom:
                    block.hit(powerups, coins, particles)
                    self.vel_y = 0
                    
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        # Fall off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.take_damage()
            
    def take_damage(self):
        if self.invincible_timer == 0:
            if self.state > SMALL_MARIO:
                self.state -= 1
                self.update_sprite()
                self.invincible_timer = 120
            else:
                self.lives -= 1
                self.rect.x = 50
                self.rect.y = 400
                self.invincible_timer = 120
            
    def collect_powerup(self, powerup):
        if powerup.powerup_type == POWERUP_MUSHROOM:
            if self.state == SMALL_MARIO:
                self.state = SUPER_MARIO
                self.score += 1000
        elif powerup.powerup_type == POWERUP_FIRE_FLOWER:
            self.state = FIRE_MARIO
            self.score += 1000
        elif powerup.powerup_type == POWERUP_LEAF:
            self.state = RACCOON_MARIO
            self.score += 1000
        self.update_sprite()
            
    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    
    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, style='ground'):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.style = style
        self.draw_platform()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw_platform(self):
        """Draw SMB3-style platforms with patterns"""
        width, height = self.image.get_size()
        
        if self.style == 'ground':
            self.image.fill(GROUND_BROWN)
            # Add pattern
            for x in range(0, width, 16):
                for y in range(0, height, 16):
                    pygame.draw.rect(self.image, BROWN, (x, y, 14, 14))
        elif self.style == 'brick':
            self.image.fill(BRICK_ORANGE)
            # Brick pattern
            brick_w = width // 4
            for i in range(4):
                pygame.draw.rect(self.image, DARK_ORANGE, (i * brick_w, 0, brick_w - 2, height))
        elif self.style == 'stone':
            self.image.fill((150, 150, 150))
            for x in range(0, width, 12):
                for y in range(0, height, 12):
                    pygame.draw.rect(self.image, (120, 120, 120), (x, y, 10, 10))
        elif self.style == 'cloud':
            self.image.fill(CLOUD_WHITE)
            pygame.draw.ellipse(self.image, WHITE, (0, 0, width, height))
        else:
            self.image.fill(GROUND_BROWN)

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.active = True
        self.draw_block()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.contents = random.choice([POWERUP_MUSHROOM, POWERUP_FIRE_FLOWER, POWERUP_LEAF, 'coin'])
        
    def draw_block(self):
        if self.active:
            # Active yellow block with question mark
            self.image.fill(COIN_GOLD)
            pygame.draw.rect(self.image, DARK_ORANGE, (0, 0, 32, 32), 3)
            # Question mark
            font = pygame.font.Font(None, 36)
            text = font.render("?", True, BLACK)
            self.image.blit(text, (8, 2))
        else:
            # Used brown block
            self.image.fill((136, 108, 56))
            pygame.draw.rect(self.image, (88, 64, 32), (0, 0, 32, 32), 3)
            
    def hit(self, powerups, coins, particles):
        if self.active:
            self.active = False
            self.draw_block()
            
            if self.contents == 'coin':
                coin = Coin(self.rect.x, self.rect.y - 40)
                coins.add(coin)
            else:
                powerup = Powerup(self.rect.x, self.rect.y - 40, self.contents)
                powerups.add(powerup)
                
            for _ in range(5):
                particles.add(Particle(self.rect.centerx, self.rect.top, COIN_GOLD))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='goomba'):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.Surface((32, 32))
        self.draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 2
        self.animate_timer = 0
        
    def draw_enemy(self):
        """Draw SMB3-style enemies"""
        if self.enemy_type == 'goomba':
            # Brown mushroom enemy
            pygame.draw.circle(self.image, BROWN, (16, 20), 14)
            pygame.draw.rect(self.image, BROWN, (4, 20, 24, 10))
            # Eyes
            pygame.draw.circle(self.image, WHITE, (11, 18), 3)
            pygame.draw.circle(self.image, WHITE, (21, 18), 3)
            pygame.draw.circle(self.image, BLACK, (11, 18), 2)
            pygame.draw.circle(self.image, BLACK, (21, 18), 2)
        elif self.enemy_type == 'koopa':
            # Green shell turtle
            pygame.draw.ellipse(self.image, SHELL_GREEN, (4, 12, 24, 20))
            pygame.draw.circle(self.image, (255, 200, 150), (16, 10), 6)
            pygame.draw.rect(self.image, SHELL_GREEN, (8, 18, 16, 3))
            
    def update(self):
        self.rect.x += self.vel_x
        self.animate_timer += 1
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel_x *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.draw_coin()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animate_timer = 0
        
    def draw_coin(self):
        """SMB3 style animated coin"""
        pygame.draw.circle(self.image, COIN_GOLD, (10, 10), 9)
        pygame.draw.circle(self.image, DARK_ORANGE, (10, 10), 7)
        pygame.draw.circle(self.image, COIN_GOLD, (10, 10), 5)
        
    def update(self):
        self.animate_timer += 1

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = pygame.Surface((28, 28))
        self.draw_powerup()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = -5
        
    def draw_powerup(self):
        """SMB3 style powerups"""
        if self.powerup_type == POWERUP_MUSHROOM:
            # Super Mushroom
            pygame.draw.circle(self.image, MUSHROOM_RED, (14, 18), 13)
            pygame.draw.rect(self.image, (255, 200, 150), (8, 18, 12, 10))
            pygame.draw.circle(self.image, WHITE, (8, 10), 4)
            pygame.draw.circle(self.image, WHITE, (20, 10), 4)
            self.color = MUSHROOM_RED
        elif self.powerup_type == POWERUP_FIRE_FLOWER:
            # Fire Flower
            pygame.draw.circle(self.image, MUSHROOM_RED, (14, 14), 8)
            pygame.draw.circle(self.image, BRICK_ORANGE, (14, 14), 5)
            pygame.draw.circle(self.image, COIN_GOLD, (7, 7), 3)
            pygame.draw.circle(self.image, COIN_GOLD, (21, 7), 3)
            pygame.draw.circle(self.image, COIN_GOLD, (7, 21), 3)
            pygame.draw.circle(self.image, COIN_GOLD, (21, 21), 3)
            self.color = MUSHROOM_RED
        elif self.powerup_type == POWERUP_LEAF:
            # Super Leaf
            pygame.draw.polygon(self.image, BROWN, [(14, 24), (4, 14), (14, 4), (24, 14)])
            pygame.draw.polygon(self.image, DARK_ORANGE, [(14, 20), (8, 14), (14, 8), (20, 14)])
            self.color = BROWN
            
    def update(self):
        self.vel_y += 0.3
        self.rect.y += self.vel_y
        if self.vel_y > 0:
            self.vel_y = 0

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        # Pole
        pygame.draw.rect(self.image, (180, 180, 180), (8, 0, 4, 100))
        # Flag
        pygame.draw.polygon(self.image, BLACK, [(12, 10), (12, 40), (20, 25)])
        pygame.draw.circle(self.image, COIN_GOLD, (8, 8), 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.question_blocks = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()
        self.generate_level()
        
    def generate_level(self):
        # World-Level calculation
        world = (self.level_num - 1) // 4 + 1
        stage = (self.level_num - 1) % 4 + 1
        
        # Ground platform
        self.platforms.add(Platform(0, 550, SCREEN_WIDTH, 50, 'ground'))
        
        # Generate platforms based on level number
        if stage == 1:  # Grass level
            for i in range(6):
                x = 120 + i * 130
                y = 450 - (i % 3) * 60
                self.platforms.add(Platform(x, y, 80, 20, 'brick'))
                if i % 2 == 0:
                    self.question_blocks.add(QuestionBlock(x + 25, y - 40))
                else:
                    self.coins.add(Coin(x + 30, y - 30))
                    
            # Enemies
            for i in range(world + 1):
                enemy_type = 'koopa' if i % 2 == 0 else 'goomba'
                self.enemies.add(Enemy(180 + i * 180, 510, enemy_type))
                
        elif stage == 2:  # Underground level
            for i in range(7):
                x = 90 + i * 110
                y = 400 - (i % 2) * 90
                self.platforms.add(Platform(x, y, 70, 20, 'stone'))
                self.coins.add(Coin(x + 25, y - 30))
                if i % 3 == 0:
                    self.question_blocks.add(QuestionBlock(x + 20, y - 40))
                
            for i in range(world + 2):
                self.enemies.add(Enemy(140 + i * 160, 510, 'goomba'))
                
        elif stage == 3:  # Sky level
            for i in range(8):
                x = 70 + i * 100
                y = 320 - (i % 4) * 70
                self.platforms.add(Platform(x, y, 60, 20, 'cloud'))
                if i % 2 == 0:
                    self.question_blocks.add(QuestionBlock(x + 15, y - 40))
                    
            for i in range(world):
                self.enemies.add(Enemy(90 + i * 220, 510, 'koopa'))
                
        else:  # Castle level (stage 4)
            for i in range(5):
                x = 140 + i * 150
                y = 420 - i * 45
                self.platforms.add(Platform(x, y, 90, 25, 'brick'))
                self.question_blocks.add(QuestionBlock(x + 30, y - 40))
                
            for i in range(world + 3):
                enemy_type = 'koopa' if i % 2 == 0 else 'goomba'
                self.enemies.add(Enemy(110 + i * 130, 510, enemy_type))
                
            # Castle platform
            self.platforms.add(Platform(650, 450, 120, 20, 'stone'))
            
        # Add flag at the end
        self.flag.add(Flag(750, 450))
        
        # Add scattered coins
        for i in range(8 + world):
            x = random.randint(100, 700)
            y = random.randint(200, 500)
            self.coins.add(Coin(x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Bros 3 - 32 Levels")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = TITLE_SCREEN
        self.current_level = 1
        self.player = None
        self.level = None
        self.fireballs = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.title_blink = 0
        self.world_map_selection = 0
        
    def new_game(self):
        self.current_level = 1
        self.player = Player(50, 400)
        self.state = WORLD_MAP
        
    def start_level(self, level_num):
        self.current_level = level_num
        self.level = Level(self.current_level)
        self.player.rect.x = 50
        self.player.rect.y = 400
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.fireballs.empty()
        self.particles.empty()
        self.state = PLAYING
        
    def next_level(self):
        if self.current_level < 32:
            self.current_level += 1
            self.state = WORLD_MAP
        else:
            self.state = GAME_WIN
            
    def draw_title_screen(self):
        # SMB3 style title with gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(92 + (y / SCREEN_HEIGHT) * 50)
            pygame.draw.line(self.screen, (color_val, color_val + 50, 252), (0, y), (SCREEN_WIDTH, y))
        
        # Title with shadow
        title_shadow = self.font_large.render("SUPER MARIO BROS 3", True, BLACK)
        title = self.font_large.render("SUPER MARIO BROS 3", True, WHITE)
        self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - 320, 102))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 322, 100))
        
        # Subtitle
        subtitle = self.font_medium.render("32 LEVELS EDITION", True, COIN_GOLD)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 200, 180))
        
        # Decorative Mario sprite
        mario_sprite = pygame.Surface((64, 64))
        pygame.draw.rect(mario_sprite, MARIO_RED, (16, 24, 32, 24))
        pygame.draw.rect(mario_sprite, MARIO_BLUE, (20, 16, 24, 24))
        pygame.draw.circle(mario_sprite, (255, 200, 150), (32, 16), 12)
        self.screen.blit(mario_sprite, (SCREEN_WIDTH // 2 - 32, 250))
        
        # Blinking start text
        self.title_blink += 1
        if self.title_blink % 60 < 30:
            start_text = self.font_small.render("PRESS ENTER TO START", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
            self.screen.blit(start_text, start_rect)
            
        # Controls
        controls = [
            "ARROW KEYS - Move  |  SHIFT - Run",
            "SPACE - Jump/Fly  |  Z - Shoot Fireball",
            "ESC - Quit"
        ]
        y = 460
        for control in controls:
            text = self.font_small.render(control, True, CLOUD_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 35
            
    def draw_world_map(self):
        # Sky background
        self.screen.fill(SKY_BLUE)
        
        # Clouds
        for i in range(5):
            x = (i * 200 + self.title_blink) % SCREEN_WIDTH
            y = 50 + i * 80
            pygame.draw.ellipse(self.screen, CLOUD_WHITE, (x, y, 80, 30))
            pygame.draw.ellipse(self.screen, CLOUD_WHITE, (x + 20, y - 10, 60, 30))
            
        # Title
        world = (self.current_level - 1) // 4 + 1
        title = self.font_large.render(f"WORLD {world}", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 140, 50))
        
        # Level circles (SMB3 style map)
        levels_in_world = [(i + (world - 1) * 4) for i in range(1, 5) if i + (world - 1) * 4 <= 32]
        
        for i, level in enumerate(levels_in_world):
            x = 200 + i * 150
            y = 300
            
            # Level node
            if level <= self.current_level:
                color = COIN_GOLD
            else:
                color = (100, 100, 100)
                
            pygame.draw.circle(self.screen, BLACK, (x + 2, y + 2), 32)
            pygame.draw.circle(self.screen, color, (x, y), 30)
            
            # Level number
            level_text = self.font_medium.render(str(level % 4 if level % 4 != 0 else 4), True, BLACK)
            text_rect = level_text.get_rect(center=(x, y))
            self.screen.blit(level_text, text_rect)
            
            # Connection lines
            if i < len(levels_in_world) - 1:
                pygame.draw.line(self.screen, BROWN, (x + 30, y), (x + 120, y), 4)
        
        # Instructions
        info = self.font_small.render("Press ENTER to start level", True, WHITE)
        self.screen.blit(info, (SCREEN_WIDTH // 2 - 150, 450))
        
        # Player stats
        stats = self.font_small.render(f"Lives: {self.player.lives}  Score: {self.player.score}  Coins: {self.player.coins}", True, WHITE)
        self.screen.blit(stats, (SCREEN_WIDTH // 2 - 200, 500))
            
    def draw_game(self):
        # Sky background
        self.screen.fill(SKY_BLUE)
        
        # Draw all sprites
        self.level.platforms.draw(self.screen)
        self.level.question_blocks.draw(self.screen)
        self.level.enemies.draw(self.screen)
        self.level.coins.draw(self.screen)
        self.level.powerups.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.particles.draw(self.screen)
        self.level.flag.draw(self.screen)
        
        # Draw player with invincibility flicker
        if self.player.invincible_timer == 0 or self.player.invincible_timer % 6 < 3:
            self.screen.blit(self.player.image, self.player.rect)
        
        # HUD Background
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 50))
        
        world = (self.current_level - 1) // 4 + 1
        stage = (self.current_level - 1) % 4 + 1
        
        # HUD Text
        level_text = self.font_small.render(f"WORLD {world}-{stage}", True, WHITE)
        self.screen.blit(level_text, (10, 12))
        
        score_text = self.font_small.render(f"SCORE: {self.player.score:06d}", True, WHITE)
        self.screen.blit(score_text, (200, 12))
        
        coins_text = self.font_small.render(f"x{self.player.coins:02d}", True, WHITE)
        self.screen.blit(coins_text, (480, 12))
        # Coin icon
        pygame.draw.circle(self.screen, COIN_GOLD, (465, 22), 8)
        
        lives_text = self.font_small.render(f"x{self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (630, 12))
        # Mario icon
        pygame.draw.circle(self.screen, MARIO_RED, (615, 22), 8)
        
        # P-Meter (for flying)
        if self.player.state == RACCOON_MARIO:
            p_meter_width = int((self.player.p_meter / 100) * 100)
            pygame.draw.rect(self.screen, WHITE, (690, 15, 102, 20), 2)
            if self.player.p_meter >= 100:
                color = COIN_GOLD
            else:
                color = MARIO_BLUE
            pygame.draw.rect(self.screen, color, (691, 16, p_meter_width, 18))
            p_text = self.font_small.render("P", True, WHITE)
            self.screen.blit(p_text, (670, 12))
        
    def draw_level_complete(self):
        self.screen.fill(BLACK)
        
        world = (self.current_level - 1) // 4 + 1
        stage = (self.current_level - 1) % 4 + 1
        
        # Title with animation
        title = self.font_large.render("COURSE CLEAR!", True, COIN_GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Level completed
        level_text = self.font_medium.render(f"World {world}-{stage} Complete!", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(level_text, level_rect)
        
        # Score
        score_text = self.font_small.render(f"Score: {self.player.score}", True, COIN_GOLD)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 340))
        self.screen.blit(score_text, score_rect)
        
        coins_text = self.font_small.render(f"Coins: {self.player.coins}", True, COIN_GOLD)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(coins_text, coins_rect)
        
        # Next instruction
        next_text = self.font_small.render("Press ENTER to continue", True, WHITE)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(next_text, next_rect)
        
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        title = self.font_large.render("GAME OVER", True, MUSHROOM_RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        score_text = self.font_medium.render(f"Final Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(score_text, score_rect)
        
        coins_text = self.font_medium.render(f"Coins Collected: {self.player.coins}", True, COIN_GOLD)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(coins_text, coins_rect)
        
        restart_text = self.font_small.render("Press ENTER to return to title", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_game_win(self):
        # Victory background
        for y in range(SCREEN_HEIGHT):
            color = int(100 + math.sin(y / 30 + self.title_blink / 10) * 50)
            pygame.draw.line(self.screen, (color, color, 100), (0, y), (SCREEN_WIDTH, y))
        
        title = self.font_large.render("CONGRATULATIONS!", True, COIN_GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)
        
        congrats = self.font_medium.render("All 32 Levels Complete!", True, WHITE)
        congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(congrats, congrats_rect)
        
        # Final stats
        score_text = self.font_medium.render(f"Final Score: {self.player.score}", True, COIN_GOLD)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(score_text, score_rect)
        
        coins_text = self.font_medium.render(f"Total Coins: {self.player.coins}", True, COIN_GOLD)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(coins_text, coins_rect)
        
        # Mario sprite celebration
        mario_sprite = pygame.Surface((96, 96))
        pygame.draw.rect(mario_sprite, MARIO_RED, (24, 36, 48, 36))
        pygame.draw.rect(mario_sprite, WHITE, (30, 24, 36, 36))
        pygame.draw.circle(mario_sprite, (255, 200, 150), (48, 24), 18)
        # Victory pose
        pygame.draw.rect(mario_sprite, MARIO_RED, (10, 50, 10, 20))  # Arm up
        pygame.draw.rect(mario_sprite, MARIO_RED, (76, 50, 10, 20))  # Arm up
        self.screen.blit(mario_sprite, (SCREEN_WIDTH // 2 - 48, 440))
        
        restart_text = self.font_small.render("Press ENTER to play again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 560))
        self.screen.blit(restart_text, restart_rect)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
                if event.key == pygame.K_RETURN:
                    if self.state == TITLE_SCREEN:
                        self.new_game()
                    elif self.state == WORLD_MAP:
                        self.start_level(self.current_level)
                    elif self.state == LEVEL_COMPLETE:
                        self.next_level()
                    elif self.state == GAME_OVER:
                        self.state = TITLE_SCREEN
                    elif self.state == GAME_WIN:
                        self.state = TITLE_SCREEN
                        
    def update(self):
        if self.state == PLAYING:
            self.player.update(
                self.level.platforms,
                self.level.enemies,
                self.level.coins,
                self.level.powerups,
                self.level.question_blocks,
                self.fireballs,
                self.particles
            )
            self.level.enemies.update()
            self.level.coins.update()
            self.level.powerups.update()
            self.fireballs.update(self.level.platforms)
            self.particles.update()
            
            # Check fireball-enemy collision
            for fireball in self.fireballs:
                enemy_hit = pygame.sprite.spritecollide(fireball, self.level.enemies, True)
                if enemy_hit:
                    fireball.kill()
                    self.player.score += 100
                    for enemy in enemy_hit:
                        for _ in range(10):
                            self.particles.add(Particle(enemy.rect.centerx, enemy.rect.centery, DARK_ORANGE))
            
            # Check if reached flag
            if pygame.sprite.spritecollide(self.player, self.level.flag, False):
                self.player.score += 1000
                self.state = LEVEL_COMPLETE
                
            # Check game over
            if self.player.lives <= 0:
                self.state = GAME_OVER
        
        # Update title blink timer
        self.title_blink += 1
                
    def draw(self):
        if self.state == TITLE_SCREEN:
            self.draw_title_screen()
        elif self.state == WORLD_MAP:
            self.draw_world_map()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == GAME_WIN:
            self.draw_game_win()
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

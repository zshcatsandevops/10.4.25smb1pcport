import os
import sys
import math
import random
import pygame

# ---------- Setup ----------
pygame.init()
pygame.display.set_caption("32-Level Platformer — NES Style")

# Screen & tiles
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 540
TILE = 32
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# NES-inspired color palette (SMB1 accurate)
SKY = (107, 129, 161)  # SMB1 sky blue
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)
BLUE = (0, 80, 220)
BROWN = (184, 112, 0)
GREEN = (0, 180, 0)
YELLOW = (252, 216, 0)
GRAY = (128, 128, 128)
DARK = (40, 40, 40)
PURPLE = (140, 70, 180)

FONT = pygame.font.Font(None, 26)
BIG_FONT = pygame.font.Font(None, 64)

MAX_LEVELS = 32
GRAVITY = 0.6

# ---------- Utility ----------
def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

# ---------- SMB1-Style Sprite Renderer ----------
class SpriteRenderer:
    @staticmethod
    def draw_player(surf, rect, facing_right=True):
        # Clear background under sprite
        pygame.draw.rect(surf, SKY, rect.inflate(2, 2))
        
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        skin = (252, 188, 176)
        overalls = (0, 80, 220)
        shirt = (220, 0, 0)
        shoe = (64, 32, 0)

        # Hat (top 1/4 height)
        pygame.draw.rect(surf, shirt, (x, y, w, h // 4))
        # Face
        pygame.draw.rect(surf, skin, (x, y + h // 4, w, h // 4))
        # Eyes (simple white dots)
        eye_y = y + h // 3
        eye_w = max(2, w // 8)
        if facing_right:
            pygame.draw.rect(surf, WHITE, (x + w - eye_w - 2, eye_y, eye_w, eye_w))
        else:
            pygame.draw.rect(surf, WHITE, (x + 2, eye_y, eye_w, eye_w))
        # Overalls (bottom 2/3)
        pygame.draw.rect(surf, overalls, (x, y + h // 2, w, h // 2))
        # Shoes
        pygame.draw.rect(surf, shoe, (x, y + h - 4, w, 4))

    @staticmethod
    def draw_goomba(surf, rect, alive=True, facing_right=True):
        if not alive:
            # Squashed Goomba: flat brown oval
            pygame.draw.ellipse(surf, BROWN, (rect.x, rect.bottom - 6, rect.width, 6))
            return

        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        body = BROWN
        feet = (100, 60, 0)
        eye_white = WHITE
        eye_black = BLACK

        # Body
        pygame.draw.ellipse(surf, body, (x, y, w, h - 4))
        # Feet
        pygame.draw.ellipse(surf, feet, (x, y + h - 6, w, 6))
        # Eyes
        eye_size = max(3, w // 6)
        left_eye_x = x + w // 3 - eye_size // 2
        right_eye_x = x + 2 * w // 3 - eye_size // 2
        eye_y = y + h // 3
        pygame.draw.ellipse(surf, eye_white, (left_eye_x, eye_y, eye_size, eye_size))
        pygame.draw.ellipse(surf, eye_white, (right_eye_x, eye_y, eye_size, eye_size))
        # Pupils (offset for facing direction)
        offset = 1 if facing_right else -1
        pygame.draw.ellipse(surf, eye_black, (left_eye_x + offset, eye_y + 1, eye_size // 2, eye_size // 2))
        pygame.draw.ellipse(surf, eye_black, (right_eye_x + offset, eye_y + 1, eye_size // 2, eye_size // 2))

    @staticmethod
    def draw_ground(surf, rect):
        # SMB1 ground is plain brown with no highlights
        pygame.draw.rect(surf, BROWN, rect)

    @staticmethod
    def draw_brick(surf, rect):
        base = (200, 76, 12)
        mortar = (120, 40, 0)
        pygame.draw.rect(surf, base, rect)
        # Mortar lines (SMB1 brick pattern)
        mid_x = rect.centerx
        mid_y = rect.centery
        pygame.draw.line(surf, mortar, (mid_x, rect.top), (mid_x, rect.bottom), 2)
        pygame.draw.line(surf, mortar, (rect.left, mid_y), (rect.right, mid_y), 2)

    @staticmethod
    def draw_question_block(surf, rect, animated=False):
        base = YELLOW
        symbol = (160, 130, 0)
        mortar = (180, 150, 0)
        pygame.draw.rect(surf, base, rect)
        # Mortar cross
        mid_x = rect.centerx
        mid_y = rect.centery
        pygame.draw.line(surf, mortar, (mid_x, rect.top), (mid_x, rect.bottom), 2)
        pygame.draw.line(surf, mortar, (rect.left, mid_y), (rect.right, mid_y), 2)
        # Question mark
        q_font = pygame.font.Font(None, 28)
        q_text = q_font.render("?", True, symbol)
        q_rect = q_text.get_rect(center=rect.center)
        surf.blit(q_text, q_rect)

# ---------- Entities ----------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 28)  # SMB1 Mario is ~16px wide
        self.velx = 0.0
        self.vely = 0.0
        self.on_ground = False
        self.facing_right = True
        self.max_speed = 5.2
        self.accel = 0.6
        self.jump_speed = 10.5
        self.ground_friction = 0.82
        self.air_drag = 0.98

    def update(self, keys, level):
        ax = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax -= self.accel
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax += self.accel
            self.facing_right = True

        self.velx += ax
        if ax == 0.0:
            self.velx *= (self.ground_friction if self.on_ground else self.air_drag)
        self.velx = clamp(self.velx, -self.max_speed, self.max_speed)

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_z]) and self.on_ground:
            self.vely = -self.jump_speed
            self.on_ground = False

        self.vely += GRAVITY
        self.vely = clamp(self.vely, -50, 15)

        # Horizontal collision
        self.rect.x += int(round(self.velx))
        for trect in level.iter_colliding_tiles(self.rect):
            if self.velx > 0:
                self.rect.right = trect.left
            elif self.velx < 0:
                self.rect.left = trect.right
            self.velx = 0

        # Vertical collision
        self.rect.y += int(round(self.vely))
        self.on_ground = False
        for trect in level.iter_colliding_tiles(self.rect):
            if self.vely > 0:
                self.rect.bottom = trect.top
                self.vely = 0
                self.on_ground = True
            elif self.vely < 0:
                self.rect.top = trect.bottom
                self.vely = 0

    def draw(self, surf, camx):
        draw_rect = self.rect.move(-camx, 0)
        SpriteRenderer.draw_player(surf, draw_rect, self.facing_right)

class Goomba:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.vx = random.choice([-1, 1]) * (1.0 + random.random() * 0.6)
        self.vy = 0.0
        self.alive = True
        self.squash_timer = 0
        self.facing_right = self.vx > 0

    def update(self, level):
        if not self.alive:
            self.squash_timer -= 1
            return

        self.vy += GRAVITY
        self.facing_right = self.vx > 0

        self.rect.x += int(self.vx)
        hit_wall = False
        for trect in level.iter_colliding_tiles(self.rect):
            hit_wall = True
            if self.vx > 0:
                self.rect.right = trect.left
            else:
                self.rect.left = trect.right
            self.vx = -self.vx
            break

        self.rect.y += int(self.vy)
        grounded = False
        for trect in level.iter_colliding_tiles(self.rect):
            if self.vy > 0:
                self.rect.bottom = trect.top
                self.vy = 0
                grounded = True
            elif self.vy < 0:
                self.rect.top = trect.bottom
                self.vy = 0

        if grounded and not hit_wall:
            ahead_x = self.rect.centerx + (12 if self.vx > 0 else -12)
            below = level.get_tile_at_pixel(ahead_x, self.rect.bottom + 2)
            if below not in level.solids:
                self.vx = -self.vx

    def draw(self, surf, camx):
        draw_rect = self.rect.move(-camx, 0)
        SpriteRenderer.draw_goomba(surf, draw_rect, self.alive, self.facing_right)

# ---------- Level ----------
class Level:
    solids = {'#', 'B', '?'}  

    def __init__(self, index):
        self.index = index
        self.grid = self._generate_level(index)
        self.h = len(self.grid)
        self.w = len(self.grid[0]) if self.h else 0
        self.pixel_w = self.w * TILE
        self.pixel_h = self.h * TILE
        self.enemies = []
        self.spawn_rect = None
        self.goal_rect = None
        self.flag_x_px = None

        for ty, row in enumerate(self.grid):
            for tx, ch in enumerate(row):
                if ch == 'G':
                    self.enemies.append(Goomba(tx * TILE + 8, ty * TILE + 16))
                    self.grid[ty][tx] = '.'
                elif ch == 'P':
                    self.spawn_rect = pygame.Rect(tx * TILE + 8, ty * TILE + 4, 16, 28)
                    self.grid[ty][tx] = '.'
                elif ch == 'F':
                    gx = tx * TILE
                    self.goal_rect = pygame.Rect(gx, 0, 2 * TILE, self.pixel_h)
                    self.flag_x_px = gx + TILE // 2
                    self.grid[ty][tx] = '.'

        if self.spawn_rect is None:
            for tx in range(self.w):
                for ty in range(self.h - 1):
                    if self.grid[ty][tx] == '.' and self.grid[ty + 1][tx] in self.solids:
                        self.spawn_rect = pygame.Rect(tx * TILE + 8, ty * TILE + 4, 16, 28)
                        break
                if self.spawn_rect:
                    break
        if self.goal_rect is None:
            gx = self.pixel_w - 3 * TILE
            self.goal_rect = pygame.Rect(gx, 0, 2 * TILE, self.pixel_h)
            self.flag_x_px = gx + TILE // 2

    def _generate_level(self, idx):
        r = random.Random(1000 + idx * 73)
        width = min(280, 180 + idx * 3)
        height = 16
        ground_y = height - 2

        grid = [['.' for _ in range(width)] for _ in range(height)]
        for x in range(width):
            grid[ground_y][x] = '#'
            grid[ground_y + 1][x] = '#'

        x = 10
        hole_prob = min(0.18, 0.08 + idx * 0.003)
        max_hole = min(4, 2 + idx // 8)
        while x < width - 10:
            if r.random() < hole_prob:
                w = r.randint(1, max_hole)
                for i in range(w):
                    if x + i < width - 2:
                        grid[ground_y][x + i] = '.'
                        grid[ground_y + 1][x + i] = '.'
                x += w + r.randint(2, 6)
            else:
                x += 1

        blocks = 26 + idx * 2
        for _ in range(blocks):
            bx = r.randint(4, width - 4)
            by = r.randint(4, ground_y - 3)
            grid[by][bx] = 'B' if r.random() < 0.6 else '?'

        for step in range(6):
            base_x = width - 20 + step * 2
            for k in range(step + 1):
                y = ground_y - k
                if 0 <= base_x < width:
                    grid[y][base_x] = '#'

        enemy_count = 8 + idx // 2
        attempts, placed = 0, 0
        while placed < enemy_count and attempts < enemy_count * 12:
            attempts += 1
            ex = r.randint(6, width - 8)
            if grid[ground_y][ex] == '#':
                grid[ground_y - 1][ex] = 'G'
                placed += 1

        grid[ground_y - 1][2] = 'P'
        grid[ground_y - 2][width - 6] = 'F'
        return grid

    def iter_colliding_tiles(self, rect):
        left = max(0, rect.left // TILE)
        right = min(self.w - 1, (rect.right - 1) // TILE)
        top = max(0, rect.top // TILE)
        bottom = min(self.h - 1, (rect.bottom - 1) // TILE)
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                ch = self.grid[ty][tx]
                if ch in self.solids:
                    yield pygame.Rect(tx * TILE, ty * TILE, TILE, TILE)

    def get_tile_at_pixel(self, px, py):
        tx = int(px) // TILE
        ty = int(py) // TILE
        if 0 <= tx < self.w and 0 <= ty < self.h:
            return self.grid[ty][tx]
        return '#'

    def draw(self, surf, camx):
        start_tx = max(0, camx // TILE - 1)
        end_tx = min(self.w, (camx + SCREEN_WIDTH) // TILE + 2)

        # Background: SMB1 sky
        surf.fill(SKY)

        for ty in range(self.h):
            for tx in range(start_tx, end_tx):
                ch = self.grid[ty][tx]
                px = tx * TILE - camx
                py = ty * TILE
                tile_rect = pygame.Rect(px, py, TILE, TILE)
                if ch == '#':
                    SpriteRenderer.draw_ground(surf, tile_rect)
                elif ch == 'B':
                    SpriteRenderer.draw_brick(surf, tile_rect)
                elif ch == '?':
                    SpriteRenderer.draw_question_block(surf, tile_rect)

        if self.flag_x_px is not None:
            fx = self.flag_x_px - camx
            pygame.draw.line(surf, (200, 200, 200), (fx, TILE), (fx, self.pixel_h - TILE), 4)
            pygame.draw.polygon(surf, GREEN, [(fx, TILE + 8), (fx + 16, TILE + 14), (fx, TILE + 20)])
            pygame.draw.circle(surf, (240, 240, 240), (int(fx), TILE), 6)

# ---------- Game loop ----------
def main():
    clock = pygame.time.Clock()
    random.seed(0)

    level_idx = 0
    level = Level(level_idx)
    player = Player(level.spawn_rect.x, level.spawn_rect.y)
    lives = 3
    score = 0
    state = "playing"

    while True:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    level = Level(level_idx)
                    player = Player(level.spawn_rect.x, level.spawn_rect.y)

        keys = pygame.key.get_pressed()

        if state == "playing":
            player.update(keys, level)
            for e in level.enemies:
                e.update(level)

            for e in list(level.enemies):
                if not e.alive:
                    if e.squash_timer <= 0:
                        level.enemies.remove(e)
                    continue
                if player.rect.colliderect(e.rect):
                    from_above = player.vely > 0 and (player.rect.bottom - e.rect.top) < 12
                    if from_above:
                        e.alive = False
                        e.squash_timer = 30
                        player.vely = -player.jump_speed * 0.6
                        score += 100
                    else:
                        lives -= 1
                        if lives <= 0:
                            state = "gameover"
                        else:
                            level = Level(level_idx)
                            player = Player(level.spawn_rect.x, level.spawn_rect.y)
                        break

            if player.rect.top > level.pixel_h + 200:
                lives -= 1
                if lives <= 0:
                    state = "gameover"
                else:
                    level = Level(level_idx)
                    player = Player(level.spawn_rect.x, level.spawn_rect.y)

            if player.rect.colliderect(level.goal_rect):
                score += 500
                level_idx += 1
                if level_idx >= MAX_LEVELS:
                    state = "allclear"
                else:
                    level = Level(level_idx)
                    player = Player(level.spawn_rect.x, level.spawn_rect.y)

        camx = clamp(player.rect.centerx - SCREEN_WIDTH // 2, 0, max(0, level.pixel_w - SCREEN_WIDTH))

        screen.fill(SKY)
        level.draw(screen, camx)
        for e in level.enemies:
            e.draw(screen, camx)
        player.draw(screen, camx)

        ui_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 32)
        pygame.draw.rect(screen, (0, 0, 0, 180), ui_bar)
        pygame.draw.rect(screen, BLACK, ui_bar, 1)
        txt = f"Level {min(level_idx+1, MAX_LEVELS)}/{MAX_LEVELS}   Lives: {lives}   Score: {score}"
        screen.blit(FONT.render(txt, True, WHITE), (10, 8))

        if state == "gameover":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            game_over = BIG_FONT.render("GAME OVER", True, RED)
            prompt = FONT.render("Press R to retry the current level", True, WHITE)
            screen.blit(game_over, game_over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
            screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

        if state == "allclear":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            congrats = BIG_FONT.render("ALL 32 LEVELS CLEARED!", True, GREEN)
            screen.blit(congrats, congrats.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        pygame.display.flip()

if __name__ == "__main__":
    main()

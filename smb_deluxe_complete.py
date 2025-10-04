import pygame
import sys

# ============================================================================
# LEVEL DATA - 32 Levels for Super Mario Bros Deluxe
# ============================================================================

# Format: (x, y, width, height, color_optional)
# Platforms, Goals: (x, y)
# Enemies: (x, y, size, speed)

LEVELS = [
    # WORLD 1 - Tutorial Levels
    {
        'name': 'Level 1-1: First Steps',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),  # Ground
            (200, 480, 150, 20, (139, 69, 19)),  # Platform
            (450, 400, 150, 20, (139, 69, 19)),
        ],
        'goal': (720, 490),
        'enemies': []
    },
    {
        'name': 'Level 1-2: Jump Training',
        'start': (50, 400),
        'platforms': [
            (0, 560, 200, 40, (0, 200, 0)),
            (250, 560, 200, 40, (0, 200, 0)),
            (500, 560, 300, 40, (0, 200, 0)),
            (300, 450, 100, 20, (139, 69, 19)),
        ],
        'goal': (750, 490),
        'enemies': []
    },
    {
        'name': 'Level 1-3: First Enemy',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (300, 480, 200, 20, (139, 69, 19)),
        ],
        'goal': (720, 490),
        'enemies': [(400, 440, 30, 2)]
    },
    {
        'name': 'Level 1-4: Stairway',
        'start': (50, 400),
        'platforms': [
            (0, 560, 200, 40, (0, 200, 0)),
            (150, 500, 100, 20, (139, 69, 19)),
            (250, 440, 100, 20, (139, 69, 19)),
            (350, 380, 100, 20, (139, 69, 19)),
            (450, 320, 100, 20, (139, 69, 19)),
            (550, 380, 100, 20, (139, 69, 19)),
            (650, 440, 150, 20, (139, 69, 19)),
        ],
        'goal': (750, 370),
        'enemies': []
    },
    
    # WORLD 2 - Basic Challenges
    {
        'name': 'Level 2-1: Gap Jumps',
        'start': (50, 400),
        'platforms': [
            (0, 560, 150, 40, (0, 200, 0)),
            (250, 560, 150, 40, (0, 200, 0)),
            (500, 560, 150, 40, (0, 200, 0)),
            (700, 560, 100, 40, (0, 200, 0)),
        ],
        'goal': (730, 490),
        'enemies': [(300, 520, 30, 2)]
    },
    {
        'name': 'Level 2-2: Platform Hopping',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (150, 450, 80, 20, (139, 69, 19)),
            (300, 380, 80, 20, (139, 69, 19)),
            (450, 310, 80, 20, (139, 69, 19)),
            (600, 380, 80, 20, (139, 69, 19)),
        ],
        'goal': (650, 310),
        'enemies': [(200, 520, 30, 2), (500, 520, 30, 2)]
    },
    {
        'name': 'Level 2-3: Enemy Patrol',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (200, 460, 400, 20, (139, 69, 19)),
        ],
        'goal': (520, 390),
        'enemies': [(250, 420, 30, 3), (450, 420, 30, 2)]
    },
    {
        'name': 'Level 2-4: Vertical Challenge',
        'start': (50, 500),
        'platforms': [
            (0, 560, 150, 40, (0, 200, 0)),
            (100, 480, 100, 20, (139, 69, 19)),
            (250, 400, 100, 20, (139, 69, 19)),
            (150, 320, 100, 20, (139, 69, 19)),
            (300, 240, 100, 20, (139, 69, 19)),
            (450, 240, 200, 20, (139, 69, 19)),
        ],
        'goal': (600, 170),
        'enemies': [(350, 200, 30, 2)]
    },
    
    # WORLD 3 - Intermediate
    {
        'name': 'Level 3-1: The Gauntlet',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (200, 450, 100, 20, (139, 69, 19)),
            (400, 450, 100, 20, (139, 69, 19)),
            (600, 450, 100, 20, (139, 69, 19)),
        ],
        'goal': (650, 380),
        'enemies': [(250, 410, 30, 2), (450, 410, 30, 3), (650, 410, 30, 2)]
    },
    {
        'name': 'Level 3-2: Precision Jumps',
        'start': (50, 400),
        'platforms': [
            (0, 560, 120, 40, (0, 200, 0)),
            (200, 500, 60, 20, (139, 69, 19)),
            (340, 440, 60, 20, (139, 69, 19)),
            (480, 380, 60, 20, (139, 69, 19)),
            (620, 440, 60, 20, (139, 69, 19)),
            (740, 500, 60, 20, (139, 69, 19)),
        ],
        'goal': (770, 430),
        'enemies': []
    },
    {
        'name': 'Level 3-3: Enemy Swarm',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (300, 420, 200, 20, (139, 69, 19)),
        ],
        'goal': (720, 490),
        'enemies': [(200, 520, 30, 2), (350, 380, 30, 3), 
                   (500, 520, 30, 2), (600, 520, 30, 3)]
    },
    {
        'name': 'Level 3-4: Up and Down',
        'start': (50, 500),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (120, 480, 80, 20, (139, 69, 19)),
            (220, 400, 80, 20, (139, 69, 19)),
            (320, 320, 80, 20, (139, 69, 19)),
            (420, 400, 80, 20, (139, 69, 19)),
            (520, 480, 80, 20, (139, 69, 19)),
            (620, 560, 180, 40, (0, 200, 0)),
        ],
        'goal': (720, 490),
        'enemies': [(270, 360, 30, 2), (470, 440, 30, 2)]
    },
    
    # WORLD 4 - Advanced
    {
        'name': 'Level 4-1: Speed Run',
        'start': (50, 400),
        'platforms': [
            (0, 560, 150, 40, (0, 200, 0)),
            (200, 560, 100, 40, (0, 200, 0)),
            (350, 560, 100, 40, (0, 200, 0)),
            (500, 560, 100, 40, (0, 200, 0)),
            (650, 560, 150, 40, (0, 200, 0)),
        ],
        'goal': (730, 490),
        'enemies': [(250, 520, 30, 4), (400, 520, 30, 4), (550, 520, 30, 4)]
    },
    {
        'name': 'Level 4-2: Sky Platforms',
        'start': (50, 500),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (150, 450, 80, 20, (139, 69, 19)),
            (280, 360, 80, 20, (139, 69, 19)),
            (410, 270, 80, 20, (139, 69, 19)),
            (540, 270, 80, 20, (139, 69, 19)),
            (670, 360, 130, 20, (139, 69, 19)),
        ],
        'goal': (730, 290),
        'enemies': [(200, 410, 30, 2), (330, 320, 30, 2)]
    },
    {
        'name': 'Level 4-3: Danger Zone',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (150, 440, 120, 20, (139, 69, 19)),
            (350, 440, 120, 20, (139, 69, 19)),
            (550, 440, 120, 20, (139, 69, 19)),
        ],
        'goal': (620, 370),
        'enemies': [(200, 400, 30, 3), (400, 400, 30, 3), 
                   (300, 520, 30, 2), (500, 520, 30, 2), (600, 400, 30, 3)]
    },
    {
        'name': 'Level 4-4: Castle Stairs',
        'start': (50, 500),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (80, 500, 60, 20, (100, 100, 100)),
            (140, 440, 60, 20, (100, 100, 100)),
            (200, 380, 60, 20, (100, 100, 100)),
            (260, 320, 60, 20, (100, 100, 100)),
            (320, 260, 60, 20, (100, 100, 100)),
            (380, 200, 60, 20, (100, 100, 100)),
            (440, 200, 360, 20, (100, 100, 100)),
        ],
        'goal': (750, 130),
        'enemies': [(190, 340, 30, 2), (310, 220, 30, 2), (550, 160, 30, 3)]
    },
    
    # WORLD 5 - Expert
    {
        'name': 'Level 5-1: Maze Runner',
        'start': (50, 500),
        'platforms': [
            (0, 560, 200, 40, (0, 200, 0)),
            (250, 480, 100, 80, (139, 69, 19)),
            (250, 380, 100, 20, (139, 69, 19)),
            (400, 480, 100, 80, (139, 69, 19)),
            (550, 380, 100, 180, (139, 69, 19)),
            (700, 480, 100, 80, (139, 69, 19)),
        ],
        'goal': (730, 410),
        'enemies': [(300, 340, 30, 2), (450, 440, 30, 2)]
    },
    {
        'name': 'Level 5-2: Floating Islands',
        'start': (50, 500),
        'platforms': [
            (0, 560, 80, 40, (0, 200, 0)),
            (140, 480, 70, 15, (139, 69, 19)),
            (250, 400, 70, 15, (139, 69, 19)),
            (360, 320, 70, 15, (139, 69, 19)),
            (470, 320, 70, 15, (139, 69, 19)),
            (580, 400, 70, 15, (139, 69, 19)),
            (690, 480, 110, 15, (139, 69, 19)),
        ],
        'goal': (740, 410),
        'enemies': [(300, 360, 30, 2), (520, 360, 30, 2)]
    },
    {
        'name': 'Level 5-3: Narrow Escape',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (200, 460, 50, 20, (139, 69, 19)),
            (300, 460, 50, 20, (139, 69, 19)),
            (400, 460, 50, 20, (139, 69, 19)),
            (500, 460, 50, 20, (139, 69, 19)),
            (600, 460, 50, 20, (139, 69, 19)),
        ],
        'goal': (630, 390),
        'enemies': [(240, 420, 30, 3), (340, 420, 30, 3), 
                   (440, 420, 30, 3), (540, 420, 30, 3)]
    },
    {
        'name': 'Level 5-4: Tower Climb',
        'start': (50, 520),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (120, 490, 70, 15, (139, 69, 19)),
            (70, 420, 70, 15, (139, 69, 19)),
            (140, 350, 70, 15, (139, 69, 19)),
            (70, 280, 70, 15, (139, 69, 19)),
            (140, 210, 70, 15, (139, 69, 19)),
            (70, 140, 130, 15, (139, 69, 19)),
            (250, 140, 550, 15, (139, 69, 19)),
        ],
        'goal': (750, 70),
        'enemies': [(120, 310, 30, 2), (120, 170, 30, 2), (400, 100, 30, 3)]
    },
    
    # WORLD 6 - Master
    {
        'name': 'Level 6-1: Death From Above',
        'start': (50, 500),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (150, 500, 60, 15, (139, 69, 19)),
            (250, 440, 60, 15, (139, 69, 19)),
            (350, 380, 60, 15, (139, 69, 19)),
            (450, 320, 60, 15, (139, 69, 19)),
            (550, 260, 60, 15, (139, 69, 19)),
            (650, 200, 150, 15, (139, 69, 19)),
        ],
        'goal': (750, 130),
        'enemies': [(200, 460, 30, 2), (300, 400, 30, 2), 
                   (400, 340, 30, 2), (500, 280, 30, 2), (600, 220, 30, 2)]
    },
    {
        'name': 'Level 6-2: Platform Hell',
        'start': (50, 500),
        'platforms': [
            (0, 560, 70, 40, (0, 200, 0)),
            (120, 480, 50, 15, (139, 69, 19)),
            (220, 400, 50, 15, (139, 69, 19)),
            (320, 320, 50, 15, (139, 69, 19)),
            (420, 400, 50, 15, (139, 69, 19)),
            (520, 480, 50, 15, (139, 69, 19)),
            (620, 400, 50, 15, (139, 69, 19)),
            (720, 480, 80, 15, (139, 69, 19)),
        ],
        'goal': (750, 410),
        'enemies': [(270, 360, 30, 2), (370, 440, 30, 2), (470, 520, 30, 3)]
    },
    {
        'name': 'Level 6-3: The Grinder',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
            (100, 450, 80, 20, (139, 69, 19)),
            (250, 450, 80, 20, (139, 69, 19)),
            (400, 450, 80, 20, (139, 69, 19)),
            (550, 450, 80, 20, (139, 69, 19)),
            (700, 450, 100, 20, (139, 69, 19)),
        ],
        'goal': (750, 380),
        'enemies': [(140, 410, 30, 4), (290, 410, 30, 4), 
                   (440, 410, 30, 4), (590, 410, 30, 4)]
    },
    {
        'name': 'Level 6-4: Final Castle',
        'start': (50, 500),
        'platforms': [
            (0, 560, 80, 40, (100, 100, 100)),
            (100, 500, 60, 15, (100, 100, 100)),
            (180, 440, 60, 15, (100, 100, 100)),
            (260, 380, 60, 15, (100, 100, 100)),
            (340, 320, 60, 15, (100, 100, 100)),
            (420, 260, 60, 15, (100, 100, 100)),
            (500, 320, 60, 15, (100, 100, 100)),
            (580, 380, 60, 15, (100, 100, 100)),
            (660, 320, 140, 15, (100, 100, 100)),
        ],
        'goal': (760, 250),
        'enemies': [(130, 460, 30, 2), (210, 400, 30, 2), (290, 340, 30, 3),
                   (370, 280, 30, 2), (530, 340, 30, 3), (610, 400, 30, 2)]
    },
    
    # WORLD 7 - Insane
    {
        'name': 'Level 7-1: No Ground',
        'start': (50, 450),
        'platforms': [
            (0, 500, 80, 15, (139, 69, 19)),
            (120, 420, 60, 15, (139, 69, 19)),
            (220, 360, 60, 15, (139, 69, 19)),
            (320, 300, 60, 15, (139, 69, 19)),
            (420, 360, 60, 15, (139, 69, 19)),
            (520, 420, 60, 15, (139, 69, 19)),
            (620, 360, 60, 15, (139, 69, 19)),
            (720, 300, 80, 15, (139, 69, 19)),
        ],
        'goal': (760, 230),
        'enemies': [(170, 380, 30, 2), (370, 320, 30, 2), (570, 380, 30, 2)]
    },
    {
        'name': 'Level 7-2: Bullet Hell',
        'start': (50, 400),
        'platforms': [
            (0, 560, 800, 40, (0, 200, 0)),
        ],
        'goal': (750, 490),
        'enemies': [(150, 520, 30, 5), (250, 520, 30, 5), (350, 520, 30, 5),
                   (450, 520, 30, 5), (550, 520, 30, 5), (650, 520, 30, 5)]
    },
    {
        'name': 'Level 7-3: Spiral Ascent',
        'start': (50, 520),
        'platforms': [
            (0, 560, 100, 40, (0, 200, 0)),
            (120, 490, 60, 15, (139, 69, 19)),
            (200, 420, 60, 15, (139, 69, 19)),
            (280, 350, 60, 15, (139, 69, 19)),
            (360, 280, 60, 15, (139, 69, 19)),
            (440, 210, 60, 15, (139, 69, 19)),
            (520, 140, 60, 15, (139, 69, 19)),
            (440, 140, 60, 15, (139, 69, 19)),
            (360, 140, 60, 15, (139, 69, 19)),
            (280, 140, 60, 15, (139, 69, 19)),
            (280, 70, 520, 15, (139, 69, 19)),
        ],
        'goal': (760, 0),
        'enemies': [(170, 450, 30, 2), (250, 380, 30, 2), (330, 310, 30, 2),
                   (410, 240, 30, 2), (490, 170, 30, 2)]
    },
    {
        'name': 'Level 7-4: The Gauntlet Supreme',
        'start': (50, 500),
        'platforms': [
            (0, 560, 70, 40, (100, 100, 100)),
            (100, 490, 50, 15, (100, 100, 100)),
            (180, 420, 50, 15, (100, 100, 100)),
            (260, 350, 50, 15, (100, 100, 100)),
            (340, 280, 50, 15, (100, 100, 100)),
            (420, 350, 50, 15, (100, 100, 100)),
            (500, 420, 50, 15, (100, 100, 100)),
            (580, 350, 50, 15, (100, 100, 100)),
            (660, 280, 140, 15, (100, 100, 100)),
        ],
        'goal': (760, 210),
        'enemies': [(130, 450, 30, 3), (210, 380, 30, 3), (290, 310, 30, 4),
                   (370, 380, 30, 3), (450, 450, 30, 3), (530, 380, 30, 4)]
    },
    
    # WORLD 8 - Impossible
    {
        'name': 'Level 8-1: Nightmare',
        'start': (50, 480),
        'platforms': [
            (0, 530, 60, 15, (139, 69, 19)),
            (100, 460, 50, 15, (139, 69, 19)),
            (190, 390, 50, 15, (139, 69, 19)),
            (280, 320, 50, 15, (139, 69, 19)),
            (370, 250, 50, 15, (139, 69, 19)),
            (460, 320, 50, 15, (139, 69, 19)),
            (550, 390, 50, 15, (139, 69, 19)),
            (640, 460, 50, 15, (139, 69, 19)),
            (730, 390, 70, 15, (139, 69, 19)),
        ],
        'goal': (760, 320),
        'enemies': [(140, 420, 30, 3), (230, 350, 30, 3), (320, 280, 30, 4),
                   (410, 350, 30, 3), (500, 420, 30, 3), (590, 490, 30, 3)]
    },
    {
        'name': 'Level 8-2: The Void',
        'start': (50, 450),
        'platforms': [
            (0, 500, 70, 15, (139, 69, 19)),
            (120, 430, 55, 15, (139, 69, 19)),
            (225, 360, 55, 15, (139, 69, 19)),
            (330, 290, 55, 15, (139, 69, 19)),
            (435, 220, 55, 15, (139, 69, 19)),
            (540, 290, 55, 15, (139, 69, 19)),
            (645, 360, 55, 15, (139, 69, 19)),
            (745, 290, 55, 15, (139, 69, 19)),
        ],
        'goal': (770, 220),
        'enemies': [(165, 390, 30, 2), (270, 320, 30, 3), (375, 250, 30, 4),
                   (480, 180, 30, 3), (585, 250, 30, 3), (690, 320, 30, 2)]
    },
    {
        'name': 'Level 8-3: Perfect Timing',
        'start': (50, 500),
        'platforms': [
            (0, 550, 60, 15, (139, 69, 19)),
            (110, 480, 45, 15, (139, 69, 19)),
            (205, 410, 45, 15, (139, 69, 19)),
            (300, 340, 45, 15, (139, 69, 19)),
            (395, 270, 45, 15, (139, 69, 19)),
            (490, 200, 45, 15, (139, 69, 19)),
            (585, 270, 45, 15, (139, 69, 19)),
            (680, 340, 120, 15, (139, 69, 19)),
        ],
        'goal': (760, 270),
        'enemies': [(140, 440, 30, 4), (235, 370, 30, 4), (330, 300, 30, 5),
                   (425, 230, 30, 4), (520, 160, 30, 4), (615, 230, 30, 4)]
    },
    {
        'name': 'Level 8-4: The Final Challenge',
        'start': (50, 520),
        'platforms': [
            (0, 560, 60, 40, (255, 0, 0)),
            (90, 500, 45, 15, (100, 100, 100)),
            (165, 440, 45, 15, (100, 100, 100)),
            (240, 380, 45, 15, (100, 100, 100)),
            (315, 320, 45, 15, (100, 100, 100)),
            (390, 260, 45, 15, (100, 100, 100)),
            (465, 200, 45, 15, (100, 100, 100)),
            (540, 260, 45, 15, (100, 100, 100)),
            (615, 320, 45, 15, (100, 100, 100)),
            (690, 260, 110, 15, (100, 100, 100)),
        ],
        'goal': (760, 190),
        'enemies': [(120, 460, 30, 4), (195, 400, 30, 4), (270, 340, 30, 5),
                   (345, 280, 30, 5), (420, 220, 30, 5), (495, 160, 30, 4),
                   (570, 220, 30, 5), (645, 280, 30, 4)]
    },
]

# Overworld node positions (x, y) - creates a winding path
OVERWORLD_NODES = [
    # World 1
    (100, 500), (150, 450), (200, 400), (250, 350),
    # World 2
    (300, 320), (350, 280), (400, 250), (450, 220),
    # World 3
    (500, 250), (550, 280), (600, 310), (650, 340),
    # World 4
    (680, 380), (650, 420), (600, 450), (550, 480),
    # World 5
    (500, 500), (450, 470), (400, 440), (350, 410),
    # World 6
    (300, 380), (250, 350), (200, 320), (150, 290),
    # World 7
    (120, 250), (150, 210), (200, 180), (250, 150),
    # World 8
    (300, 130), (350, 110), (400, 100), (450, 90),
]

# ============================================================================
# GAME ENGINE
# ============================================================================

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
SKY_BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)

# Game States
STATE_OVERWORLD = 0
STATE_LEVEL = 1
STATE_GAME_OVER = 2
STATE_VICTORY = 3

class Player(pygame.sprite.Sprite):
    """The player character with fixed physics."""
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 50))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect()
        
        # Physics variables
        self.pos = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        # Movement constants
        self.ACC = 0.5
        self.FRIC = -0.12
        self.GRAVITY = 0.8
        self.JUMP_STRENGTH = -16
        self.MAX_SPEED = 8
        self.on_ground = False
        
    def reset_position(self, x, y):
        """Reset player to starting position."""
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.topleft = (x, y)

    def move(self):
        """Handle horizontal movement."""
        self.acc = pygame.math.Vector2(0, self.GRAVITY)
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -self.ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.ACC

        # Apply friction
        self.acc.x += self.vel.x * self.FRIC
        
        # Update velocity
        self.vel += self.acc
        
        # Limit horizontal speed
        if abs(self.vel.x) > self.MAX_SPEED:
            self.vel.x = self.MAX_SPEED if self.vel.x > 0 else -self.MAX_SPEED
        
        # Update horizontal position
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        
        # Keep player on screen horizontally
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        if self.pos.x > SCREEN_WIDTH - self.rect.width:
            self.pos.x = SCREEN_WIDTH - self.rect.width
            self.vel.x = 0
            
        self.rect.x = int(self.pos.x)

    def jump(self):
        """Jump if on ground."""
        if self.on_ground:
            self.vel.y = self.JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        """Update vertical position and handle collisions."""
        # Update vertical position
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = int(self.pos.y)
        
        # Check vertical collisions
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        if hits:
            if self.vel.y > 0:  # Falling - land on top
                self.rect.bottom = hits[0].rect.top
                self.pos.y = self.rect.y
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:  # Jumping - hit bottom
                self.rect.top = hits[0].rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0
        
        # Fall off bottom = death
        if self.rect.top > SCREEN_HEIGHT:
            return True  # Player died
        
        return False

class Platform(pygame.sprite.Sprite):
    """Platform/block class."""
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft=(x, y))

class Goal(pygame.sprite.Sprite):
    """Level goal/flag."""
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((30, 60))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    """Simple enemy that moves left and right."""
    def __init__(self, x, y, width, speed=2):
        super().__init__()
        self.surf = pygame.Surface((width, width))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 1
        self.start_x = x
        self.patrol_distance = 100
        
    def update(self):
        """Move enemy back and forth."""
        self.rect.x += self.speed * self.direction
        
        if self.rect.x > self.start_x + self.patrol_distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

class Level:
    """Manages a single level."""
    def __init__(self, level_data):
        self.platforms = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        
        # Create platforms
        for platform in level_data['platforms']:
            p = Platform(*platform)
            self.platforms.add(p)
            self.all_sprites.add(p)
        
        # Create goal
        if 'goal' in level_data:
            g = Goal(*level_data['goal'])
            self.goals.add(g)
            self.all_sprites.add(g)
        
        # Create enemies
        if 'enemies' in level_data:
            for enemy_data in level_data['enemies']:
                e = Enemy(*enemy_data)
                self.enemies.add(e)
                self.all_sprites.add(e)
        
        self.start_pos = level_data.get('start', (50, 300))
        
    def update(self):
        """Update all level elements."""
        self.enemies.update()

class OverworldNode:
    """Represents a level node on the overworld."""
    def __init__(self, x, y, level_num, unlocked=False, completed=False):
        self.x = x
        self.y = y
        self.level_num = level_num
        self.unlocked = unlocked
        self.completed = completed
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)

class Overworld:
    """Overworld map where players select levels."""
    def __init__(self):
        self.nodes = []
        self.current_node = 0
        
        # Create nodes from level data
        for i, node_data in enumerate(OVERWORLD_NODES):
            unlocked = (i == 0)  # First level is unlocked
            node = OverworldNode(node_data[0], node_data[1], i, unlocked)
            self.nodes.append(node)
        
        self.player_pos = [self.nodes[0].x, self.nodes[0].y]
        
    def move_selection(self, direction):
        """Move to next/previous level."""
        if direction == 1 and self.current_node < len(self.nodes) - 1:
            if self.nodes[self.current_node + 1].unlocked:
                self.current_node += 1
        elif direction == -1 and self.current_node > 0:
            self.current_node -= 1
        
        # Update player position with smooth movement
        target_node = self.nodes[self.current_node]
        self.player_pos[0] = target_node.x
        self.player_pos[1] = target_node.y
    
    def complete_level(self, level_num):
        """Mark level as completed and unlock next."""
        if level_num < len(self.nodes):
            self.nodes[level_num].completed = True
            if level_num + 1 < len(self.nodes):
                self.nodes[level_num + 1].unlocked = True
    
    def draw(self, screen):
        """Draw the overworld map."""
        screen.fill(SKY_BLUE)
        
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("SUPER MARIO BROS DELUXE", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Draw paths between nodes
        for i in range(len(self.nodes) - 1):
            if self.nodes[i + 1].unlocked:
                color = YELLOW
            else:
                color = (100, 100, 100)
            pygame.draw.line(screen, color, 
                           (self.nodes[i].x, self.nodes[i].y),
                           (self.nodes[i + 1].x, self.nodes[i + 1].y), 4)
        
        # Draw nodes
        for node in self.nodes:
            if node.completed:
                color = GREEN
            elif node.unlocked:
                color = YELLOW
            else:
                color = (100, 100, 100)
            
            pygame.draw.circle(screen, color, (node.x, node.y), 15)
            pygame.draw.circle(screen, BLACK, (node.x, node.y), 15, 2)
            
            # Draw level number
            font_small = pygame.font.Font(None, 24)
            num_text = font_small.render(str(node.level_num + 1), True, BLACK)
            screen.blit(num_text, (node.x - num_text.get_width() // 2, 
                                   node.y - num_text.get_height() // 2))
        
        # Draw player marker
        pygame.draw.circle(screen, RED, (int(self.player_pos[0]), 
                                         int(self.player_pos[1])), 8)
        
        # Draw instructions
        font_small = pygame.font.Font(None, 28)
        instructions = font_small.render("Arrow Keys: Move  |  SPACE/ENTER: Select Level", 
                                        True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 
                                   SCREEN_HEIGHT - 40))

class Game:
    """Main game controller."""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Bros Deluxe")
        self.clock = pygame.time.Clock()
        
        self.state = STATE_OVERWORLD
        self.overworld = Overworld()
        self.current_level = None
        self.player = Player()
        self.lives = 3
        
    def start_level(self, level_num):
        """Start playing a level."""
        if level_num < len(LEVELS):
            self.current_level = Level(LEVELS[level_num])
            self.player.reset_position(*self.current_level.start_pos)
            self.state = STATE_LEVEL
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == STATE_OVERWORLD:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.overworld.move_selection(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.overworld.move_selection(1)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.start_level(self.overworld.current_node)
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            elif self.state == STATE_LEVEL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_OVERWORLD
            
            elif self.state in [STATE_GAME_OVER, STATE_VICTORY]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_OVERWORLD
        
        return True
    
    def update(self):
        """Update game state."""
        if self.state == STATE_LEVEL and self.current_level:
            # Update player
            self.player.move()
            died = self.player.update(self.current_level.platforms)
            
            # Update level
            self.current_level.update()
            
            # Check for death
            if died or pygame.sprite.spritecollide(self.player, 
                                                   self.current_level.enemies, False):
                self.lives -= 1
                if self.lives <= 0:
                    self.state = STATE_GAME_OVER
                    self.lives = 3
                else:
                    self.player.reset_position(*self.current_level.start_pos)
            
            # Check for level completion
            if pygame.sprite.spritecollide(self.player, 
                                          self.current_level.goals, False):
                self.overworld.complete_level(self.overworld.current_node)
                if self.overworld.current_node >= len(LEVELS) - 1:
                    self.state = STATE_VICTORY
                else:
                    self.state = STATE_OVERWORLD
    
    def draw(self):
        """Draw the current game state."""
        if self.state == STATE_OVERWORLD:
            self.overworld.draw(self.screen)
        
        elif self.state == STATE_LEVEL:
            self.screen.fill(SKY_BLUE)
            
            # Draw level
            for sprite in self.current_level.all_sprites:
                self.screen.blit(sprite.surf, sprite.rect)
            
            # Draw player
            self.screen.blit(self.player.surf, self.player.rect)
            
            # Draw HUD
            font = pygame.font.Font(None, 36)
            lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
            level_text = font.render(f"Level {self.overworld.current_node + 1}", 
                                    True, BLACK)
            self.screen.blit(lives_text, (10, 10))
            self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        
        elif self.state == STATE_GAME_OVER:
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 72)
            game_over = font.render("GAME OVER", True, RED)
            self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - 50))
            font_small = pygame.font.Font(None, 36)
            continue_text = font_small.render("Press ENTER to return to map", 
                                             True, WHITE)
            self.screen.blit(continue_text, 
                           (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 50))
        
        elif self.state == STATE_VICTORY:
            self.screen.fill(SKY_BLUE)
            font = pygame.font.Font(None, 72)
            victory = font.render("YOU WIN!", True, YELLOW)
            self.screen.blit(victory, (SCREEN_WIDTH // 2 - victory.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 50))
            font_small = pygame.font.Font(None, 36)
            continue_text = font_small.render("You've completed all 32 levels!", 
                                             True, BLACK)
            self.screen.blit(continue_text, 
                           (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

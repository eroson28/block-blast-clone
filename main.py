import os
import random
import pygame

# so the interaction bar on top doesn't start offscreen
os.environ['SDL_VIDEO_WINDOW_POS'] = "20,20"
pygame.init()

# define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
OUTER_BORDER = 30
INNER_BORDER = 30
INNEST_BORDER = 5
TASKBAR_HEIGHT = 200
SQUARE_LENGTH = (SCREEN_WIDTH - (2*OUTER_BORDER) - (2*INNER_BORDER) - (2*INNEST_BORDER) - (7 * INNEST_BORDER)) / 8.0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("block-blast-clone by eroson28")

BLOCK_SHAPES = {
    "2x2square": {
        "rotations": [[[1, 1], [1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    "3x3square": {
        "rotations": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "color": (255, 255, 0),
        "weight": 4
    },
    "I_straight_2": {
        "rotations": [[[1], [1]], [[1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    "I_straight_3": {
        "rotations": [[[1], [1], [1]], [[1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    "I_straight_4": {
        "rotations": [[[1], [1], [1], [1]], [[1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    "I_straight_5": {
        "rotations": [[[1], [1], [1], [1], [1]], [[1, 1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 1
    },
    "L_shape_2": {
        "rotations": [[[1, 0], [1, 1]], [[1, 1], [1, 0]], [[0, 1], [1, 1]], [[1, 1], [0, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    "L_shape_3_1": {
        "rotations": [[[1, 0], [1, 0], [1, 1]], [[0, 1], [0, 1], [1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1], [0, 1], [0, 1]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    "L_shape_3_2": {
        "rotations": [[[1, 0, 0], [1, 0, 0], [1, 1, 1]], [[0, 0, 1], [0, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 0], [1, 0, 0]], [[1, 1, 1], [0, 0, 1], [0, 0, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    "3x3staircase": {
        "rotations": [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[0, 0, 1], [0, 1, 0], [1, 0, 0]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    "2x2staircase": {
        "rotations": [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    "2x3rect": {
        "rotations": [[[1, 1, 1], [1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    "S_shaped": {
        "rotations": [[[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]], [[0, 1], [1, 1], [1, 0]], [[1, 0], [1, 1], [0, 1]]],
        "color": (255, 255, 0),
        "weight": 5
    },
    "T_shaped": {
        "rotations": [[[1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]], [[1, 0], [1, 1], [1, 0]]],
        "color": (255, 255, 0),
        "weight": 3
    }
}

class Block:
    def __init__(self, block_type_name, row, col):
        definition = BLOCK_SHAPES[block_type_name]
        self.color = definition["color"]
        self.rotations = definition["rotations"]
        self.current_rotation_index = 0
        self.shape = self.rotations[self.current_rotation_index] # The active shape

        self.row = row
        self.col = col

        self.height = len(self.shape)
        self.width = len(self.shape[0]) if self.height > 0 else 0

def choose_block():
    # Chooses a random block based on weighted probability
    randomBlock = random.randint(1, len(BLOCK_SHAPES))
    randomWeight = random.randint(1, 5)
    
    while True:
        if BLOCK_SHAPES[randomBlock]['weight'] >= randomWeight:
            return BLOCK_SHAPES[randomBlock]
        else:
            randomBlock = random.randint(1, len(BLOCK_SHAPES))

# pegs stores the binary state of each square. pegRectObjects stores references to 
# the Rect object of each peg at it's respective coordinate
pegs = [[0] * 8 for i in range(8)]
pegRectObjects = [[0] * 8 for i in range(8)]
dragging = False
currentPos = (0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(8):
                    for j in range(8):         
                        if pegRectObjects[i][j].collidepoint(event.pos):
                            dragging = True
                            print("COLLISION")
                            mouse_x, mouse_y = event.pos
                            # TO-DO
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                Block.x = mouse_x + offset_x
                Block.y = mouse_y + offset_y

    # Update frame
    screen.fill("#D8DEE1")
    pygame.draw.rect(screen, "#52759C", (OUTER_BORDER, OUTER_BORDER, (SCREEN_WIDTH - (2 *OUTER_BORDER)), (SCREEN_HEIGHT - TASKBAR_HEIGHT - (2 * OUTER_BORDER))))
    pygame.draw.rect(screen, "#0b274f", (OUTER_BORDER + INNER_BORDER, OUTER_BORDER + INNER_BORDER, SCREEN_WIDTH - (2 *OUTER_BORDER + 2 * INNER_BORDER), SCREEN_HEIGHT - TASKBAR_HEIGHT - (2 *OUTER_BORDER + 2 * INNER_BORDER)))
    pygame.draw.rect(screen, "#143050", (0, SCREEN_HEIGHT - TASKBAR_HEIGHT, SCREEN_WIDTH, TASKBAR_HEIGHT))

    pegs[2][2] = 1;
    # Draw most recent pegboard
    for i in range(8):
        for j in range(8):
            xpos = OUTER_BORDER + INNER_BORDER + INNEST_BORDER + i * (SQUARE_LENGTH + INNEST_BORDER)
            ypos = OUTER_BORDER + INNER_BORDER + INNEST_BORDER + j * (SQUARE_LENGTH + INNEST_BORDER)
            if pegs[i][j] == 0:
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#8f9631ff", (xpos, ypos, SQUARE_LENGTH, SQUARE_LENGTH))
            else:
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#b7d414ff", (xpos, ypos, SQUARE_LENGTH, SQUARE_LENGTH))

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
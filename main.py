import os
import random
import time
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
BORDER_SUM = OUTER_BORDER + INNER_BORDER + INNEST_BORDER
TASKBAR_HEIGHT = 200
SQUARE_LENGTH = (SCREEN_WIDTH - (2*OUTER_BORDER) - (2*INNER_BORDER) - (2*INNEST_BORDER) - (7 * INNEST_BORDER)) / 8.0
SMALL_SQUARE_LENGTH = SQUARE_LENGTH / 4.0
BLOCK_1_DRAWPOS = BORDER_SUM + (SCREEN_WIDTH / 200)
BLOCK_2_DRAWPOS = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 200)
BLOCK_3_DRAWPOS = SCREEN_WIDTH - BLOCK_1_DRAWPOS
BLOCK_DRAW_POSITIONS = {
        0: BLOCK_1_DRAWPOS,
        1: BLOCK_2_DRAWPOS,
        2: BLOCK_3_DRAWPOS
    }
BLOCKSPAWN_HEIGHT = SCREEN_HEIGHT - (TASKBAR_HEIGHT / 1.2) - (SCREEN_HEIGHT / 100)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("block-blast-clone by eroson28")

BLOCK_SHAPES = {
    #2x2square
    0: {
        "rotations": [[[1, 1], [1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    #3x3square
    1: {
        "rotations": [[[1, 1, 1]], [[1, 1, 1]], [[1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    #I_straight_2
    2: {
        "rotations": [[[1], [1]], [[1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    #I_straight_3
    3: {
        "rotations": [[[1], [1], [1]], [[1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    #I_straight_4
    4: {
        "rotations": [[[1], [1], [1], [1]], [[1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    #I_straight_5
    5: {
        "rotations": [[[1], [1], [1], [1], [1]], [[1, 1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "weight": 1
    },
    #L_shape_2
    6: {
        "rotations": [[[1, 0], [1, 1]], [[1, 1], [1, 0]], [[0, 1], [1, 1]], [[1, 1], [0, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    #L_shape_3_1
    7: {
        "rotations": [[[1, 0], [1, 0], [1, 1]], [[0, 1], [0, 1], [1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1], [0, 1], [0, 1]], [[0, 0, 1], [1, 1, 1]], [[1, 0, 0], [1, 1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1, 1], [0, 0, 1]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    #L_shape_3_2
    8: {
        "rotations": [[[1, 0, 0], [1, 0, 0], [1, 1, 1]], [[0, 0, 1], [0, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 0], [1, 0, 0]], [[1, 1, 1], [0, 0, 1], [0, 0, 1]]],
        "color": (255, 255, 0),
        "weight": 2
    },
    #3x3staircase
    9: {
        "rotations": [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[0, 0, 1], [0, 1, 0], [1, 0, 0]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    #2x2staircase
    10: {
        "rotations": [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
        "color": (255, 255, 0),
        "weight": 3
    },
    #2x3rect
    11: {
        "rotations": [[[1, 1, 1], [1, 1, 1]], [[1, 1], [1, 1], [1, 1]]],
        "color": (255, 255, 0),
        "weight": 4
    },
    #S_shaped
    12: {
        "rotations": [[[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]], [[0, 1], [1, 1], [1, 0]], [[1, 0], [1, 1], [0, 1]]],
        "color": (255, 255, 0),
        "weight": 5
    },
    #T_shaped
    13: {
        "rotations": [[[1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]], [[1, 0], [1, 1], [1, 0]]],
        "color": (255, 255, 0),
        "weight": 2
    }
}

class Block:
    def __init__(self, block_index, rotation_index):
        definition = BLOCK_SHAPES[block_index]
        self.color = definition["color"]
        self.shape = definition["rotations"][rotation_index]
        
        self.height = len(self.shape)
        self.width = len(self.shape[0])
        
        print("Shape: " + str(self.shape))
        print("Height:" + str(self.height))
        print("Width: " + str(self.width))

def choose_block():
    # Chooses a random block based on weighted probability
    # Helper function of spawn_block()
    randomBlock = random.randint(0, len(BLOCK_SHAPES) - 1)
    randomWeight = random.randint(1, 5)
    
    while True:
        if BLOCK_SHAPES[randomBlock]["weight"] >= randomWeight:
            numberOfRotations = len(BLOCK_SHAPES[randomBlock]["rotations"])
            randomRotation = random.randint(0, numberOfRotations - 1)
            return (randomBlock, randomRotation)
        else:
            randomBlock = random.randint(0, len(BLOCK_SHAPES) - 1)

def spawn_block(index):
    # Spawns a block and stores it in a rectangle object array
    randomGen = choose_block()
    spawnedBlock = Block(randomGen[0], randomGen[1])
    currentBlocks[index] = spawnedBlock

# GAME VARIABLES
# pegs stores the binary state of each square. pegRectObjects stores references to 
# the Rect object of each peg at it's respective coordinate
pegs = [[0] * 8 for i in range(8)]
pegRectObjects = [[0] * 8 for i in range(8)]
# pegRectObjectsPopulated exists to prevent error from the object 
# list being referenced before it has been populated
pegRectObjectsPopulated = False
dragging = False
currentMousePos = [0, 0]
currentBlocks = [None, None, None]

spawn_block(0)
spawn_block(1)
spawn_block(2)

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
                            Block.row = mouse_x + 1
                            Block.col = mouse_y + 1
                            # TO-DO
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                Block.row = mouse_x + 1
                Block.col = mouse_y + 1
                # TO-DO
            for i in range(8):
                    for j in range(8):
                        if pegRectObjectsPopulated:
                            if pegRectObjects[i][j].collidepoint(event.pos):
                                currentMousePos = [i, j]
                                print(currentMousePos)

    pegs[2][2] = 1;
    
    # Redraw static background
    screen.fill("#D8DEE1")
    pygame.draw.rect(screen, "#52759C", (OUTER_BORDER, OUTER_BORDER, (SCREEN_WIDTH - (2 *OUTER_BORDER)), (SCREEN_HEIGHT - TASKBAR_HEIGHT - (2 * OUTER_BORDER))))
    pygame.draw.rect(screen, "#0b274f", (OUTER_BORDER + INNER_BORDER, OUTER_BORDER + INNER_BORDER, SCREEN_WIDTH - (2 *OUTER_BORDER + 2 * INNER_BORDER), SCREEN_HEIGHT - TASKBAR_HEIGHT - (2 *OUTER_BORDER + 2 * INNER_BORDER)))
    pygame.draw.rect(screen, "#143050", (0, SCREEN_HEIGHT - TASKBAR_HEIGHT, SCREEN_WIDTH, TASKBAR_HEIGHT))

    # Draw most recent pegboard
    for i in range(8):
        for j in range(8):
            x = BORDER_SUM + i * (SQUARE_LENGTH + INNEST_BORDER)
            y = BORDER_SUM + j * (SQUARE_LENGTH + INNEST_BORDER)
            if pegs[i][j] == 0:
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#8f9631ff", (x, y, SQUARE_LENGTH, SQUARE_LENGTH))
            else:
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#b7d414ff", (x, y, SQUARE_LENGTH, SQUARE_LENGTH))
    pegRectObjectsPopulated = True
    
    # Redraw 3 choice pieces
    for i in range(3):
        if currentBlocks[i]:
            for j in range(currentBlocks[i].height):
                for k in range(currentBlocks[i].width):
                    if currentBlocks[i].shape[j][k] == 1:
                        pygame.draw.rect(screen, "#B9C6D5", (BLOCK_DRAW_POSITIONS[i] + (SMALL_SQUARE_LENGTH * 2 * k), BLOCKSPAWN_HEIGHT + (SMALL_SQUARE_LENGTH * 2 * j), SMALL_SQUARE_LENGTH, SMALL_SQUARE_LENGTH))
                    
    clock.tick(60)  # limits FPS to 60

pygame.quit()
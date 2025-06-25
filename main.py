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
BLOCK_2_DRAWPOS = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 30)
BLOCK_3_DRAWPOS = SCREEN_WIDTH - 2 * BLOCK_1_DRAWPOS
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
    
    spawnedBlock.initial_draw_x = BLOCK_DRAW_POSITIONS[index]
    spawnedBlock.initial_draw_y = BLOCKSPAWN_HEIGHT
    spawnedBlock.current_draw_x = BLOCK_DRAW_POSITIONS[index]
    spawnedBlock.current_draw_y = BLOCKSPAWN_HEIGHT
    
    currentBlocks[index] = spawnedBlock
    
    currentBlockRectObjects[index] = [[None for x in range(spawnedBlock.width)] for y in range(spawnedBlock.height)]

def spawn_three_blocks():
    spawn_block(0)
    spawn_block(1)
    spawn_block(2)
    
def check_valid_placement(block):
    for i in range(block.height):
        for j in range(block.width):     
            gridRow = gridMousePos[0] + j - blockMousePos[0]
            gridCol = gridMousePos[1] + i - blockMousePos[1]

            if block.shape[i][j] == 1:
                if gridRow < 0 or gridRow > 7 or gridCol < 0 or gridCol > 7:
                    print("out of bounds")
                    return False
                if pegs[gridRow][gridCol] == 1:
                    print("peg occupied")
                    return False
    return True        
            
def place_block(block):
    if check_valid_placement(block):
        for i in range(block.height):
            for j in range(block.width):     
                gridRow = gridMousePos[0] + j - blockMousePos[0]
                gridCol = gridMousePos[1] + i - blockMousePos[1]
                if block.shape[i][j] == 1:
                    pegs[gridRow][gridCol] = 1
        currentBlocks[currentBlockIndex] = None
    else:
        print("False")
        
def clear_rows():
    global score

    rows_to_clear = []
    cols_to_clear = []

    for row in range(8):
        if all(pegs[col][row] == 1 for col in range(8)):
            rows_to_clear.append(row)

    for col in range(8):
        if all(pegs[col][row] == 1 for row in range(8)):
            cols_to_clear.append(col)

    for row in rows_to_clear:
        for col in range(8):
            pegs[col][row] = 0

    for col in cols_to_clear:
        for row in range(8):
            pegs[col][row] = 0

    score += 10 * (len(rows_to_clear) + len(cols_to_clear))
    
# GAME VARIABLES
pegs = [[0] * 8 for i in range(8)]
pegRectObjects = [[0] * 8 for i in range(8)]
# pegRectObjectsPopulated exists to prevent error from the object 
# list being referenced before it has been populated
pegRectObjectsPopulated = False
dragging = False
draggedBlock = None
currentMousePos = [0, 0]
currentBlocks = [None, None, None]
currentBlockIndex = None
drag_offset_x, drag_offset_y = 0.0, 0.0
currentBlockRectObjects = [[[] for x in range(5)] for y in range(3)]
blockMousePos = [None, None]
# score isn't used yet, but might be in the future
score = 0
spawn_three_blocks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                for i in range(3):
                    if currentBlocks[i] is not None:
                        for j in range(currentBlocks[i].height):
                            for k in range(currentBlocks[i].width):
                                if currentBlockRectObjects[i][j][k] is not None:
                                    if currentBlockRectObjects[i][j][k].collidepoint(event.pos):
                                        dragging = True
                                        draggedBlock = currentBlocks[i]
                                        currentBlockIndex = i
                                        drag_offset_x = draggedBlock.current_draw_x - mouse_x 
                                        drag_offset_y = draggedBlock.current_draw_y - mouse_y
                                        blockMousePos = [k, j]
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging and draggedBlock is not None:        
                    dragging = False
                    place_block(draggedBlock)
                    draggedBlock = None
                if currentBlocks == [None, None, None]:
                    spawn_three_blocks()
                clear_rows()
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if dragging and draggedBlock is not None:
                draggedBlock.current_draw_x = mouse_x + drag_offset_x
                draggedBlock.current_draw_y = mouse_y + drag_offset_y
            for i in range(8):
                    for j in range(8):
                        if pegRectObjectsPopulated:
                            if pegRectObjects[i][j].collidepoint(event.pos):
                                gridMousePos = [i, j]
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(8):
                    for j in range(8):
                        pegs[i][j] = 0
                score = 0
                currentBlocks = [None, None, None]
                spawn_three_blocks()
    
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
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#636823ff", (x, y, SQUARE_LENGTH, SQUARE_LENGTH))
            else:
                pegRectObjects[i][j] = pygame.draw.rect(screen, "#b7d414ff", (x, y, SQUARE_LENGTH, SQUARE_LENGTH))
    pegRectObjectsPopulated = True
    
    # Redraw 3 choice pieces
    for i in range(3):
        if currentBlocks[i]:
            current_x = currentBlocks[i].current_draw_x
            current_y = currentBlocks[i].current_draw_y
            for j in range(currentBlocks[i].height):
                for k in range(currentBlocks[i].width):
                    if currentBlocks[i].shape[j][k] == 1:
                        currentBlockRectObjects[i][j][k] = pygame.draw.rect(screen, "#B9C6D5", (current_x + (SMALL_SQUARE_LENGTH * 1.3 * k), current_y + (SMALL_SQUARE_LENGTH * 1.3 * j), SMALL_SQUARE_LENGTH, SMALL_SQUARE_LENGTH))
                    
    clock.tick(60)  # limits FPS to 60
    pygame.display.flip()
    
pygame.quit()
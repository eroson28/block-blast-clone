import os
import pygame
import random

# so the interaction bar on top doesn't start offscreen
os.environ['SDL_VIDEO_WINDOW_POS'] = "20,20"
pygame.init()

# define constants
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 1000
outerBorder = 30
innerBorder = 30
innestBorder = 5
taskbarHeight = 200
squareLength = (screenWidth - (2*outerBorder) - (2*innerBorder) - (2*innestBorder) - (7 * innestBorder)) / 8.0
screen = pygame.display.set_mode((screenWidth, screenHeight))

BLOCK_SHAPES = {
    "2x2square": {
        "rotations": [[1, 1], [1, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "3x3square": {
        "rotations": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
        
    },
    "I_straight_2": {
        "rotations": [[[1], [1]], [[1, 1]]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "I_straight_3": {
        "rotations": [[[1], [1], [1]], [[1, 1, 1]]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "I_straight_4": {
        "rotations": [[[1], [1], [1], [1]], [[1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "I_straight_5": {
        "rotations": [[[1], [1], [1], [1], [1]], [[1, 1, 1, 1, 1]]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "L_shape_2": {
        "shape": [[1, 0], [1, 1]], [[1, 1], [1, 0]], [[0, 1], [1, 1]], [[1, 1], [1, 0]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "L_shape_3_1": {
        "shape": [[1, 0, 0], [1, 0, 0], [1, 1, 0]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "L_shape_3_2": {
        "shape": [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "3x3staircase": {
        "shape": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "2x2staircase": {
        "shape": [[1, 0], [0, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "2x3rect": {
        "shape": [[1, 1, 1], [1, 1, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "S_shaped": {
        "shape": [[1, 1, 0], [0, 1, 1]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    },
    "T_shaped": {
        "shape": [[1, 1, 1], [0, 1, 0]],
        "color": (255, 255, 0),
        "probability": 100 / 14.0
    }
}

class Block:
    def __init__(self, shape, color, row, col):
        self.shape = shape 
        self.color = color
        self.row = row      # Top-left corner grid row
        self.col = col      # Top-left corner grid column

pygame.display.set_caption("test")
pegs = [[0] * 8 for i in range(8)]

running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#D8DEE1")
    pygame.draw.rect(screen, "#52759C", (outerBorder, outerBorder, (screenWidth - (2 *outerBorder)), (screenHeight - taskbarHeight - (2 * outerBorder))))
    pygame.draw.rect(screen, "#0b274f", (outerBorder + innerBorder, outerBorder + innerBorder, screenWidth - (2 *outerBorder + 2 * innerBorder), screenHeight - taskbarHeight - (2 *outerBorder + 2 * innerBorder)))
    pygame.draw.rect(screen, "#143050", (0, screenHeight - taskbarHeight, screenWidth, taskbarHeight))

    pegs[2][2] = 1;
    # RENDER YOUR GAME HERE
    for i in range(8):
        for j in range(8):
            xpos = outerBorder + innerBorder + innestBorder + i * (squareLength + innestBorder)
            ypos = outerBorder + innerBorder + innestBorder + j * (squareLength + innestBorder)
            if pegs[i][j] == 0:
                pygame.draw.rect(screen, "#8f9631ff", (xpos, ypos, squareLength, squareLength))
            else:
                pygame.draw.rect(screen, "#b7d414ff", (xpos, ypos, squareLength, squareLength))

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
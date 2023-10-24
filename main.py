import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 700
GAME_WIDTH, GAME_HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPE_COLORS = [
    # purple 
    (64, 0, 128),
    (64, 0, 128),
    (64, 0, 128),
    (64, 0, 128),
    # yellow 
    (255, 213, 0),
    (255, 213, 0),
    (255, 213, 0),
    (255, 213, 0),
    # red 
    (255, 0, 0),
    (255, 0, 0),
    (255, 0, 0),
    (255, 0, 0),
    # green 
    (0, 255, 0),
    (0, 255, 0),
    (0, 255, 0),
    (0, 255, 0),
    # light blue 
    (0, 192, 255),
    (0, 192, 255),
    (0, 192, 255),
    (0, 192, 255),
    # dark blue 
    (0, 0, 255),
    (0, 0, 255),
    (0, 0, 255),
    (0, 0, 255),
    # orange 
    (255,100,0),
    (255,100,0),
    (255,100,0),
    (255,100,0)
    ]
SHAPES = [
    # purple
    [[1, 1, 1], 
     [0, 1, 0]], # down
    [[0, 1], 
     [1, 1], 
     [0, 1]], # left
    [[0, 1, 0], 
     [1, 1, 1]], # up
    [[1, 0], 
     [1, 1], 
     [1, 0]], # right
    # yellow
    [[1, 1], 
     [1, 1]],
    [[1, 1], 
     [1, 1]],
    [[1, 1], 
     [1, 1]],
    [[1, 1], 
     [1, 1]],
    # red
    [[1, 1, 0],
     [0, 1, 1]], # horizontal
    [[0, 1],
     [1, 1],
     [1, 0]], # vertical
    [[1, 1, 0],
     [0, 1, 1]], # horizontal
    [[0, 1],
     [1, 1],
     [1, 0]], # vertical
    # green
    [[0, 1, 1],
     [1, 1, 0]], # horizontal
    [[1, 0],
     [1, 1],
     [0, 1]], # vertical
    [[0, 1, 1],
     [1, 1, 0]], # horizontal
    [[1, 0],
     [1, 1],
     [0, 1]], # vertical
     # light blue
    [[1, 1, 1, 1]], # horizontal
    [[1], 
     [1], 
     [1], 
     [1]], # vertical
    [[1, 1, 1, 1]], # horizontal
    [[1], 
     [1], 
     [1], 
     [1]], # vertical
    # dark blue
    [[1, 1, 1], 
     [0, 0, 1]], # down
    [[0, 1],
     [0, 1],
     [1, 1]], # left
    [[1, 0, 0], 
     [1, 1, 1]], # up
    [[1, 1],
     [1, 0],
     [1, 0]], # right
     # orange
    [[1, 1, 1], 
     [1, 0, 0]], # down
    [[1, 1],
     [0, 1],
     [0, 1]], # left
    [[0, 0, 1],
     [1, 1, 1]], # up
    [[1, 0],
     [1, 0],
     [1, 1]] # right
]

scoring = {
    0: 0,
    1: 100,
    2: 300,
    3: 500,
    4: 800
}

# Initialize variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def draw_grid(grid):
    for x in range(0, GAME_WIDTH+BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT+BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (GAME_WIDTH, y))
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, SHAPE_COLORS[cell-1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_shape(shape, offset):
    shape_color = SHAPE_COLORS[SHAPES.index(shape)]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, shape_color, (offset[0] * BLOCK_SIZE + x * BLOCK_SIZE, offset[1] * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_next(up_next):
    shape_color = SHAPE_COLORS[SHAPES.index(up_next)]
    x = GAME_WIDTH+5
    y = 5
    pygame.draw.rect(screen, WHITE, (x, y, BLOCK_SIZE*3, BLOCK_SIZE*3), 2)
    for row in range(len(up_next)):
        for col in range(len(up_next[0])):
            if up_next[row][col]:
                pygame.draw.rect(screen, shape_color, (x + 10 + col * 15, y + 10 + row * 15, 15, 15))

def draw_saved(saved):
    x = GAME_WIDTH+5
    y = 10 + BLOCK_SIZE*3
    pygame.draw.rect(screen, WHITE, (x, y, BLOCK_SIZE*3, BLOCK_SIZE*3), 2)
    if saved:
        shape_color = SHAPE_COLORS[SHAPES.index(saved)]
        for row in range(len(saved)):
            for col in range(len(saved[0])):
                if saved[row][col]:
                    pygame.draw.rect(screen, shape_color, (x + 10 + col * 15, y + 10 + row * 15, 15, 15))

def show_points(points):
    shape_color = SHAPE_COLORS[SHAPES.index(up_next)]
    x = 5
    y = GAME_HEIGHT+5
    w = BLOCK_SIZE*6
    h = BLOCK_SIZE*3
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Score: {points}", True, WHITE)
    screen.blit(text_surface, (x + w/4, y + h/4))

def check_collision(shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if offset[1] + y >= len(grid) or offset[0] + x < 0 or offset[0] + x >= len(grid[0]) or grid[offset[1] + y][offset[0] + x]:
                    return True
    return False

def merge_shape(shape, offset):
    idx = SHAPES.index(shape)+1
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[offset[1] + y][offset[0] + x] = idx

def remove_full_lines(last_tetris):
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    num_lines = len(full_lines)
    points = scoring[num_lines]
    if num_lines == 4:
        if last_tetris:
            points += 400
        last_tetris = True
    else:
        last_tetris = False
    for index in full_lines:
        del grid[index]
        grid.insert(0, [0 for _ in range(GAME_WIDTH // BLOCK_SIZE)])
    return points

def hard_drop():
    new_offset = [current_shape_offset[0], current_shape_offset[1]]
    while not check_collision(current_shape, [current_shape_offset[0], new_offset[1]+1]):
        new_offset[1] += 1
    return new_offset

def game_over():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (GAME_WIDTH // 2 - game_over_text.get_width() // 2, GAME_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

grid = [[0 for _ in range(GAME_WIDTH // BLOCK_SIZE)] for _ in range(GAME_HEIGHT // BLOCK_SIZE)]

current_shape = random.choice(SHAPES)
up_next = random.choice(SHAPES)
saved = None
points = 0
current_shape_offset = [GAME_WIDTH // 2 // BLOCK_SIZE - len(current_shape[0]) // 2, 0]
fall_time = 0
last_tetris = False
game_over_flag = False

while not game_over_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_flag = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_offset = [current_shape_offset[0] - 1, current_shape_offset[1]]
                if not check_collision(current_shape, new_offset):
                    current_shape_offset = new_offset
            elif event.key == pygame.K_RIGHT:
                new_offset = [current_shape_offset[0] + 1, current_shape_offset[1]]
                if not check_collision(current_shape, new_offset):
                    current_shape_offset = new_offset
            elif event.key == pygame.K_DOWN:
                new_offset = [current_shape_offset[0], current_shape_offset[1] + 1]
                if not check_collision(current_shape, new_offset):
                    current_shape_offset = new_offset
            elif event.key == pygame.K_UP:
                new_shape = [[current_shape[y][x] for y in range(len(current_shape))] for x in range(len(current_shape[0]) - 1, -1, -1)]
                if not check_collision(new_shape, current_shape_offset):
                    current_shape = new_shape
            elif event.key == pygame.K_SPACE:
                if saved:
                    new_shape = saved
                    saved = current_shape
                    if not check_collision(new_shape, current_shape_offset):
                        current_shape = new_shape
                    
                else:
                    saved = current_shape
                    new_shape = up_next
                    up_next = random.choice(SHAPES)
                    if not check_collision(new_shape, current_shape_offset):
                        current_shape = new_shape
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                current_shape_offset = hard_drop()


    screen.fill(BLACK)

    # Move shape down
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time / 1000 > 1:
        fall_time = 0
        new_offset = [current_shape_offset[0], current_shape_offset[1] + 1]
        if not check_collision(current_shape, new_offset):
            current_shape_offset = new_offset
        else:
            merge_shape(current_shape, current_shape_offset)
            points += remove_full_lines(last_tetris)
            current_shape = up_next
            up_next = random.choice(SHAPES)
            current_shape_offset = [GAME_WIDTH // 2 // BLOCK_SIZE - len(current_shape[0]) // 2, 0]
            if check_collision(current_shape, current_shape_offset):
                game_over()

    # Draw grid and current shape
    draw_grid(grid)
    draw_shape(current_shape, current_shape_offset)
    draw_next(up_next)
    draw_saved(saved)
    show_points(points)

    pygame.display.flip()

pygame.quit()
quit()
import pygame
import time
import random
import math

(HEIGHT, WIDTH) = (500, 500)
BLOCK_SIZE = 10

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen.fill(0xffffff)

def reload():
    """Reload screen changes"""
    pygame.display.flip()

def draw(x, y, color=0xddd):
    """Draw a pixel on the screen"""
    global screen
    pxl = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, pxl)
    reload()

def draw_pixels(pixels, color=0xddd, is_clear=False):
    """Draw many pixels on the screen"""
    for i, (x, y) in enumerate(pixels):
        # Head
        if i == 0 and not is_clear:
            draw(x, y, color=0x9213bd)
        else:
            draw(x, y, color=color)

def move_x(x, pos):
    poses = ["RIGHT", "LEFT"]
    nums = [1, -1]
    return (x + nums[poses.index(pos)]) % (WIDTH/BLOCK_SIZE)  # Go over screen bounds

def move_y(y, pos):
    poses = ["DOWN", "UP"]
    nums = [1, -1]
    return (y + nums[poses.index(pos)]) % (HEIGHT/BLOCK_SIZE)  # Go over screen bounds

def new_apple():
    global snake

    snake_blocks = [(x, y) for x, y, _ in snake]

    valid_blocks = []
    for x in range(math.floor(WIDTH / BLOCK_SIZE)):
        for y in range(math.floor(HEIGHT / BLOCK_SIZE)):
            if (x, y) not in snake_blocks:
                valid_blocks.append((x, y))

    x, y = random.choice(valid_blocks)
    draw(x, y, color=0xed3948)
    return (x, y)

snake_size = 6
snake = [(0, i, "DOWN") for i in range(snake_size)][::-1]
apple = new_apple()

print(f'Apple: {apple}')
print(f'Snake Size: {len(snake)}')

last_run = time.time()
score = 0
snake_speed = .1


while True:
    draw(*apple, color=0xed3948)
    new_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()  # Exit button

        # Arrow keys < ^ V >
        if event.type == pygame.KEYDOWN:
            keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
            if event.key in keys:
                names = ["UP", "DOWN", "RIGHT", "LEFT"]
                tmp_pos = names[keys.index(event.key)]
                if not ((tmp_pos in ["UP", "DOWN"] and snake[0][2] in ["UP", "DOWN"])
                        or (tmp_pos in ["RIGHT", "LEFT"] and snake[0][2] in ["RIGHT", "LEFT"])):
                    new_pos = tmp_pos

    if (time.time() - last_run) > snake_speed or new_pos:
        last_run = time.time()

        # Clear last snake block
        draw(snake[-1][0], snake[-1][1], color=0xffffff)

        # Move snake
        new_snake = []
        for i, (x, y, pos) in enumerate(snake):
            new_snake.append((
                move_x(x, pos) if pos in ["RIGHT", "LEFT"] else x,
                move_y(y, pos) if pos in ["DOWN", "UP"] else y,
                (new_pos or pos) if (i == 0) else (snake[i-1][2])
            ))

        # Collides with itself
        if new_snake[0][:2] in [(x, y) for x, y, _ in new_snake[1:]]:
            screen.fill(0x8a0101)
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text = font.render('You lost!', True, (255, 255, 255, 1))
            rect = text.get_rect(center=(WIDTH/2, HEIGHT/3))
            screen.blit(text, rect)
            text = font.render(f'Score: {score}', True, (120, 255, 190, 1))
            rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text, rect)

            reload()
            break

        # Collides with apple
        if apple in [(x, y) for x, y, _ in new_snake]:
            score += 1
            snake_speed -= random.choice([.004, 0])
            pygame.display.set_caption(f'Score: {score}')

            lx, ly, lpos = new_snake[-1]
            cx, cy, cpos = None, None, None

            if lpos == "RIGHT": cx = lx-1; cpos = "RIGHT"
            elif lpos == "LEFT": cx = lx+1; cpos = "LEFT"
            elif lpos == "UP": cy = ly+1; cpos = "UP"
            elif lpos == "DOWN": cy = ly-1; cpos = "DOWN"

            if not cx: cx = lx
            if not cy: cy = ly

            new_snake.append((cx, cy, lpos))
            draw(*apple, color=0xffffff)
            apple = new_apple()


        # Draw new snake
        snake = new_snake
        draw_pixels([(x, y) for (x, y, _) in snake])


while 1:  # Lost
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()  # Exit button

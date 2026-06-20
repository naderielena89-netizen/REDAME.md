import pygame
import random #این خط برای اینه که غذای مار به طور رندوم و تصادفی انتخاب بشه
import sys #این خط اینجا باز میشه و توی خط اخر بسته میشه تا بازی بعد از باخت کامل تموم بشه

# -----------------------------
# تنظیمات اولیه
# -----------------------------
pygame.init() # این خط برای اینه که تمام ماژول ها و تمام ابزار های پای گیم باز بشه که بتونه چیزهایی مثل کیبورد  و کنترل کنه

WIDTH, HEIGHT = 600, 400 #عرض و ارتفاع صفحه بازی به طور پیکسل تعریف میشود
GRID_SIZE = 20 #اندازه هر گرید
FPS = 6 #سرعت*

WHITE = (255, 255, 255) #رنگ ها را با کد rgb نوشته شده
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 0, 0)
GRAY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 36)


# -----------------------------
# توابع کمکی
# -----------------------------
def draw_text(text, color, x, y, font_obj):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


def random_food_position():
    x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    return [x, y]


def reset_game():
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = [GRID_SIZE, 0]
    next_direction = direction[:]
    food = random_food_position()
    score = 0
    game_over = False
    return snake, direction, next_direction, food, score, game_over


# -----------------------------
# شروع بازی
# -----------------------------
snake, direction, next_direction, food, score, game_over = reset_game()

# -----------------------------
# حلقه اصلی بازی
# -----------------------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != [0, GRID_SIZE]:
                    next_direction = [0, -GRID_SIZE]
                elif event.key == pygame.K_DOWN and direction != [0, -GRID_SIZE]:
                    next_direction = [0, GRID_SIZE]
                elif event.key == pygame.K_LEFT and direction != [GRID_SIZE, 0]:
                    next_direction = [-GRID_SIZE, 0]
                elif event.key == pygame.K_RIGHT and direction != [-GRID_SIZE, 0]:
                    next_direction = [GRID_SIZE, 0]
            else:
                if event.key == pygame.K_r:
                    snake, direction, next_direction, food, score, game_over = reset_game()

    if not game_over:
        direction = next_direction[:]
        head_x, head_y = snake[0]
        new_head = [head_x + direction[0], head_y + direction[1]]
        snake.insert(0, new_head)

        # برخورد با غذا
        if snake[0] == food:
            score += 1
            food = random_food_position()
        else:
            snake.pop()

        # برخورد با دیوار
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            game_over = True

        # برخورد با خودش
        if snake[0] in snake[1:]:
            game_over = True

    # -----------------------------
    # رسم روی صفحه
    # -----------------------------
    screen.fill(BLACK)

    # شبکه پس‌زمینه
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # غذا
    pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

    # مار
    for i, part in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (part[0], part[1], GRID_SIZE, GRID_SIZE))

    # امتیاز
    draw_text(f"Score: {score}", WHITE, 10, 10, font)

    # صفحه پایان
    if game_over:
        draw_text("Game Over", WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 40, big_font)
        draw_text("Press R to Restart", WHITE, WIDTH // 2 - 120, HEIGHT // 2 + 10, font)

    pygame.display.flip()

pygame.quit()
sys.exit()

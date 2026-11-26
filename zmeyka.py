import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна и сетки
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 12

# Цвета (RGB)
BLACK = (20, 20, 20)
GRID_COLOR = (45, 45, 45)  # Цвет линий сетки
GREEN = (0, 220, 90)
DARK_GREEN = (0, 150, 60)
RED = (230, 60, 60)
WHITE = (240, 240, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка на Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)


def draw_grid():
    """Отрисовывает сетку игрового поля."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def get_random_food(snake_body):
    """Генерирует координаты еды, не совпадающие с телом змейки."""
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake_body:
            return (x, y)


def show_game_over(score):
    """Отображает экран проигрыша и ждет перезапуска или выхода."""
    screen.fill(BLACK)
    msg_over = font.render(f"Игра окончена! Счет: {score}", True, RED)
    msg_restart = font.render("Нажмите R для рестарта или Q для выхода", True, WHITE)

    screen.blit(msg_over, (WIDTH // 2 - msg_over.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(msg_restart, (WIDTH // 2 - msg_restart.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    while True:
        # Начальные параметры змейки
        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = (CELL_SIZE, 0)
        food = get_random_food(snake)
        score = 0
        running = True

        while running:
            # 1. Обработка событий (Стрелки + WASD)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

            # 2. Обновление координат головы
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # 3. Проверка столкновений со стенами и с собой
            if (
                new_head[0] < 0
                or new_head[0] >= WIDTH
                or new_head[1] < 0
                or new_head[1] >= HEIGHT
                or new_head in snake
            ):
                running = False
                continue

            snake.insert(0, new_head)

            # 4. Проверка поедания еды
            if new_head == food:
                score += 10
                food = get_random_food(snake)
            else:
                snake.pop()

            # 5. Отрисовка объектов
            screen.fill(BLACK)
            draw_grid()  # Рисуем сетку поверх фона

            # Еда (с небольшим отступом, чтобы не перекрывать границы клетки)
            pygame.draw.rect(screen, RED, (food[0] + 1, food[1] + 1, CELL_SIZE - 1, CELL_SIZE - 1))

            # Змейка
            for index, segment in enumerate(snake):
                color = GREEN if index == 0 else DARK_GREEN
                pygame.draw.rect(screen, color, (segment[0] + 1, segment[1] + 1, CELL_SIZE - 1, CELL_SIZE - 1))

            # Счет
            score_text = font.render(f"Счет: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        if not show_game_over(score):
            break


if __name__ == "__main__":
    main()

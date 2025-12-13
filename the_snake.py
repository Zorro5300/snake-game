import random
from typing import Optional, Tuple

import pygame

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self,
        position: Optional[Tuple[int, int]] = None,
        body_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        Инициализирует игровой объект.

        Args:
            position: Начальная позиция объекта. Если None - центр экрана
            body_color: Цвет объекта. Если None - белый
        """
        self.position = position if position else (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        self.body_color = body_color if body_color else WHITE

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод для отрисовки объекта.

        Args:
            surface: Поверхность для отрисовки
        """
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайную позицию для яблока."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на игровом поле.

        Args:
            surface: Поверхность для отрисовки
        """
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_position = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки.

        Returns:
            Координаты головы змейки (x, y)
        """
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            current_x, current_y = self.direction
            next_x, next_y = self.next_direction

            if not (current_x + next_x == 0 and current_y + next_y == 0):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки, двигая её в текущем направлении."""
        head_x, head_y = self.get_head_position()

        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.last_position = self.positions[-1] if self.positions else None

        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self) -> None:
        """Увеличивает длину змейки на 1 сегмент."""
        self.length += 1

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_position = None

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на игровом поле.

        Args:
            surface: Поверхность для отрисовки
        """
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)

            if i == 0:
                pygame.draw.rect(surface, (0, 200, 0), rect)
                eye_size = GRID_SIZE // 5
                if self.direction == RIGHT:
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + GRID_SIZE - eye_size, pos[1] + eye_size),
                        eye_size
                    )
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + GRID_SIZE - eye_size,
                         pos[1] + GRID_SIZE - eye_size),
                        eye_size
                    )
                elif self.direction == LEFT:
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + eye_size, pos[1] + eye_size),
                        eye_size
                    )
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + eye_size, pos[1] + GRID_SIZE - eye_size),
                        eye_size
                    )
                elif self.direction == UP:
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + eye_size, pos[1] + eye_size),
                        eye_size
                    )
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + GRID_SIZE - eye_size, pos[1] + eye_size),
                        eye_size
                    )
                elif self.direction == DOWN:
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + eye_size, pos[1] + GRID_SIZE - eye_size),
                        eye_size
                    )
                    pygame.draw.circle(
                        surface, WHITE,
                        (pos[0] + GRID_SIZE - eye_size,
                         pos[1] + GRID_SIZE - eye_size),
                        eye_size
                    )
            else:
                color_value = max(50, 255 - i * 10)
                segment_color = (0, color_value, 0)
                pygame.draw.rect(surface, segment_color, rect)

            pygame.draw.rect(surface, (0, 150, 0), rect, 1)

        if self.last_position:
            erase_rect = pygame.Rect(
                self.last_position[0], self.last_position[1],
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, BACKGROUND_COLOR, erase_rect)


def handle_keys(snake: Snake, event: pygame.event.Event) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой.

    Args:
        snake: Объект змейки
        event: Событие клавиатуры
    """
    if event.key == pygame.K_UP:
        snake.next_direction = UP
    elif event.key == pygame.K_DOWN:
        snake.next_direction = DOWN
    elif event.key == pygame.K_LEFT:
        snake.next_direction = LEFT
    elif event.key == pygame.K_RIGHT:
        snake.next_direction = RIGHT


def draw_score(surface: pygame.Surface, score: int) -> None:
    """Отрисовывает счет на экране.

    Args:
        surface: Поверхность для отрисовки
        score: Текущий счет
    """
    font = pygame.font.Font(None, 36)
    text = font.render(f'Счет: {score}', True, WHITE)
    surface.blit(text, (10, 10))


def draw_grid(surface: pygame.Surface) -> None:
    """Отрисовывает сетку на игровом поле.

    Args:
        surface: Поверхность для отрисовки
    """
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


def main() -> None:
    """Основная функция игры. Содержит главный игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка - Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keys(snake, event)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            score += 1

            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)
        draw_score(screen, score)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
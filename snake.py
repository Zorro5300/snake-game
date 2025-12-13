import random
from typing import Optional, Tuple

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)

screen = None
clock = None


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position: Optional[Tuple[int, int]] = None):
        """Инициализирует базовые атрибуты объекта."""
        if position is None:
            self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        else:
            self.position = position
        self.body_color = None

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__()
        self.body_color = (0, 255, 0)
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
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
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.last = self.positions[-1] if self.positions else None

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
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (0, 200, 0), rect, 1)

        if self.last:
            erase_rect = pygame.Rect(
                self.last[0],
                self.last[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, erase_rect)


def handle_keys(snake: Snake, event: pygame.event.Event) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    if event.key == pygame.K_UP:
        snake.next_direction = (0, -1)
    elif event.key == pygame.K_DOWN:
        snake.next_direction = (0, 1)
    elif event.key == pygame.K_LEFT:
        snake.next_direction = (-1, 0)
    elif event.key == pygame.K_RIGHT:
        snake.next_direction = (1, 0)


def main() -> None:
    """Основная функция игры."""
    global screen, clock

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    snake = Snake()
    apple = Apple()
    clock = pygame.time.Clock()
    running = True

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

            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()


if __name__ == '__main__':
    main()

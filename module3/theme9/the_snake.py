from random import randint
from typing import List, Tuple

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс представляющий игровой объект"""

    def __init__(self) -> None:
        self.position: Tuple[int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """
        Абстрактный метод для отрисовки игрового объекта.

        Должен быть реализован в подклассах, чтобы определять
        логику отрисовки конкретного объекта на экране.
        """
        pass


# Тут опишите все классы игры.
class Snake(GameObject):
    """Game object - Snake"""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions: List[Tuple[int]] = [self.position]
        self.last = None
        self.direction: Tuple[int] = RIGHT
        self.next_direction = None
        self.body_color: Tuple[int] = SNAKE_COLOR

    def draw(self) -> None:
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow=False) -> None:
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        current_head_position = self.get_head_position()
        new_head_position = (
            current_head_position[0] + self.direction[0] * GRID_SIZE,
            current_head_position[1] + self.direction[1] * GRID_SIZE,
        )

        if new_head_position[0] < 0:
            new_head_position = (
                SCREEN_WIDTH - GRID_SIZE,
                new_head_position[1],
            )
        elif new_head_position[0] >= SCREEN_WIDTH:
            new_head_position = (
                0,
                new_head_position[1],
            )
        elif new_head_position[1] < 0:
            new_head_position = (
                new_head_position[0],
                SCREEN_HEIGHT - GRID_SIZE,
            )
        elif new_head_position[1] >= SCREEN_HEIGHT:
            new_head_position = (
                new_head_position[0],
                0,
            )

        self.positions.insert(0, new_head_position)
        if not grow:
            self.positions.pop()

    def get_head_position(self) -> Tuple[int]:
        """
        возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self) -> None:
        """
        сбрасывает змейку в начальное состояние
        после столкновения с собой
        """
        self.length = 1
        self.positions: List[Tuple[int]] = [self.position]
        self.last = None
        self.direction: Tuple[int] = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Game object - Apple"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> Tuple[int]:
        """
        Устанавливает случайное положение яблока на игровом поле.
        Координаты выбираются так, чтобы яблоко оказалось в пределах
        игрового поля, и были кратны размеру сетки GRID_SIZE.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Функция обработки действий пользователя
def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main function"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)

        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.move(grow=True)
            apple.position = apple.randomize_position()
        else:
            snake.move()

        snake.draw()
        apple.draw()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()

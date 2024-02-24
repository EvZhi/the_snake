from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Ценральная точка экрана
DEFAULT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет базового игрового класса
DEFAULT_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
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


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=DEFAULT_POSITION, body_color=DEFAULT_COLOR):
        """Инициализация базовых атрибутов игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки игровых объектов."""
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}.'
        )

    def draw_cell(self, cell_position, cell_size=GRID_SIZE):
        """Метод отрисовки ячейки игрового объекта."""
        return pygame.Rect(
            cell_position,
            (cell_size, cell_size)
        )


class Snake(GameObject):
    """Класс игрового объекта - Змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация атрибутов Змейки."""
        super().__init__()
        # Цвет змейки
        self.body_color = body_color
        # Длинна змейки
        self.length = 1
        # Позиции ячеек тела змейки:
        self.positions = [self.position]
        # Направление движения змейки. По умолчанию - вправо
        self.direction = RIGHT
        # Следующее направление движения змейки
        self.next_direction = None
        # Позиция последней ячейки тела змейки - хвоста
        self.last = None

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле."""
        # Отрисовка головы змейки
        head_rect = self.draw_cell(self.positions[0])
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание хвоста змейки
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возращающий позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод описывающий логику движения змейки"""
        head_position = self.get_head_position()

        new_position_head = (
            (head_position[0] + (self.direction[0]
             * GRID_SIZE)) % SCREEN_WIDTH,
            (head_position[1] + (self.direction[1]
             * GRID_SIZE)) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_position_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Метод обновления направления движения Змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self. direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс игрового объекта - Яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__(body_color)
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self, snake_pos=[DEFAULT_POSITION]):
        """Метод опредления рандомной позиции яблока"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position in snake_pos:
                continue
            else:
                break

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле."""
        rect = self.draw_cell(self.position)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def main():
    """Главная функция игры - точка входа"""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()

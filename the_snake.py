from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
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

# Цвет камня
ROCK_COLOR = (192, 192, 192)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Создаем класс ИгровойОбъект"""

    def __init__(self) -> None:
        self.position = SCREEN_CENTER
        self.body_color = None

    def draw(self):
        """Метод отрисовки"""
        pass


class Apple(GameObject):
    """Создаем подкласс Яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self, *args):
        """Метод рандомизации координат яблока"""
        new_position = (
            ((randint(0, GRID_WIDTH - 1)) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1)) * GRID_SIZE,
        )
        if new_position not in SCREEN_CENTER and new_position not in args:
            self.position = new_position

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Rock(GameObject):
    """Создаем подкласс Камень"""

    def __init__(self):
        super().__init__()
        self.body_color = ROCK_COLOR
        self.positions = []
        self.randomize_position()

    def draw(self):
        """Метод отрисовки камня"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, *args):
        """Метод рандомизации координат камня"""
        new_position = (
            ((randint(0, GRID_WIDTH - 1)) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1)) * GRID_SIZE,
        )
        if new_position not in SCREEN_CENTER and new_position not in args:
            self.position = new_position
        self.positions.append(new_position)


class Snake(GameObject):
    """Создаем подкласс Змейка"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Метод определения следующего направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод определения координат "головы" змейки"""
        return self.positions[0]

    def move(self):
        """Метод определения алгоритма движения змейки"""
        self.update_direction()
        x, y = self.get_head_position()
        # Распаковка кортежа координат головы змейки
        delta_x, delta_y = self.direction

        if self.direction == UP or self.direction == DOWN:
            y = (y + delta_y * GRID_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT

        elif self.direction == RIGHT or self.direction == LEFT:
            x = (x + delta_x * GRID_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH
        next_position = (x, y)
        # Удаление последнего элемента из списка позиций
        # змейки, если яблоко не съедено
        if self.lenght <= len(self.positions):
            self.positions.insert(0, next_position)
            self.last = self.positions.pop()
        else:
            self.positions.insert(0, next_position)

    def reset(self):
        """Метод сброса игры"""
        self.lenght = 1
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        directions = [RIGHT, LEFT, UP, DOWN]
        self.next_direction = choice(directions)

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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


def handle_keys(game_object):
    """Функция взаимодействия с клавишами управления"""
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
    """Основная логика игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    rock = Rock()
    rock_created = False
    while True:
        clock.tick(SPEED)
        snake.draw()
        apple.draw()
        snake.move()
        rock.draw()
        handle_keys(snake)
        if snake.lenght % 10 == 0 and rock_created is False:
            rock.randomize_position(snake.positions, apple.position)
            rock.draw()
            rock_created = True
        if apple.position == snake.get_head_position():
            snake.lenght += 1
            apple.randomize_position(snake.positions, rock.positions)
            if snake.lenght % 10 != 0:
                rock_created = False
        if (
            snake.get_head_position() in snake.positions[1:]
            or snake.get_head_position() in rock.positions
        ):
            snake.reset()
            rock.positions = []
            apple.randomize_position(snake.positions)
            rock.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()

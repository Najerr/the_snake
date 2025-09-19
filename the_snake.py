from random import choice, randint

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Создаем класс ИгровойОбъект"""

    def __init__(
        self,
        position: tuple = SCREEN_CENTER,
        body_color=None
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заглушка метода отрисовки родительского класса"""
        pass


class Apple(GameObject):
    """Создаем подкласс Яблоко"""

    def __init__(
        self,
        position: tuple = SCREEN_CENTER,
        body_color: tuple = APPLE_COLOR,
        restricted_area=None,
    ):
        super().__init__(position, body_color)
        self.restricted_area = restricted_area or []
        self.randomize_position(restricted_area)

    def randomize_position(self, restricted_area):
        """Метод рандомизации координат яблока"""
        while True:
            self.position = (
                ((randint(0, GRID_WIDTH - 1)) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1)) * GRID_SIZE,
            )
            if self.position not in self.restricted_area:
                return self.position
            break

    def draw(self, body_color=None):
        """Метод отрисовки"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        if not body_color:
            pg.draw.rect(screen, self.body_color, rect)
        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Rock(Apple):
    """Создаем подкласс Камень"""

    def __init__(
        self,
        position: tuple = SCREEN_CENTER,
        body_color: tuple = ROCK_COLOR,
        restricted_area=None,
    ):
        super().__init__(position, body_color, restricted_area)


class Snake(GameObject):
    """Создаем подкласс Змейка"""

    def __init__(
        self, position: tuple = SCREEN_CENTER, body_color: tuple = SNAKE_COLOR
    ):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Метод определения следующего направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод определения координат 'головы' змейки"""
        return self.positions[0]

    def move(self):
        """Метод определения алгоритма движения змейки"""
        self.update_direction()
        x, y = self.get_head_position()
        # Распаковка кортежа координат головы змейки
        delta_x, delta_y = self.direction
        y = (y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        x = (x + delta_x * GRID_SIZE) % SCREEN_WIDTH
        next_position = (x, y)
        # Удаление последнего элемента из списка позиций
        # змейки, если яблоко не съедено
        self.positions.insert(0, next_position)
        self.last = (
            self.positions.pop() if (
                self.lenght < len(self.positions)
            ) else None
        )

    def reset(self):
        """Метод сброса игры"""
        self.lenght = 1
        self.positions = [self.position]
        directions = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(directions)
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод отрисовки змейки"""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция взаимодействия с клавишами управления"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(restricted_area=snake.positions)
    rock = Rock(restricted_area=[apple.position, snake.positions])
    rock_created = False
    rock.positions = [rock.position]
    while True:
        clock.tick(SPEED)
        snake.move()
        handle_keys(snake)
        if snake.lenght % 10 == 0 and rock_created is False:
            rock_position = rock.randomize_position(
                [*snake.positions, apple.position]
            )
            rock.positions.append(rock_position)
            rock.draw()
            rock_created = True
        if apple.position == snake.get_head_position():
            snake.lenght += 1
            apple.randomize_position([*snake.positions, *rock.positions])
            if snake.lenght % 10 != 0:
                rock_created = False
        elif (
            snake.get_head_position() in snake.positions[1:]
            or snake.get_head_position() in rock.positions
        ):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            rock.positions = [
                rock.randomize_position([*snake.positions, *rock.positions])
            ]
            apple.randomize_position([*snake.positions, *rock.positions])
        snake.draw()
        rock.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

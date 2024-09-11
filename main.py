import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1280, 800  # Установлено новое разрешение
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SIZE = 30  # Изменим размер, чтобы соответствовать текстуре мяча
BRICK_WIDTH, BRICK_HEIGHT = 500, 100

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Загрузка фонового изображения
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Загрузка текстуры ракетки
paddle_image = pygame.image.load("paddle_texture.png")  # Загрузите изображение для ракетки
paddle_image = pygame.transform.scale(paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))  # Масштабируем изображение под размеры ракетки

# Загрузка текстуры кирпича
brick_image = pygame.image.load("brick_texture.png")  # Загрузите изображение для кирпича
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))  # Масштабируем изображение под размеры кирпича

# Загрузка текстуры мяча
ball_image = pygame.image.load("ball_texture.png")  # Загрузите изображение для мяча
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))  # Масштабируем изображение под размеры мяча

# Классы для игровых объектов
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        # Ограничение движения на экране
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - PADDLE_WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH

    def draw(self):
        screen.blit(paddle_image, self.rect.topleft)  # Отрисовка текстуры ракетки

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 100, BALL_SIZE, BALL_SIZE)
        self.speed = [5, -5]  # Скорость по x и y

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        # Отскок от стен
        if self.rect.x <= 0 or self.rect.x >= WIDTH - BALL_SIZE:
            self.speed[0] = -self.speed[0]
        if self.rect.y <= 0:
            self.speed[1] = -self.speed[1]

    def draw(self):
        screen.blit(ball_image, self.rect.topleft)  # Отрисовка текстуры мяча

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    def draw(self):
        screen.blit(brick_image, self.rect.topleft)  # Отрисовка текстуры кирпича

# Функция для отображения текста
def display_message(message, y_offset=0, color=RED):
    font = pygame.font.Font(None, 52)  # Уменьшен размер шрифта
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

# Главная игровая функция
def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()

    # Создаем кирпичи
    bricks = []
    for x in range(0, WIDTH, BRICK_WIDTH + 5):
        for y in range(50, 200, BRICK_HEIGHT + 5):
            bricks.append(Brick(x, y))

    score = 0  # Счет игрока
    running = True
    game_active = True
    while running:
        screen.blit(background_image, (0, 0))  # Отображение фонового изображения

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-10)
            if keys[pygame.K_RIGHT]:
                paddle.move(10)

            # Движение мяча
            ball.move()

            # Проверка коллизии мяча с ракеткой
            if ball.rect.colliderect(paddle.rect):
                ball.speed[1] = -ball.speed[1]

            # Проверка коллизии мяча с кирпичами
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    ball.speed[1] = -ball.speed[1]
                    bricks.remove(brick)
                    score += 10  # Увеличиваем счет на 10 при разрушении кирпича

            # Проверка, если мяч упал ниже экрана
            if ball.rect.y >= HEIGHT:
                game_active = False

            # Проверка, остались ли кирпичи
            if not bricks:  # Если игрок выиграл
        
                game_active = False

            # Отрисовка игровых объектов
            paddle.draw()
            ball.draw()
            for brick in bricks:
                brick.draw()

            # Отображение счета
            score_display = f"Счет: {score}"
            font = pygame.font.Font(None, 36)
            text = font.render(score_display, True, WHITE)
            screen.blit(text, (10, 10))  # Отображаем счет в верхнем левом углу
        else:
            if bricks:
            # Отображение сообщения о проигрыше
                display_message("Вы проиграли!", -50, RED)
                display_message("Нажмите R, чтобы перезапустить", 50, WHITE)
            else:
                display_message("Вы выиграли!", -50, GREEN)  # Сообщение о победе зеленого цвета
                display_message("Нажмите R, чтобы перезапустить", 50, WHITE)
            # Проверка нажатия клавиши R для перезапуска игры
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                ball.reset()
                score = 0  # Сбрасываем счет
                game_active = True
                bricks.clear()
                for x in range(0, WIDTH, BRICK_WIDTH + 5):
                    for y in range(50, 200, BRICK_HEIGHT + 5):
                        bricks.append(Brick(x, y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Запускаем игру
if __name__ == "__main__":
    main()
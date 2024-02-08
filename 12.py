import requests
import json
from threading import Timer
import pygame
import sys
import time


control = 'meditation'
# Выберите показатель 'meditation', 'concentration' или 'attention'

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

from requests.exceptions import HTTPError


# Инициализация
pygame.init()

# Установка экрана
width = 468
height = 470
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Управление машинкой')

# Загрузка изображений
bg_img = pygame.image.load('Back.jpg')
car_img = pygame.image.load('Car.jpg')

# Переменные
car_x = 28
car_y = 350
car_speed = 1
bg_x = 0
distance = 0

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)  # Шрифт для отображения текста


# Значение переменной meditation
meditation = 65


def query():
    try:
        response = requests.get('http://127.0.0.1:2336/bci')
        response.raise_for_status()
        data = json.loads(response.content)
        if data['result'] is True:
            value = data[control]
            print (value)
            return value
        else:
            print('No device')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    

# Опрос 5 раз в секунду (каждые 200 мс)


time.sleep(5)

while running:

    timer = query()
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление машинкой с клавиатуры
    keys = pygame.key.get_pressed()
    if timer > 60:
        car_x += car_speed
        distance += 0.05
    if timer < 60:
        car_x +=  0.05
    
    # Проверка на выход за границы экрана
    if car_x < 0 or car_x > width:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Конец игры", True, (255, 0, 0))
        screen.blit(text, (28, 250))
        pygame.display.update()
        pygame.time.delay(2000)  # Задержка перед выходом из игры
        running = False
    # Движение фона вправо
    bg_x -= 1
    if bg_x <= -width:
        bg_x = 0

    # Отрисовка заднего фона и машинки
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(car_img, (car_x, car_y))

  # Вывод пройденного расстояния
    distance_text = font.render(f"{int(distance)} м", True, (255, 255, 255))
    screen.blit(distance_text, (width -250, 20))

    # Обновление экрана
    pygame.display.update()

    # Ограничение частоты кадров
    clock.tick(60)

# Завершение игры
pygame.quit()
sys.exit()


    

import requests
import json
from threading import Timer
import pygame
import sys


control = 'meditation'
# Выберите показатель 'meditation', 'concentration' или 'attention'

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

from requests.exceptions import HTTPError

screen = pygame.display.set_mode((800, 600))

# Значение переменной meditation
meditation = 65


def query():
    try:
        response = requests.get('http://127.0.0.1:2336/bci')
        response.raise_for_status()
        data = json.loads(response.content)
        if data['result'] is True:
            value = data[control]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Заполняем экран белым цветом
            screen.fill((255, 255, 255))

            if value > 60:
                # Рисуем круг, если meditation > 60
                pygame.draw.circle(screen, (0, 0, 255), (400, 300), 50)
            else:
                # Рисуем треугольник, если meditation <= 60
                pygame.draw.polygon(screen, (0, 255, 0), [(350, 250), (450, 250), (400, 350)])

            # Обновляем экран
            pygame.display.flip()
            # В этом месте использовать 'value' для управления игровым процессом
            print(control + ':' + str(value) + '%')
        else:
            print('No device')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    

# Опрос 5 раз в секунду (каждые 200 мс)
timer = RepeatTimer(0.2, query)

def main():    
    timer.start()
    
if __name__ == "__main__":
    main()
    
    
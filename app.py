from time import perf_counter
from copy import deepcopy
import json, os, time
try: import keyboard
except:
    os.system("pip install keyboard")

# Загрузка лабиринта из файла
with open('lab.json', 'r') as f:
    data = json.load(f)
labirint = deepcopy(data["labirint1"])
class Peni:
    def __init__(self):
        self.path = 0
        self._cords = [1, 1]
        self.status = 'playing'
        labirint[self._cords[1]][self._cords[0]] = 2  # Начальная позиция игрока

    @property
    def cords(self):
        return self._cords

    @cords.setter
    def cords(self, new_cords):
        if labirint[self._cords[1]][self._cords[0]] == 2:
            labirint[self._cords[1]][self._cords[0]] = 4  # Отметить предыдущую позицию как пройденный путь
        self._cords = new_cords
        labirint[self._cords[1]][self._cords[0]] = 2  # Отметить текущую позицию игрока

    def forward(self):
        if self._cords[1] + 1 < len(labirint[0]) and labirint[self._cords[1] + 1][self._cords[0]] in [0, 3, 4]:
            if labirint[self._cords[1] + 1][self._cords[0]] == 3: self.status = 'win'
            self.cords = [self._cords[0], self._cords[1] + 1]
            self.path += 1

    def backward(self):
        if self._cords[1] - 1 >= 0 and labirint[self._cords[1] - 1][self._cords[0]] in [0, 3, 4]:
            if labirint[self._cords[1] - 1][self._cords[0]] == 3: self.status = 'win'
            self.cords = [self._cords[0], self._cords[1] - 1]
            self.path += 1

    def right(self):
        if self._cords[0] + 1 < len(labirint) and labirint[self._cords[1]][self._cords[0] + 1] in [0, 3, 4]:
            if labirint[self._cords[1]][self._cords[0] + 1] == 3: self.status = 'win'
            self.cords = [self._cords[0] + 1, self._cords[1]]
            self.path += 1

    def left(self):
        if self._cords[0] - 1 >= 0 and labirint[self._cords[1]][self._cords[0] - 1] in [0, 3, 4]:
            if labirint[self._cords[1]][self._cords[0] - 1] == 3: self.status = 'win'
            self.cords = [self._cords[0] - 1, self._cords[1]]
            self.path += 1

    def reset(self):
        global labirint
        with open('lab.json', 'r') as f:
            data = json.load(f)
        labirint = deepcopy(data["labirint1"])
        self.path = 0
        self._cords = [1, 1]
        labirint[self._cords[1]][self._cords[0]] = 2  # Установить начальное положение игрока

def render():
    img_labirint = ''
    for i in labirint:
        t = ""
        for ii in i:
            t += str(ii)
        img_labirint += f'{t}\n'
    print(img_labirint.replace('1', '🟫').replace('0', '🟪').replace('2', '🟨').replace('3', '🟥').replace('4', '🟩'))

def check_type(cords):
    # Добавьте свою логику проверки выигрыша
    return 'win' if labirint[cords[1]][cords[0]] == 3 else 'playing'

def main():
    peni = Peni()
    start = perf_counter()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка консоли
        render()
        command = None
        print("Введите команду (w: Прямо, s: Назад, d: Направо, a: Налево, r: Перезагрузить, q: Выход): ")
        while command is None:
            if keyboard.is_pressed('w'): command = 'w'
            elif keyboard.is_pressed('s'): command = 's'
            elif keyboard.is_pressed('a'): command = 'a'
            elif keyboard.is_pressed('d'): command = 'd'
            elif keyboard.is_pressed('r'): command = 'r'
            elif keyboard.is_pressed('q'): command = 'q'
            if command:
                time.sleep(0.2)
                break
        
        if command == 's':
            peni.forward()
        elif command == 'w':
            peni.backward()
        elif command == 'd':
            peni.right()
        elif command == 'a':
            peni.left()
        elif command == 'r':
            peni.reset()
        elif command == 'q':
            break
        
        if peni.status == 'win':
            end = perf_counter()
            print(f'Ты победил{" и побил рекорд по времени" if float(data["top_time"]) > float(f"{(end - start):.3f}") else ""}{" и по пути" if data["top_path"] > peni.path else ""}!\nДлина твоего пути: {peni.path}\nВремя игры: {(end - start):.07f}\n{"Прошлый рекорд по времени: " if float(data["top_time"]) > float(f"{(end - start):.3f}") else "Текущий рекорд по времени: "}{data["top_time"]}\n{"Прошлый рекорд по пути: " if data["top_path"] > peni.path else "Текущий рекорд по пути: "}{data["top_path"]}')
            
            if float(data['top_time']) > float(f"{(end - start):.3f}"): 
                data['top_time'] = float(f"{(end - start):.3f}")
            if data['top_path'] > peni.path: 
                data['top_path'] = peni.path
            with open('lab.json', 'w') as file:
                json.dump(data, file, indent=4)
            break

if __name__ == "__main__":
    main()

import json
import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

SAVE_FILE = "save.json"

# Функция сохранения игры
def save_game(player_name, current_scene, bonuses):
    data = {
        "player_name": player_name,
        "current_scene": current_scene,
        "bonuses": bonuses  # сохраняем бонусы
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)
    print(Fore.GREEN + "Игра сохранена!")

# Функция загрузки игры
def load_game():
    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
            print(Fore.YELLOW + "Игра загружена!")
            return data["player_name"], data["current_scene"], data["bonuses"]
    except FileNotFoundError:
        return None, None, 0  # Если сохранения нет, бонусы = 0

# Функция удаления сохранения
def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print(Fore.RED + "Сохранение удалено. Начинаем новую игру!")

# Базовый класс Сцены
class Scene:
    def __init__(self):
        self.next_scene = None

# Начальная сцена
class SceneStart(Scene):
    def enter(self):
        print(Fore.CYAN + "\nВы находитесь на развилке в лесу. Куда вы хотите пойти?")
        print("1. В лес")
        print("2. В пещеру")
        print("3. В деревню")
        choice = input("Выберите действие (1-3): ")

        if choice == "1":
            self.next_scene = "forest"
        elif choice == "2":
            self.next_scene = "cave"
        elif choice == "3":
            self.next_scene = "village"
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.next_scene = "start"

# Лесная сцена
class SceneForest(Scene):
    def enter(self):
        print(Fore.GREEN + "\nВы вошли в лес. Здесь много деревьев и звуков природы.")
        print("1. Исследовать тропинку")
        print("2. Вернуться на развилку")
        choice = input("Выберите действие (1-2): ")

        if choice == "1":
            print("Вы нашли сокровище! Ваш бонус увеличен.")
            game.bonuses += 10  # Используем game.bonuses для увеличения бонуса
            self.next_scene = "start"
        elif choice == "2":
            self.next_scene = "start"
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.next_scene = "forest"

# Пещерная сцена
class SceneCave(Scene):
    def enter(self):
        print(Fore.RED + "\nВы вошли в пещеру. Темно и страшно.")
        print("1. Идти к свету")
        print("2. Вернуться на развилку")
        choice = input("Выберите действие (1-2): ")

        if choice == "1":
            print("Вы встретили дракона! Он вас съел...")
            self.next_scene = "end"
        elif choice == "2":
            self.next_scene = "start"
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.next_scene = "cave"

# Деревня
class SceneVillage(Scene):
    def enter(self):
        print(Fore.YELLOW + "\nВы пришли в деревню. Здесь много людей.")
        print("1. Поговорить с местными жителями")
        print("2. Вернуться на развилку")
        choice = input("Выберите действие (1-2): ")

        if choice == "1":
            print("Местные жители рассказали вам о страшной пещере.")
            self.next_scene = "start"
        elif choice == "2":
            self.next_scene = "start"
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.next_scene = "village"

# Конец игры
class SceneEnd(Scene):
    def enter(self):
        print(Fore.MAGENTA + "\nИгра окончена.")
        print("Спасибо за игру!")
        print("1. Сохранить игру")
        print("2. Выйти из игры")
        choice = input("Выберите действие (1-2): ")

        if choice == "1":
            save_game(game.player_name, game.current_scene, game.bonuses)
            sys.exit(0)
        elif choice == "2":
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.next_scene = "end"


# Главный класс игры
class Game:
    scenes = {
        "start": SceneStart(),
        "forest": SceneForest(),
        "cave": SceneCave(),
        "village": SceneVillage(),
        "end": SceneEnd(),
    }

    def __init__(self):
        self.player_name = None
        self.current_scene = "start"
        self.bonuses = 0

    def start_game(self):
        # Проверка на наличие сохранения
        if os.path.exists(SAVE_FILE):
            print(Fore.YELLOW + "Обнаружено сохранение игры!")
            print("1. Загрузить сохранение")
            print("2. Начать новую игру")
            choice = input("Выберите действие (1-2): ")

            if choice == "1":
                self.player_name, self.current_scene, self.bonuses = load_game()
                print(Fore.CYAN + f"Добро пожаловать обратно, {self.player_name}!")
            elif choice == "2":
                delete_save()
                self.start_new_game()
            else:
                print("Неверный ввод. Начинаем новую игру.")
                self.start_new_game()
        else:
            self.start_new_game()

        self.play()

    def start_new_game(self):
        self.player_name = input("Введите ваше имя: ")
        print(Fore.CYAN + f"Добро пожаловать, {self.player_name}! Приключение начинается!")
        self.current_scene = "start"
        self.bonuses = 0

    def play(self):
        while True:
            scene = self.scenes[self.current_scene]
            scene.enter()
            self.current_scene = scene.next_scene

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start_game()
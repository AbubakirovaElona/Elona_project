import json
import sys
from colorama import Fore, Style, init

init(autoreset=True)

# Функция сохранения игры
def save_game(player_name, current_scene, score):
    data = {"player_name": player_name, "current_scene": current_scene, "score": score}
    with open("save.json", "w") as file:
        json.dump(data, file)
    print(Fore.GREEN + "Игра сохранена!")

# Функция загрузки игры
def load_game():
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
            print(Fore.YELLOW + "Игра загружена!")
            return data["player_name"], data["current_scene"], data["score"]
    except FileNotFoundError:
        print(Fore.RED + "Файл сохранения не найден. Начните новую игру.")
        return None, None, 0

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
        print("4. Сохранить игру")
        print("5. Выйти из игры")
        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            self.next_scene = "forest"
        elif choice == "2":
            self.next_scene = "cave"
        elif choice == "3":
            self.next_scene = "village"
        elif choice == "4":
            save_game(game.player_name, game.current_scene, game.score)
            self.next_scene = "start"
        elif choice == "5":
            print(Fore.MAGENTA + "Спасибо за игру!")
            sys.exit(0)  # Завершение игры
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
            print("Вы нашли сокровище! Вы получаете 10 очков.")
            game.score += 10  # Добавляем очки к общему счету
            print(Fore.YELLOW + f"Ваш текущий счет: {game.score}")
            self.next_scene = "end"
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
        print(Fore.YELLOW + f"Ваш финальный счет: {game.score}")
        self.show_end_menu()

    def show_end_menu(self):
        print("\n1. Сохранить игру")
        print("2. Начать новую игру")
        print("3. Выйти из игры")
        choice = input("Выберите действие (1-3): ")


        if choice == "1":
            save_game(game.player_name, game.current_scene, game.score)
            self.next_scene = "start"
        elif choice == "2":
            game.start_new_game()
            game.play()
        elif choice == "3":
            print(Fore.MAGENTA + "Спасибо за игру!")
            sys.exit(0)  # Завершение игры
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.show_end_menu()

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
        self.score = 0

    def start_game(self):
        print(Fore.CYAN + "Добро пожаловать в игру!")
        print("1. Начать новую игру")
        print("2. Загрузить игру")
        choice = input("Выберите действие (1-2): ")

        if choice == "2":
            player_name, scene, score = load_game()
            if player_name and scene:  # Если удалось загрузить игру
                self.player_name = player_name
                self.current_scene = scene
                self.score = score
                print(Fore.CYAN + f"Добро пожаловать обратно, {self.player_name}!")
                print(Fore.YELLOW + f"Ваш текущий счет: {self.score}")
                self.play()  # Продолжить игру
            else:
                print("Не удалось загрузить игру. Начинаем новую.")
                self.start_new_game()
                self.play()
        else:
            self.start_new_game()
            self.play()

    def start_new_game(self):
        self.player_name = input("Введите ваше имя: ")
        self.current_scene = "start"
        self.score = 0
        print(Fore.CYAN + f"Добро пожаловать, {self.player_name}! Приключение начинается!")

    def play(self):
        while True:
            scene = self.scenes[self.current_scene]
            scene.enter()
            self.current_scene = scene.next_scene

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start_game()
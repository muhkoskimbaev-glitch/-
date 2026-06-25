import random
import time

users = {}
current_user = None

#АВТОРИЗАЦИЯ
def register():
    global users
    username = input("Введите имя пользователя: ")

    if username in users:
        print(" Пользователь уже существует")
        return

    password = input("Введите пароль (минимум 5 символов, латиница и цифры): ")

    if len(password) < 5 or not password.isalnum():
        print(" Неверный пароль")
        return
#СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
    users[username] = {
        "password": password,
        "cards": [],
        "notes": []
    }
    print(" Регистрация успешна")


def login():
    global current_user

    username = input("Логин: ")
    password = input("Пароль: ")

    if username in users and users[username]["password"] == password:
        current_user = username
        print(" Вход выполнен")
    else:
        print(" Неверные данные")


#КАРТОЧКИ
def add_card():
    q = input("Введите вопрос: ")
    a = input("Введите ответ: ")
    users[current_user]["cards"].append({"q": q, "a": a})
    print("✅ Карточка добавлена")


def random_card():
    cards = users[current_user]["cards"]
    if not cards:
        print(" Нет карточек")
        return

    card = random.choice(cards)
    print("Вопрос:", card["q"])
    input("Нажми Enter чтобы увидеть ответ...")
    print("Ответ:", card["a"])


#ВИКТОРИНА
def quiz():
    cards = users[current_user]["cards"]

    if not cards:
        print(" Нет карточек")
        return

    score = 0
    random.shuffle(cards)

    for card in cards:
        print("\nВопрос:", card["q"])

        start = time.time()
        answer = input("Ответ (30 сек): ")
        end = time.time()

        if end - start > 30:
            print("⏰ Время вышло")
            continue

        if answer.strip().lower() == card["a"].strip().lower():
            print("✅ Верно")
            score += 1
        else:
            print(" Неверно. Правильный ответ:", card["a"])

    print(f"\n Результат: {score} из {len(cards)}")


#ЗАМЕТКИ
def add_note():
    note = input("Введите заметку: ")
    users[current_user]["notes"].append(note)
    print("✅ Добавлено")


def view_notes():
    notes = users[current_user]["notes"]
    if not notes:
        print(" Нет заметок")
        return

    for i, n in enumerate(notes):
        print(f"{i + 1}. {n}")


def delete_note():
    view_notes()
    notes = users[current_user]["notes"]

    if not notes:
        return

    try:
        index = int(input("Номер для удаления: ")) - 1
        notes.pop(index)
        print("✅ Удалено")
    except:
        print(" Ошибка")


#МЕНЮ
def user_menu():
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Добавить карточку")
        print("2. Случайная карточка")
        print("3. Викторина")
        print("4. Добавить заметку")
        print("5. Показать заметки")
        print("6. Удалить заметку")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            add_card()
        elif choice == "2":
            random_card()
        elif choice == "3":
            quiz()
        elif choice == "4":
            add_note()
        elif choice == "5":
            view_notes()
        elif choice == "6":
            delete_note()
        elif choice == "0":
            break


def main():
    while True:
        print("--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Регистрация")
        print("2. Вход")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
            if current_user:
                user_menu()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()

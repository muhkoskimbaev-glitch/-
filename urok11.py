import random
# Функция выбора компьютера
def get_computer_choice():
    варианты = ["камень", "ножницы", "бумага"]
    return random.choice(варианты)
# Функция  определение победителя
def determine_winner(player, computer):
    if player == computer:
        return "ничья"
    elif (player == "камень" and computer == "ножницы") or \
         (player == "ножницы" and computer == "бумага") or \
         (player == "бумага" and computer == "камень"):
        return "игрок"
    else:
        return "компьютер"
# Основная функция
def main():
    player_score = 0
    computer_score = 0

    print("Добро пожаловать в игру Камень-Ножницы-Бумага!")
    print("Правила: камень бьет ножницы, ножницы бьют бумагу, бумага бьет камень.")
    print("Игра до 3 побед.")

    while True:
        player = input("Введите (камень/ножницы/бумага): ").lower()
        if player == 'выход':
            print('Игра завершена')
            break
        if player not in ["камень", "ножницы", "бумага"]:
            print("Неверный ввод, попробуй еще раз!")
            continue

        computer = get_computer_choice()
        print("Компьютер выбрал:", computer)

        result = determine_winner(player, computer)

        if result == "ничья":
            print("Ничья!")
        elif result == "игрок":
            print("Ты выиграл раунд!")
            player_score += 1
        else:
            print("Компьютер выиграл раунд!")
            computer_score += 1

        print(f"Счет: Игрок {player_score} - {computer_score} Компьютер")
# Финал
    print("Игра окончена!")
    if player_score == 3:
        print("Поздравляю! Ты победил ")
    else:
        print("Победил компьютер ")

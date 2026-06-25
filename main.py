import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8612704459:AAHxiECiygtakfxbMkio687Dga_dUgEteV4'
API_KEY = 'bd40360e4e8ba0c4a75b6445'

bot = telebot.TeleBot(BOT_TOKEN)

POPULAR_CURRENCIES = ['USD', 'EUR', 'RUB', 'KZT', 'GBP', 'CNY', 'TRY', 'AED']

user_states = {}
# Структура: { user_id: { 'step': 'base'|'target'|'amount', 'base': str, 'target': str } }


def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get('result') == 'success':
            rates = data['conversion_rates']
            if target_currency in rates:
                return rates[target_currency]
    except requests.RequestException:
        return None
    return None


def currency_keyboard():

    markup = InlineKeyboardMarkup(row_width=4)
    buttons = [InlineKeyboardButton(c, callback_data=f"currency_{c}") for c in POPULAR_CURRENCIES]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот для конвертации валют.\n\n"
        "Используй /convert — чтобы начать конвертацию.\n"
        "Используй /help — чтобы узнать, как работать со мной."
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📖 *Как пользоваться ботом:*\n\n"
        "1️⃣ Отправь /convert\n"
        "2️⃣ Выбери *исходную* валюту из кнопок\n"
        "3️⃣ Выбери *целевую* валюту\n"
        "4️⃣ Введи сумму для конвертации\n\n"
        "💡 *Быстрая конвертация одной строкой:*\n"
        "`/calc <сумма> <из> <в>`\n"
        "Пример: `/calc 100 USD KZT`\n\n"
        "📌 *Доступные команды:*\n"
        "/start — начало работы\n"
        "/convert — пошаговая конвертация\n"
        "/calc — быстрая конвертация\n"
        "/help — эта справка",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['convert'])
def convert_start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'step': 'base'}
    bot.send_message(
        message.chat.id,
        "🔄 *Шаг 1/3:* Выбери *исходную* валюту:",
        reply_markup=currency_keyboard(),
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('currency_'))
def handle_currency_choice(call):
    user_id = call.from_user.id
    chosen = call.data.replace('currency_', '')
    state = user_states.get(user_id)

    if not state:
        bot.answer_callback_query(call.id, "Сначала отправь /convert")
        return

    if state['step'] == 'base':
        user_states[user_id]['base'] = chosen
        user_states[user_id]['step'] = 'target'
        bot.edit_message_text(
            f"✅ Исходная валюта: *{chosen}*\n\n🔄 *Шаг 2/3:* Выбери *целевую* валюту:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=currency_keyboard(),
            parse_mode='Markdown'
        )

    elif state['step'] == 'target':
        base = state['base']
        if chosen == base:
            bot.answer_callback_query(call.id, "⚠️ Целевая валюта не должна совпадать с исходной!")
            return
        user_states[user_id]['target'] = chosen
        user_states[user_id]['step'] = 'amount'
        bot.edit_message_text(
            f"✅ Исходная: *{base}* → Целевая: *{chosen}*\n\n💰 *Шаг 3/3:* Введи сумму:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode='Markdown'
        )

    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id, {}).get('step') == 'amount')
def handle_amount(message):
    user_id = message.from_user.id
    state = user_states[user_id]

    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Введи корректное положительное число.")
        return

    base = state['base']
    target = state['target']
    rate = get_exchange_rate(base, target)

    if rate is None:
        bot.send_message(message.chat.id, " Не удалось получить курс валют. Попробуй позже.")
    else:
        result = amount * rate
        bot.send_message(
            message.chat.id,
            f"💱 *Результат конвертации:*\n\n"
            f"`{amount:,.2f} {base}` = `{result:,.2f} {target}`\n\n"
            f"📈 Курс: 1 {base} = {rate:.4f} {target}\n\n"
            f"Хочешь ещё? Отправь /convert",
            parse_mode='Markdown'
        )

    del user_states[user_id]

@bot.message_handler(commands=['calc'])
def quick_convert(message):
    parts = message.text.split()
    if len(parts) != 4:
        bot.send_message(
            message.chat.id,
            "⚠️ Неверный формат. Используй:\n`/calc <сумма> <из> <в>`\nПример: `/calc 100 USD KZT`",
            parse_mode='Markdown'
        )
        return

    _, raw_amount, base_currency, target_currency = parts
    base_currency = base_currency.upper()
    target_currency = target_currency.upper()

    try:
        amount = float(raw_amount.replace(',', '.'))
        if amount <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Введи корректное положительное число для суммы.")
        return

    rate = get_exchange_rate(base_currency, target_currency)

    if rate is None:
        bot.send_message(
            message.chat.id,
            f"❌ Не удалось получить курс для пары {base_currency}/{target_currency}.\n"
            "Проверь правильность кодов валют (например: USD, EUR, KZT)."
        )
    else:
        result = amount * rate
        bot.send_message(
            message.chat.id,
            f"💱 *Результат:*\n\n"
            f"`{amount:,.2f} {base_currency}` = `{result:,.2f} {target_currency}`\n\n"
            f"📈 Курс: 1 {base_currency} = {rate:.4f} {target_currency}",
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "🤷 Не понимаю эту команду. Отправь /help для справки."
    )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
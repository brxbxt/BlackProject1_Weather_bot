from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging
import asyncio
import requests
from API_KEY import API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Вставь сюда токен
API_TOKEN = API_KEY

# URL веб-сервиса Flask
WEATHER_API_URL = "http://127.0.0.1:5000/"

# Создаём бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Состояния
STATE_SELECTING_ROUTE = 'SELECTING_ROUTE'
STATE_SELECTING_DAYS = 'SELECTING_DAYS'
STATE_CONFIRMING = 'CONFIRMING'

# Словарь для хранения состояния пользователей
user_states = {}

# Обработчик команды /start
@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    user_states[message.from_user.id] = {'state': STATE_SELECTING_ROUTE, 'route': {}, 'days': None}
    await message.answer(
        "Привет! Я помогу вам узнать прогноз погоды для маршрута. Введите начальный город или выберите команду /help для справки."
    )

# Обработчик команды /help
@dp.message(F.text == '/help')
async def help_command(message: types.Message):
    await message.answer(
        "Список доступных команд:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справку\n"
        "/weather - Запросить прогноз погоды для маршрута"
    )

# Обработчик команды /weather
@dp.message(F.text == '/weather')
async def weather_command(message: types.Message):
    user_states[message.from_user.id] = {'state': STATE_SELECTING_ROUTE, 'route': {}, 'days': None}
    await message.answer('Введите начальный город (например, "Москва"):')

# Обработка ввода маршрута
@dp.message()
async def handle_route_input(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id]['state'] != STATE_SELECTING_ROUTE:
        await message.answer('Пожалуйста, начните с команды /weather.')
        return

    route = user_states[user_id].setdefault('route', {})

    if 'start_location' not in route:
        route['start_location'] = message.text.strip()
        await message.answer('Введите конечный город (например, "Нью-Йорк"):')
    elif 'end_location' not in route:
        route['end_location'] = message.text.strip()
        await message.answer('Введите промежуточные города через запятую (например, "Рязань, Казань"):')
    elif 'stops' not in route:
        stops = message.text.split(',') if message.text.strip() else []
        route['stops'] = [stop.strip() for stop in stops]
        user_states[user_id]['state'] = STATE_SELECTING_DAYS
        await message.answer('Выберите количество дней для прогноза:', reply_markup=get_days_keyboard())

# Функция для создания клавиатуры с выбором дней
def get_days_keyboard():
    inline_buttons = [
        [InlineKeyboardButton(text=f'{i} дней', callback_data=f'days:{i}')]
        for i in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

# Обработка выбора количества дней
@dp.callback_query(F.data.startswith('days:'))
async def handle_days_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_states or user_states[user_id]['state'] != STATE_SELECTING_DAYS:
        await callback_query.answer('Ошибка: выберите маршрут сначала.', show_alert=True)
        return

    days = int(callback_query.data.split(':')[1])
    user_states[user_id]['days'] = days
    user_states[user_id]['state'] = STATE_CONFIRMING

    # Подтверждение маршрута
    route = user_states[user_id]['route']
    await callback_query.message.answer(
        f'Ваш маршрут: {route["start_location"]} -> {" -> ".join(route["stops"])} -> {route["end_location"]}\n'
        f'Прогноз на {days} дней. Подтвердите запрос.',
        reply_markup=get_confirm_keyboard()
    )

# Функция для создания инлайн-клавиатуры с подтверждением
def get_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data='confirm'),
            InlineKeyboardButton(text='Изменить', callback_data='change')
        ]
    ])
    return keyboard

# Обработка подтверждения маршрута
@dp.callback_query(F.data == 'confirm')
async def handle_confirmation(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_states or user_states[user_id]['state'] != STATE_CONFIRMING:
        await callback_query.answer('Ошибка: выберите маршрут сначала.', show_alert=True)
        return

    # Отправка запроса к веб-сервису
    route = user_states[user_id]['route']
    payload = {
        "start_location": route['start_location'],
        "stops": route['stops'],
        "end_location": route['end_location'],
        "days": user_states[user_id]['days']
    }

    try:
        response = requests.post(WEATHER_API_URL, json=payload)
        response.raise_for_status()
        weather_data = response.json()

        # Вывод результата
        await callback_query.message.answer(format_weather_data(weather_data))
    except requests.RequestException as e:
        await callback_query.message.answer(f'Ошибка подключения: {e}')

# Функция для форматирования данных о погоде
def format_weather_data(data):
    result = []
    for point in data:
        result.append(
            f"Город: {point['location']}\n\n"
            f"1. Температура на следующие дни: \n{', '.join([f'{temp} °C' for temp in point['Temperatures']])} \n"
            f"2. Влажность на следующие дни: \n{', '.join([f'{humid} %' for humid in point['Humidities']])} \n"
            f"3. Ветер на следующие дни: \n{', '.join([f'{wind} км/ч' for wind in point['Wind_speeds']])} \n"
            f"4. Осадки на следующие дни: \n{', '.join([f'{precip} %' for precip in point['Precip_probs']])} \n"
        )
    return "\n\n".join(result)

# Обработка кнопки «Изменить»
@dp.callback_query(F.data == 'change')
async def handle_change(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_states[user_id] = {'state': STATE_SELECTING_ROUTE, 'route': {}, 'days': None}
    await callback_query.message.answer('Давайте начнём заново. Введите начальный город:')

# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')

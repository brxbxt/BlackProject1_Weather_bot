from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio
from API_KEY import API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# В этой переменной будет храниться токен.
# Сделай так, чтобы в переменной API_TOKEN была строка
# с твоим токеном. Помни, что токен - это чувствительная
# информация, и в коде его хранить нельзя.
# Используй чтение из внешнего файла или получи его
# через переменную окружения с помощью os.getenv
API_TOKEN = API_KEY

print(API_TOKEN)

# Создаём бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

### --- ОБРАБОТЧИК КОМАНД ---
@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    # Создаём кнопки
    button_about = KeyboardButton(text='О боте')
    button_inline = KeyboardButton(text='Инлайн-кнопки')

    # Создаём клавиатуру и добавляем кнопки
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_about], [button_inline]],
        resize_keyboard=True
    )

    await message.answer(
        'Привет! Я демонстрационный бот. Выберите действие с помощью кнопок ниже или отправьте команду /help.',
        reply_markup=reply_keyboard,
    )

@dp.message(F.text == '/help')
async def help_command(message: types.Message):
    await message.answer(
        'Список доступных команд:\n'
        '/start - Начать работу с ботом\n'
        '/help - Получить помощь\n'
        'Также вы можете воспользоваться кнопками ниже.'
    )

### --- ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ---
@dp.message(F.text == 'О боте')
async def about_bot(message: types.Message):
    await message.answer('Этот бот создан для демонстрации возможностей библиотеки Aiogram!')

### --- ИНЛАЙН-КНОПКИ ---
@dp.message(F.text == 'Инлайн-кнопки')
async def send_inline_keyboard(message: types.Message):
    # Создаём инлайн-кнопки
    button_link = InlineKeyboardButton(text='Ссылка', url='https://example.com')
    button_callback = InlineKeyboardButton(text='Голосовать', callback_data='vote')

    # Создаём инлайн-клавиатуру
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_link], [button_callback]]
    )

    await message.answer('Выберите действие:', reply_markup=inline_keyboard)

### --- CALLBACK-ЗАПРОСЫ ---
@dp.callback_query(F.data == 'vote')
async def vote_callback(callback: types.CallbackQuery):
    await callback.message.answer('Спасибо за ваш голос!')
    await callback.answer()

### --- НЕОБРАБОТАННЫЕ СООБЩЕНИЯ ---
@dp.message()
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды или кнопки.')

### --- ЗАПУСК БОТА ---
if __name__ == '__main__':
    async def main():
        # Запускаем polling
        await dp.start_polling(bot)

    asyncio.run(main())
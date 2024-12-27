# BlackProject1_Weather_bot

Telegram Weather Bot — это бот для запроса прогноза погоды на маршруте с начальной, промежуточными и конечной точками. Он взаимодействует с веб-сервисом Flask для получения прогноза погоды, а также предоставляет пользователю удобный интерфейс для взаимодействия через команды и кнопки.

## Основные возможности
- **Команда /start** — приветствие пользователя и краткое описание возможностей бота.
- **Команда /help** — отображает список доступных команд и инструкцию по использованию.
- **Команда /weather** — позволяет пользователю запросить прогноз погоды. Бот запрашивает:
  - начальную точку маршрута,
  - конечную точку маршрута,
  - промежуточные точки (опционально),
  - временной интервал прогноза (выбирается через кнопки).
- Поддержка инлайн-клавиатур для выбора временного интервала прогноза и подтверждения маршрута.
- Информативный вывод прогноза погоды для каждой точки маршрута:
  - Температура,
  - Влажность,
  - Скорость ветра,
  - Осадки.

## Установка и настройка

1. **Клонируйте репозиторий или загрузите файлы.**

2. **Создайте виртуальное окружение Python:**

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
     ```
     API_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
     ```

5. **Запустите сервер Flask:**
   - Перейдите в папку с веб-сервисом и выполните:
     ```bash
     python weather_app.py
     ```

6. **Запустите бота:**
   ```bash
   python bot.py
   ```

## Использование

### Команды бота

- **/start**
  Приветствие пользователя. Начало работы с ботом.

- **/help**
  Выводит список доступных команд и краткое описание.

- **/weather**
  Запрашивает у пользователя маршрут:
  1. Введите начальную точку маршрута.
  2. Введите конечную точку маршрута.
  3. (Опционально) Введите промежуточные точки через запятую.
  4. Выберите количество дней для прогноза (от 1 до 5).

  После подтверждения маршрута бот отправляет запрос к серверу Flask и выводит прогноз в формате:
  ```
  Город: Москва
  
  1. Температура на следующие дни
  2. Влажность на следующие дни
  3. Ветер на следующие дни
  4. Осадки на следующие дни
  ```

### Пример использования
1. Запустите команду `/start` для приветствия.
2. Используйте команду `/weather` для запроса прогноза.
3. Следуйте инструкциям бота:
   - Введите начальный, конечный и промежуточные города.
   - Выберите количество дней для прогноза.
4. Получите структурированный прогноз погоды для маршрута.

## Файлы проекта

### `bot.py`
Код Telegram-бота, обрабатывающего команды и взаимодействующего с пользователем. Отправляет запросы к серверу Flask.

### `weather_app.py`
Код веб-сервиса Flask для обработки маршрута и предоставления прогноза погоды. Использует локальные данные для симуляции прогноза.

### `locations.json`
Файл с координатами городов для сервиса Flask.
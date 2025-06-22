# TechSupportBot

TechSupportBot — это серверлес Telegram-бот для сбора баг-репортов, идей и связи с командой поддержки. Разработан на TypeScript, Telegraf и деплоится на Vercel.

## Возможности
- Приветственное сообщение с картинкой и кнопками
- Кнопки: баг-репорт, предложение идеи, заказать разработку, связаться с командой
- Сбор информации от пользователя и отправка в чат поддержки
- Кнопки для изменения статуса запроса и ответа пользователю

## Переменные окружения
Создайте файл `.env` в корне проекта:
```
ADMIN_USERNAME=your_admin_username
SUPPORT_CHAT_USERNAME=your_support_chat_username
BOT_TOKEN=your_telegram_bot_token
```

## Быстрый старт локально
1. Установите зависимости:
   ```bash
   npm install
   ```
2. Запустите TypeScript компиляцию в watch-режиме:
   ```bash
   npx tsc --watch
   ```
3. Для тестирования используйте ngrok или локальный сервер для Telegram webhook.

## Деплой на Vercel
1. Зарегистрируйтесь на [Vercel](https://vercel.com/).
2. Залейте проект на GitHub.
3. Импортируйте репозиторий на Vercel.
4. В настройках проекта добавьте переменные окружения из `.env`.
5. Укажите root-эндпоинт для webhook Telegram:
   - В настройках Telegram-бота выполните:
     ```bash
     curl -F "url=https://<your-vercel-domain>/api/bot" https://api.telegram.org/bot<your_telegram_bot_token>/setWebhook
     ```
6. После деплоя бот будет принимать сообщения через Vercel serverless function.

## Структура проекта
- `src/bot.ts` — основной код бота
- `api/bot.ts` — serverless endpoint для Vercel
- `public/` — публичные файлы (например, картинки)

## Лицензия
MIT 

## Интеграция с Google Sheets для хранения тикетов

1. **Создайте Google Cloud Project**
   - Перейдите на https://console.cloud.google.com/ и создайте новый проект.

2. **Включите Google Sheets API**
   - В меню "APIs & Services" выберите "Enable APIs and Services".
   - Найдите "Google Sheets API" и включите его.

3. **Создайте сервисный аккаунт**
   - В меню "APIs & Services" выберите "Credentials".
   - Нажмите "Create Credentials" → "Service account".
   - Дайте имя, создайте аккаунт, роли можно не назначать.
   - После создания выберите аккаунт, вкладка "Keys" → "Add Key" → "Create new key" → JSON.
   - Скачайте файл, переименуйте его в `google-credentials.json` и поместите в корень проекта (или настройте путь в .env).

4. **Создайте Google-таблицу**
   - Перейдите на https://sheets.google.com/ и создайте новую таблицу.
   - Скопируйте её ID из URL (например, https://docs.google.com/spreadsheets/d/ID_ТАБЛИЦЫ/edit).

5. **Дайте сервисному аккаунту доступ к таблице**
   - Откройте таблицу, нажмите "Поделиться".
   - Вставьте email сервисного аккаунта (из JSON-файла) и дайте права "Редактор".

6. **Добавьте переменные в .env**
   ```
   GOOGLE_SHEET_ID=ID_ТАБЛИЦЫ
   GOOGLE_CREDENTIALS_PATH=google-credentials.json
   ```

7. **Структура таблицы**
   - Первая строка: `id`, `user_id`, `username`, `date`, `category`, `status`, `message`, `attachments`, `rating`
   - Новые тикеты будут добавляться в новые строки.

8. **Установите зависимости**
   ```bash
   npm install googleapis
   ```

9. **Готово!**
   - Теперь тикеты будут сохраняться в Google Sheets. 

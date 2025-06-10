![](header.png)

# `🌿 TECH SUPPORT BOT`

Telegram бот для технической поддержки и отслеживания ошибок.

## Возможности

### Возможности для пользователей
- Отправка отчетов об ошибках
- Отправка предложений по улучшению
- Отслеживание статуса тикетов
- Просмотр справочной информации
- Просмотр информации о разработчиках
- Просмотр информации о продуктах

### Возможности для администраторов
- Просмотр всех тикетов
- Обновление статуса тикетов
- Отправка сообщений пользователям
- Получение статуса тикета
- Управление отчетами об ошибках и предложениями

## Команды

### Команды пользователей
- `/start` - Запуск бота и отображение главного меню
- `/help` - Показать справочную информацию
- `/devs` - Показать информацию о разработчиках
- `/products` - Показать информацию о продуктах

### Команды администраторов
- `/help` - Показать справочную информацию для администраторов
- `/get_all_tickets` - Получить список всех тикетов
- `/get_ticket_status | <id_тикета> | <категория>` - Получить статус конкретного тикета
- `/set_ticket_status | <id_тикета> | <категория> | <новый_статус>` - Обновить статус тикета
- `/admin_answer | <id_клиента> | <сообщение>` - Отправить сообщение пользователю

## Установка

### Требования
- Python 3.13+
- PostgreSQL 15+
- Docker и Docker Compose

### Переменные окружения
Создайте файл `.env` со следующими переменными:
```env
BOT_TOKEN=ваш_токен_бота_telegram
CHANNEL=id_вашего_канала_telegram
DEVS=id_чата_разработчиков_telegram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tech_support
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

### Установка через Docker
1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/TechSupportBot.git
cd TechSupportBot
```

2. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

### Ручная установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/TechSupportBot.git
cd TechSupportBot
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # В Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите бота:
```bash
python src/main.py
```

## Структура проекта
```
TechSupportBot/
├── src/
│   ├── admin.py           # Обработчики команд администратора
│   ├── config.py          # Настройки конфигурации
│   ├── db/                # Файлы базы данных
│   │   ├── crud.py        # Операции с базой данных
│   │   ├── database.py    # Подключение к базе данных
│   │   └── models.py      # Модели базы данных
│   ├── handlers/          # Обработчики команд пользователя
│   ├── kb_builder.py      # Построитель клавиатуры
│   ├── main.py           # Основной файл приложения
│   └── resources/        # Статические ресурсы
├── docker-compose.yml    # Конфигурация Docker
├── Dockerfile           # Файл сборки Docker
└── requirements.txt     # Зависимости Python
```

## Участие в разработке
1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте ваши изменения (`git commit -m 'Добавлена новая функция'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Лицензия
Этот проект распространяется под лицензией MIT - подробности в файле LICENSE. 

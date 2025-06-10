![](header.png)

# `🌿 TECH SUPPORT BOT`

A Telegram bot for technical support and bug tracking system.

## Features

### User Features
- Submit bug reports
- Submit feature suggestions
- Track ticket status
- View help information
- View developer information
- View product information

### Admin Features
- View all tickets
- Update ticket status
- Send messages to users
- Get ticket status
- Manage bug reports and suggestions

## Commands

### User Commands
- `/start` - Start the bot and show main menu
- `/help` - Show help information
- `/devs` - Show developer information
- `/products` - Show product information

### Admin Commands
- `/help` - Show admin help information
- `/get_all_tickets` - Get a list of all tickets
- `/get_ticket_status | <ticket_id> | <category>` - Get status of a specific ticket
- `/set_ticket_status | <ticket_id> | <category> | <new_status>` - Update ticket status
- `/admin_answer | <client_id> | <message>` - Send a message to a user

## Installation

### Prerequisites
- Python 3.13+
- PostgreSQL 15+
- Docker and Docker Compose

### Environment Variables
Create a `.env` file with the following variables:
```env
BOT_TOKEN=your_telegram_bot_token
CHANNEL=your_telegram_channel_id
DEVS=your_telegram_dev_chat_id
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tech_support
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

### Docker Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/TechSupportBot.git
cd TechSupportBot
```

2. Build and start the containers:
```bash
docker-compose up --build
```

### Manual Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/TechSupportBot.git
cd TechSupportBot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the bot:
```bash
python src/main.py
```

## Project Structure
```
TechSupportBot/
├── src/
│   ├── admin.py           # Admin command handlers
│   ├── config.py          # Configuration settings
│   ├── db/                # Database related files
│   │   ├── crud.py        # Database operations
│   │   ├── database.py    # Database connection
│   │   └── models.py      # Database models
│   ├── handlers/          # User command handlers
│   ├── kb_builder.py      # Keyboard builder
│   ├── main.py           # Main application file
│   └── resources/        # Static resources
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Docker build file
└── requirements.txt     # Python dependencies
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

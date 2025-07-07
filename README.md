# TechSupportBot

**TechSupportBot** is a Telegram bot for user support, bug reporting, idea collection, and development order requests. The bot supports multiple languages and can work both in polling mode (locally) and via webhook (e.g., on Vercel).

## Features

- Accepts user requests (bug reports, feature suggestions, development orders)
- Supports attachments: text, photos, videos, documents
- Multilingual interface (Russian, English, Japanese, Spanish)
- Notifies a dedicated support chat about new tickets
- Ticket status system (new, in progress, completed, review)
- Users can change the interface language

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Nighty3098/TechSupportBot.git
cd TechSupportBot
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

Create a `.env` file in the project root and specify:

```
BOT_TOKEN=your_bot_token
SUPPORT_CHAT_USERNAME=support_chat_or_user
NOTIFY_CHAT=chat_id_for_tickets
```

- `BOT_TOKEN` — your Telegram bot token
- `SUPPORT_CHAT_USERNAME` — username of the support chat/user for development orders
- `NOTIFY_CHAT` — chat ID (e.g., `-1001234567890`) where tickets will be sent

### 4. Run the bot locally

```bash
npm run dev
```

The bot will start in polling mode (for development).

### 5. Deploy to Vercel

- Use the function from `api/bot.ts` as the webhook endpoint.
- Set environment variables in your Vercel project settings.
- In Telegram, set the webhook to your Vercel endpoint URL.

## Project Structure

- `src/bot.ts` — main bot logic
- `src/locales/` — language files
- `api/bot.ts` — webhook endpoint (for Vercel)
- `src/local.ts` — polling mode launcher for local development

## Main Commands and Scenarios

- `/start` — greeting and main menu
- Menu buttons:
  - Bug report
  - Suggest an idea
  - Order development
  - Change language

The user selects a category, sends a message (and optionally attachments). The ticket is sent to the support chat with a status change button. When the status is changed, the user receives a notification.

## Localization

Supported languages:
- Russian
- English
- Japanese
- Spanish

## Dependencies

- [telegraf](https://github.com/telegraf/telegraf) — Telegram Bot API framework
- [dotenv](https://github.com/motdotla/dotenv) — environment variables
- [@vercel/node](https://vercel.com/docs/functions/serverless-functions/runtimes/node) — serverless functions for Vercel
- [typescript](https://www.typescriptlang.org/)

## Scripts

- `npm run build` — build TypeScript
- `npm run dev` — run in development mode (polling)
- `npm run start` — run (polling)
- `npm run local` — run (polling)

## License

ISC

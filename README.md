# TechSupportBot

A modern, multi-language Telegram support bot for teams and projects. Supports bug reports, feature requests, development orders, and admin ticket status management. Deployable on Vercel (webhook) and locally (polling).

---

## Features
- Multi-language support (English, Russian, Japanese, Spanish, Chinese)
- User-friendly menu with emoji and rich formatting
- Bug report, feature request, and development order flows
- Admin can change ticket status (in progress, closed, etc.)
- User receives notifications when ticket status changes
- Works on Vercel (webhook) and locally (polling)

---

## Quick Start (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nighty3098/TechSupportBot.git
   cd TechSupportBot
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your values:
     ```env
     BOT_TOKEN=your_bot_token
     SUPPORT_CHAT_USERNAME=your_support_username
     NOTIFY_CHAT=your_notify_chat_id
     ```

4. **Run the bot in polling mode:**
   ```bash
   npm run dev
   # or
   npm run local
   ```

---

## Deploy to Vercel (Webhook Mode)

1. **Push your code to GitHub.**
2. **Connect your repo to Vercel.**
3. **Set environment variables in Vercel dashboard:**
   - `BOT_TOKEN`
   - `SUPPORT_CHAT_USERNAME`
   - `NOTIFY_CHAT`
4. **Deploy!**
5. **Set the Telegram webhook:**
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<your-vercel-domain>/api/bot
   ```

---

## Project Structure

```
TechSupportBot/
├── api/
│   └── bot.ts           # Vercel serverless handler (webhook)
├── src/
│   ├── bot.ts           # Main bot logic
│   ├── local.ts         # Local entry point (polling)
│   └── locales/         # All language files
│       ├── messages.en.ts
│       ├── messages.ru.ts
│       ├── messages.ja.ts
│       ├── messages.es.ts
│       └── messages.zh.ts
├── public/
│   └── header.png       # (Optional) Local image for polling mode
├── package.json
├── vercel.json
└── README.md
```

---

## Environment Variables
- `BOT_TOKEN` — Your Telegram bot token
- `SUPPORT_CHAT_USERNAME` — Username for dev orders (without @)
- `NOTIFY_CHAT` — Chat ID for notifications (can be group/channel ID)

---

## Usage
- Users interact with the bot via menu buttons
- Admins can change ticket status via inline buttons in the support chat
- Users are notified when their ticket is in progress or closed
- Language can be changed via the menu or `/lang` command

---

## Local Development Tips
- Use polling mode for local development
- The bot will send a welcome image only in local mode (if `public/header.png` exists)
- All formatting uses HTML (`parse_mode: 'HTML'`)

---

## Vercel Deployment Tips
- The bot works as a webhook via `api/bot.ts`
- No image is sent in welcome messages on Vercel (text only)
- Make sure to set the webhook after each deploy

---

## License
MIT

import bot from './bot';

if (process.env.NODE_ENV === 'development') {
  bot.launch();
  console.log('Bot started in polling mode');
} else {
  console.log('Bot not started: use webhook mode (Vercel)');
} 

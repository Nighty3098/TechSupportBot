import type { VercelRequest, VercelResponse } from '@vercel/node';
import bot from '../src/bot';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    try {
      await bot.handleUpdate(req.body);
      res.status(200).send('ok');
    } catch (e) {
      res.status(500).send('Error');
    }
  } else {
    res.status(200).send('Bot is running');
  }
} 

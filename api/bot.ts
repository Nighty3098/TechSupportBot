import type { VercelRequest, VercelResponse } from '@vercel/node';
import bot from '../src/bot';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Включаем CORS для webhook
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    try {
      console.log('Received webhook update:', req.body);
      await bot.handleUpdate(req.body);
      res.status(200).json({ ok: true });
    } catch (error) {
      console.error('Webhook error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  } else {
    res.status(200).json({ message: 'Bot webhook endpoint is running' });
  }
} 

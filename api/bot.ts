import type { VercelRequest, VercelResponse } from '@vercel/node';
import bot from '../src/bot';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    await bot.handleUpdate(req.body);
    res.status(200).end('ok');
  } else {
    res.status(405).end();
  }
} 

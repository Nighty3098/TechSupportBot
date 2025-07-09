import type { VercelRequest, VercelResponse } from '@vercel/node';
import bot from '../src/bot';

const NOTIFY_CHAT = process.env.NOTIFY_CHAT!;

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  let message: string | undefined;
  if (req.headers['content-type']?.includes('application/json')) {
    message = req.body?.message;
  } else if (typeof req.body === 'string') {
    try {
      const parsed = JSON.parse(req.body);
      message = parsed.message;
    } catch {
      message = undefined;
    }
  }

  if (!message) {
    res.status(400).json({ error: 'No message provided' });
    return;
  }

  try {
    await bot.telegram.sendMessage(NOTIFY_CHAT, `External webhook:\n${message}`);
    res.status(200).json({ ok: true });
  } catch (error) {
    res.status(500).json({ error: 'Failed to send message' });
  }
} 

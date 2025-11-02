import type { VercelRequest, VercelResponse } from '@vercel/node';
// Forward /api/webhook to the existing /api/bot handler
import handler from './bot';

export default async function webhookHandler(req: VercelRequest, res: VercelResponse) {
  return handler(req as any, res as any);
}

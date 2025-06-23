// Файл перемещён в src/locales/messages.ja.ts

export const messages_ja = {
  welcomeCaption: `👋 <b>TechSupportBotへようこそ！</b>\n\n✨ <b>サポートチームへの連絡をお手伝いします。</b>\n\n<b>下からご希望の項目を選択してください：</b>`,
  bugReport: '🐞 <b>見つけたバグについて説明してください：</b>',
  featureRequest: '💡 <b>アイデアを説明してください：</b>',
  orderDev: (supportUsername: string) => `🛠 <b>開発依頼は</b> <a href=\"https://t.me/${supportUsername}\">@${supportUsername}</a> <b>までご連絡ください。</b>`,
  thanks: '🙏 <b>ありがとうございます！</b> ご要望は<i>サポート</i>に<b>送信されました</b>！ ��',
  bugButton: '🐞 バグ報告',
  featureButton: '💡 アイデアを提案',
  orderButton: '🛠 開発を依頼',
  ticketCaption: (
    date: string,
    username: string,
    category: string,
    status: string,
    message: string
  ) => `📝 <b>新しいリクエスト</b>\n\n📅 <b>日付:</b> <i>${date}</i>\n👤 <b>ユーザー:</b> <a href=\"https://t.me/${username}\">@${username}</a>\n📂 <b>カテゴリ:</b> <i>${category}</i>\n🔖 <b>ステータス:</b> <b>${status}</b>\n${message ? `💬 <b>メッセージ:</b> <i>${message}</i>` : ''}`,
  langButton: '🌐 言語',
  inProgressNotify: '⏳ <b>あなたのチケットは<i>対応中</i>です！</b> しばらくお待ちください。🚀',
  closedNotify: '✅ <b>あなたのチケットは<i>クローズ</i>されました。</b> ご利用ありがとうございました！🎉',
}; 

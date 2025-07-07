export const messages_ja = {
  welcomeCaption: `🫠 <b><i>TechSupportBot</i>へようこそ！</b>\n\n✨ <b>サポートチームへの連絡をお手伝いします。</b>\n\n<b>下のオプションから選択してください:</b>`,
  bugReport: '🐞 <b>発見したエラーについて説明してください。エラーに至った操作もできるだけ詳しくご記入ください。\n\nエラーログファイルや画像も添付できます。</b>',
  featureRequest: '💡 <b>ご希望のアイデアを説明してください。\n\nファイルや画像も添付できます:</b>',
  orderDev: (supportUsername: string) => `🛠 <b>開発依頼は、こちらまでご連絡ください:</b> <a href="https://t.me/${supportUsername}">@${supportUsername}</a>`,
  thanks: '🙏 <b>ありがとうございます！</b> ご依頼は<i>サポート</i>に<b>送信されました</b>！🚀',
  bugButton: '🐞 バグ報告',
  featureButton: '💡 アイデアを提案',
  orderButton: '🛠 開発を依頼',
  langButton: '🌐 言語',
  inProgressNotify: '⏳ <b>あなたのチケットは<i>対応中</i>です！</b> 返信をお待ちください。🚀',
  closedNotify: '✅ <b>あなたのチケットは<i>クローズされました</i>。</b> ご連絡ありがとうございました！🎉',
  backButton: '⬅️ 戻る'
};

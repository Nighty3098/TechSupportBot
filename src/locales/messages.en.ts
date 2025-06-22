// Файл перемещён в src/locales/messages.en.ts

export const messages_en = {
  welcomeCaption: `👋 <b>Welcome to <i>TechSupportBot</i>!</b>\n\n✨ <b>I will help you contact our team.</b>\n\n<b>Please choose an option below:</b>`,
  bugReport: '🐞 <b>Please describe the bug you found:</b>',
  featureRequest: '💡 <b>Please describe your idea:</b>',
  orderDev: (supportUsername: string) => `🛠 <b>To order development, write to us:</b> <a href=\"https://t.me/${supportUsername}\">@${supportUsername}</a>`,
  thanks: '🙏 <b>Thank you!</b> Your request has been <b>sent</b> to <i>support</i>! ��',
  bugButton: '🐞 Bug report',
  featureButton: '💡 Suggest an idea',
  orderButton: '🛠 Order development',
  ticketCaption: (
    date: string,
    username: string,
    category: string,
    status: string,
    message: string
  ) => `📝 <b>New request</b>\n\n📅 <b>Date:</b> <i>${date}</i>\n👤 <b>User:</b> <a href=\"https://t.me/${username}\">@${username}</a>\n📂 <b>Category:</b> <i>${category}</i>\n🔖 <b>Status:</b> <b>${status}</b>\n${message ? `💬 <b>Message:</b> <i>${message}</i>` : ''}`,
  langButton: '🌐 Language',
  inProgressNotify: '⏳ <b>Your ticket is now <i>in progress</i>!</b> Please wait for a response. 🚀',
  closedNotify: '✅ <b>Your ticket has been <i>closed</i>.</b> Thank you for contacting us! 🎉',
}; 

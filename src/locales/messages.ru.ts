// Файл перемещён в src/locales/messages.ru.ts

export const messages_ru = {
  welcomeCaption: `👋 <b>Добро пожаловать в <i>TechSupportBot</i>!</b>\n\n✨ <b>Я помогу вам связаться с нашей командой.</b>\n\n<b>Выберите нужный пункт ниже:</b>`,
  bugReport: '🐞 <b>Пожалуйста, опишите найденную ошибку:</b>',
  featureRequest: '💡 <b>Пожалуйста, опишите вашу идею:</b>',
  orderDev: (supportUsername: string) => `🛠 <b>Для заказа разработки напишите нам:</b> <a href=\"https://t.me/${supportUsername}\">@${supportUsername}</a>`,
  thanks: '🙏 <b>Спасибо!</b> Ваш запрос <b>отправлен</b> в <i>техподдержку</i>! ��',
  bugButton: '🐞 Баг-репорт',
  featureButton: '💡 Предложить идею',
  orderButton: '🛠 Заказать разработку',
  ticketCaption: (
    date: string,
    username: string,
    category: string,
    status: string,
    message: string
  ) => `📝 <b>Новый запрос</b>\n\n📅 <b>Дата:</b> <i>${date}</i>\n👤 <b>Пользователь:</b> <a href=\"https://t.me/${username}\">@${username}</a>\n📂 <b>Категория:</b> <i>${category}</i>\n🔖 <b>Статус:</b> <b>${status}</b>\n${message ? `💬 <b>Сообщение:</b> <i>${message}</i>` : ''}`,
  langButton: '🌐 Язык',
  inProgressNotify: '⏳ <b>Ваш тикет <i>взяли в работу</i>!</b> Ожидайте ответа. 🚀',
  closedNotify: '✅ <b>Ваш тикет <i>закрыт</i>.</b> Спасибо за обращение! 🎉',
}; 

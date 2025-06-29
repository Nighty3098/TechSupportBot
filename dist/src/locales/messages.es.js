"use strict";
// Файл перемещён в src/locales/messages.es.ts
Object.defineProperty(exports, "__esModule", { value: true });
exports.messages_es = void 0;
exports.messages_es = {
    welcomeCaption: `👋 <b>¡Bienvenido a <i>TechSupportBot</i>!</b>\n\n✨ <b>Te ayudaré a contactar con nuestro equipo.</b>\n\n<b>Elige una opción abajo:</b>`,
    bugReport: '🐞 <b>Por favor, describe el error que encontraste:</b>',
    featureRequest: '💡 <b>Por favor, describe tu idea:</b>',
    orderDev: (supportUsername) => `🛠 <b>Para solicitar desarrollo, escríbenos a:</b> <a href=\"https://t.me/${supportUsername}\">@${supportUsername}</a>`,
    thanks: '🙏 <b>¡Gracias!</b> Tu solicitud ha sido <b>enviada</b> al <i>soporte</i>! ��',
    bugButton: '🐞 Reportar un error',
    featureButton: '💡 Sugerir una idea',
    orderButton: '🛠 Solicitar desarrollo',
    ticketCaption: (date, username, category, status, message) => `📝 <b>Nueva solicitud</b>\n\n📅 <b>Fecha:</b> <i>${date}</i>\n👤 <b>Usuario:</b> <a href=\"https://t.me/${username}\">@${username}</a>\n📂 <b>Categoría:</b> <i>${category}</i>\n🔖 <b>Estado:</b> <b>${status}</b>\n${message ? `💬 <b>Mensaje:</b> <i>${message}</i>` : ''}`,
    langButton: '🌐 Idioma',
    inProgressNotify: '⏳ <b>¡Tu ticket está <i>en proceso</i>!</b> Por favor, espera una respuesta. 🚀',
    closedNotify: '✅ <b>Tu ticket ha sido <i>cerrado</i>.</b> ¡Gracias por contactarnos! 🎉',
};

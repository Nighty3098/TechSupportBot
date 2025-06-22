"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const dotenv_1 = require("dotenv");
const telegraf_1 = require("telegraf");
(0, dotenv_1.config)();
const BOT_TOKEN = process.env.BOT_TOKEN;
const ADMIN_USERNAME = process.env.ADMIN_USERNAME;
const SUPPORT_CHAT_USERNAME = process.env.SUPPORT_CHAT_USERNAME;
const bot = new telegraf_1.Telegraf(BOT_TOKEN);
const WELCOME_IMAGE = 'https://i.imgur.com/0y0y0y0.png'; // Замените на свою картинку
const mainMenu = telegraf_1.Markup.inlineKeyboard([
    [telegraf_1.Markup.button.callback('🐞 Баг-репорт', 'bug_report')],
    [telegraf_1.Markup.button.callback('💡 Предложить идею', 'feature_request')],
    [telegraf_1.Markup.button.callback('🛠 Заказать разработку', 'order_dev')],
    [telegraf_1.Markup.button.callback('✉️ Связаться с командой', 'contact_team')],
]);
bot.use((0, telegraf_1.session)());
bot.start((ctx) => __awaiter(void 0, void 0, void 0, function* () {
    yield ctx.replyWithPhoto(WELCOME_IMAGE, Object.assign({ caption: `👋 Добро пожаловать в TechSupportBot!\n\nЯ помогу вам связаться с нашей командой. Выберите нужный пункт ниже:` }, mainMenu));
}));
bot.action('bug_report', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    ctx.session = { category: 'Баг', step: 'ask_message' };
    yield ctx.reply('Пожалуйста, опишите найденную ошибку:');
}));
bot.action('feature_request', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    ctx.session = { category: 'Фича', step: 'ask_message' };
    yield ctx.reply('Пожалуйста, опишите вашу идею:');
}));
bot.action('order_dev', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    yield ctx.reply('Для заказа разработки напишите нам: @' + SUPPORT_CHAT_USERNAME);
}));
bot.action('contact_team', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    yield ctx.reply('Связаться с командой: @' + SUPPORT_CHAT_USERNAME);
}));
bot.on('text', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    var _a, _b, _c;
    if (ctx.session && ctx.session.step === 'ask_message') {
        const category = ctx.session.category;
        const message = ctx.message.text;
        const date = new Date().toLocaleString('ru-RU');
        const username = ((_a = ctx.from) === null || _a === void 0 ? void 0 : _a.username) || ((_b = ctx.from) === null || _b === void 0 ? void 0 : _b.first_name);
        const formatted = `📝 Новый запрос\n\nДата: ${date}\nПользователь: @${username}\nКатегория: ${category}\nСообщение: ${message}`;
        yield ctx.telegram.sendMessage(`@${SUPPORT_CHAT_USERNAME}`, formatted, {
            reply_markup: {
                inline_keyboard: [
                    [
                        { text: 'В работе', callback_data: 'status_in_progress' },
                        { text: 'Закрыто', callback_data: 'status_closed' },
                        { text: 'Ответить', callback_data: `reply_user_${(_c = ctx.from) === null || _c === void 0 ? void 0 : _c.id}` },
                    ],
                ],
            },
        });
        yield ctx.reply('Спасибо! Ваш запрос отправлен в техподдержку.');
        ctx.session = {};
    }
}));
exports.default = bot;

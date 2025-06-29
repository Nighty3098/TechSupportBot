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
const fs_1 = require("fs");
const messages_ru_1 = require("./locales/messages.ru");
const messages_en_1 = require("./locales/messages.en");
const messages_ja_1 = require("./locales/messages.ja");
const messages_es_1 = require("./locales/messages.es");
const messages_zh_1 = require("./locales/messages.zh");
(0, dotenv_1.config)();
const BOT_TOKEN = process.env.BOT_TOKEN;
const ADMIN_USERNAME = process.env.ADMIN_USERNAME;
const SUPPORT_CHAT_USERNAME = process.env.SUPPORT_CHAT_USERNAME;
const NOTIFY_CHAT = process.env.NOTIFY_CHAT;
const bot = new telegraf_1.Telegraf(BOT_TOKEN);
const WELCOME_IMAGE_PATH = 'public/header.png';
const mainMenu = (ctx) => {
    const MESSAGES = getMessages(ctx);
    return telegraf_1.Markup.inlineKeyboard([
        [telegraf_1.Markup.button.callback(MESSAGES.bugButton, 'bug_report')],
        [telegraf_1.Markup.button.callback(MESSAGES.featureButton, 'feature_request')],
        [telegraf_1.Markup.button.callback(MESSAGES.orderButton, 'order_dev')],
        [telegraf_1.Markup.button.callback(MESSAGES.langButton, 'choose_lang')],
    ]);
};
bot.use((0, telegraf_1.session)());
// Возможные статусы тикета
const TICKET_STATUSES = [
    { key: 'new', label: 'New' },
    { key: 'in_progress', label: 'In development' },
    { key: 'closed', label: 'Completed' },
    { key: 'review', label: 'On review' },
];
function getStatusLabel(key) {
    var _a;
    return ((_a = TICKET_STATUSES.find((s) => s.key === key)) === null || _a === void 0 ? void 0 : _a.label) || 'Unknown';
}
const LANGUAGES = {
    ru: { name: 'Русский', messages: messages_ru_1.messages_ru },
    en: { name: 'English', messages: messages_en_1.messages_en },
    ja: { name: '日本語', messages: messages_ja_1.messages_ja },
    es: { name: 'Español', messages: messages_es_1.messages_es },
    zh: { name: '中文', messages: messages_zh_1.messages_zh },
};
function getUserLang(ctx) {
    if (!ctx.session)
        return 'en';
    return ctx.session.lang || 'en';
}
function getMessages(ctx) {
    return LANGUAGES[getUserLang(ctx)].messages;
}
bot.command('lang', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    yield ctx.reply('Выберите язык / Choose your language / 言語を選択してください / Elige tu idioma / 请选择语言:', {
        reply_markup: {
            inline_keyboard: Object.entries(LANGUAGES).map(([code, { name }]) => [
                { text: name, callback_data: `setlang_${code}` }
            ])
        }
    });
}));
bot.action(/setlang_(\w+)/, (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const lang = ctx.match[1];
    if (!ctx.session)
        ctx.session = {};
    if (lang in LANGUAGES) {
        ctx.session.lang = lang;
        yield ctx.answerCbQuery('Язык изменён / Language changed');
        const MESSAGES = LANGUAGES[lang].messages;
        yield ctx.replyWithPhoto({ source: (0, fs_1.createReadStream)(WELCOME_IMAGE_PATH) }, Object.assign(Object.assign({ caption: MESSAGES.welcomeCaption }, mainMenu(ctx)), { parse_mode: 'HTML' }));
    }
    else {
        yield ctx.answerCbQuery('Unknown language');
    }
}));
bot.start((ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const MESSAGES = getMessages(ctx);
    yield ctx.replyWithPhoto({ source: (0, fs_1.createReadStream)(WELCOME_IMAGE_PATH) }, Object.assign(Object.assign({ caption: MESSAGES.welcomeCaption }, mainMenu(ctx)), { parse_mode: 'HTML' }));
}));
bot.action('bug_report', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    ctx.session = Object.assign(Object.assign({}, ctx.session), { category: 'Баг', step: 'ask_message' });
    const MESSAGES = getMessages(ctx);
    yield ctx.reply(MESSAGES.bugReport, { parse_mode: 'HTML' });
}));
bot.action('feature_request', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    ctx.session = Object.assign(Object.assign({}, ctx.session), { category: 'Фича', step: 'ask_message' });
    const MESSAGES = getMessages(ctx);
    yield ctx.reply(MESSAGES.featureRequest, { parse_mode: 'HTML' });
}));
bot.action('order_dev', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const MESSAGES = getMessages(ctx);
    yield ctx.reply(MESSAGES.orderDev(SUPPORT_CHAT_USERNAME), { parse_mode: 'HTML' });
}));
bot.action('choose_lang', (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    yield ctx.reply('Выберите язык / Choose your language / 言語を選択してください / Elige tu idioma / 请选择语言:', {
        reply_markup: {
            inline_keyboard: Object.entries(LANGUAGES).map(([code, { name }]) => [
                { text: name, callback_data: `setlang_${code}` }
            ])
        },
        parse_mode: 'HTML',
    });
}));
bot.on(['text', 'photo', 'video', 'document'], (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    var _a, _b, _c;
    if (ctx.session && ctx.session.step === 'ask_message') {
        const category = ctx.session.category || 'unknown';
        const msg = ctx.message;
        const message = msg.text || msg.caption || '';
        const date = new Date().toLocaleString('ru-RU');
        const username = ((_a = ctx.from) === null || _a === void 0 ? void 0 : _a.username) || ((_b = ctx.from) === null || _b === void 0 ? void 0 : _b.first_name) || 'unknown';
        const status = 'new';
        const userId = (_c = ctx.from) === null || _c === void 0 ? void 0 : _c.id;
        const MESSAGES = getMessages(ctx);
        const fullCaption = MESSAGES.ticketCaption(date, username, category, getStatusLabel(status), message);
        if (msg.photo && Array.isArray(msg.photo)) {
            const photo = msg.photo[msg.photo.length - 1];
            yield ctx.telegram.sendPhoto(NOTIFY_CHAT, photo.file_id, { caption: fullCaption, parse_mode: 'HTML' });
        }
        else if (msg.video) {
            yield ctx.telegram.sendVideo(NOTIFY_CHAT, msg.video.file_id, { caption: fullCaption, parse_mode: 'HTML' });
        }
        else if (msg.document) {
            yield ctx.telegram.sendDocument(NOTIFY_CHAT, msg.document.file_id, { caption: fullCaption, parse_mode: 'HTML' });
        }
        else {
            yield ctx.telegram.sendMessage(NOTIFY_CHAT, fullCaption, {
                reply_markup: {
                    inline_keyboard: [
                        [
                            { text: `Статус: ${getStatusLabel(status)}`, callback_data: `ticket_status_menu|${status}|${userId}` }
                        ],
                    ],
                },
                parse_mode: 'HTML',
            });
        }
        yield ctx.reply(MESSAGES.thanks, { parse_mode: 'HTML' });
        ctx.session = Object.assign(Object.assign({}, ctx.session), { step: undefined, category: undefined });
        yield ctx.replyWithPhoto({ source: (0, fs_1.createReadStream)(WELCOME_IMAGE_PATH) }, Object.assign(Object.assign({ caption: MESSAGES.welcomeCaption }, mainMenu(ctx)), { parse_mode: 'HTML' }));
    }
}));
// Открытие меню изменения статуса
bot.action(/ticket_status_menu\|([^|]+)\|(\d+)/, (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const currentStatus = ctx.match[1];
    const userId = ctx.match[2];
    yield ctx.answerCbQuery();
    yield ctx.editMessageReplyMarkup({
        inline_keyboard: [
            TICKET_STATUSES.filter(s => s.key !== currentStatus).map(s => ({
                text: s.label,
                callback_data: `set_ticket_status|${s.key}|${userId}`
            })),
            [
                { text: `Статус: ${getStatusLabel(currentStatus)}`, callback_data: `ticket_status_menu|${currentStatus}|${userId}` }
            ]
        ]
    });
}));
// Изменение статуса тикета
bot.action(/set_ticket_status\|([^|]+)\|(\d+)/, (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const newStatus = ctx.match[1];
    const userId = ctx.match[2];
    // @ts-ignore
    const oldText = ctx.update.callback_query.message.text;
    const newText = oldText.replace(/Статус: .*/, `Статус: ${getStatusLabel(newStatus)}`);
    yield ctx.editMessageText(newText, {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: `Статус: ${getStatusLabel(newStatus)}`, callback_data: `ticket_status_menu|${newStatus}|${userId}` }
                ],
            ],
        },
    });
    // Оповещение пользователя о смене статуса
    let notifyText = '';
    if (newStatus === 'in_progress') {
        notifyText = LANGUAGES['en'].messages.inProgressNotify;
    }
    else if (newStatus === 'closed') {
        notifyText = LANGUAGES['en'].messages.closedNotify;
    }
    if (notifyText && userId) {
        try {
            yield ctx.telegram.sendMessage(userId, notifyText, { parse_mode: 'HTML' });
        }
        catch (e) {
            // ignore if user has blocked bot or can't be reached
        }
    }
    yield ctx.answerCbQuery('Статус обновлён');
}));
exports.default = bot;

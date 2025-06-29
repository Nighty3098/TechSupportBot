import { config } from "dotenv";
import {
  Telegraf,
  Markup,
  Context as TelegrafContext,
  session as telegrafSession,
} from "telegraf";
import { messages_ru } from "./locales/messages.ru";
import { messages_en } from "./locales/messages.en";
import { messages_ja } from "./locales/messages.ja";
import { messages_es } from "./locales/messages.es";
import { messages_zh } from "./locales/messages.zh";

config();

const BOT_TOKEN = process.env.BOT_TOKEN!;
const SUPPORT_CHAT_USERNAME = process.env.SUPPORT_CHAT_USERNAME!;
const NOTIFY_CHAT = process.env.NOTIFY_CHAT!;

interface MySession {
  category?: string;
  step?: string;
  replyToUserId?: number;
  lang?: string;
}

interface MyContext extends TelegrafContext {
  session: MySession;
}

const bot = new Telegraf<MyContext>(BOT_TOKEN);

const mainMenu = (ctx: MyContext) => {
  const MESSAGES = getMessages(ctx);
  return Markup.inlineKeyboard([
    [Markup.button.callback(MESSAGES.bugButton, "bug_report")],
    [Markup.button.callback(MESSAGES.featureButton, "feature_request")],
    [Markup.button.callback(MESSAGES.orderButton, "order_dev")],
    [Markup.button.callback(MESSAGES.langButton, "choose_lang")],
  ]);
};

bot.use(telegrafSession());

declare module "telegraf" {
  interface SessionData {
    category?: string;
    step?: string;
  }
}

// Возможные статусы тикета
const TICKET_STATUSES = [
  { key: "new", label: "New" },
  { key: "in_progress", label: "In development" },
  { key: "closed", label: "Completed" },
  { key: "review", label: "On review" },
];

function getStatusLabel(key: string) {
  return TICKET_STATUSES.find((s) => s.key === key)?.label ?? "Unknown";
}

const LANGUAGES = {
  ru: { name: "Русский", messages: messages_ru },
  en: { name: "English", messages: messages_en },
  ja: { name: "日本語", messages: messages_ja },
  es: { name: "Español", messages: messages_es },
  zh: { name: "中文", messages: messages_zh },
};

function getUserLang(ctx: MyContext): keyof typeof LANGUAGES {
  if (!ctx.session) return "en";
  return (ctx.session.lang as keyof typeof LANGUAGES) ?? "en";
}

function getMessages(ctx: MyContext) {
  return LANGUAGES[getUserLang(ctx) as keyof typeof LANGUAGES].messages;
}

bot.command("lang", async (ctx) => {
  await ctx.reply(
    "Выберите язык / Choose your language / 言語を選択してください / Elige tu idioma / 请选择语言:",
    {
      reply_markup: {
        inline_keyboard: Object.entries(LANGUAGES).map(([code, { name }]) => [
          { text: name, callback_data: `setlang_${code}` },
        ]),
      },
    },
  );
});

bot.action(/setlang_(\w+)/, async (ctx) => {
  const lang = ctx.match[1];
  if (!ctx.session) ctx.session = {};
  if (lang in LANGUAGES) {
    ctx.session.lang = lang;
    await ctx.answerCbQuery("Язык изменён / Language changed");
    const MESSAGES = LANGUAGES[lang as keyof typeof LANGUAGES].messages;
    await ctx.reply(MESSAGES.welcomeCaption, {
      ...mainMenu(ctx as MyContext),
      parse_mode: "HTML",
    });
  } else {
    await ctx.answerCbQuery("Unknown language");
  }
});

bot.start(async (ctx) => {
  const MESSAGES = getMessages(ctx);
  await ctx.reply(MESSAGES.welcomeCaption, {
    ...mainMenu(ctx),
    parse_mode: "HTML",
  });
});

bot.action("bug_report", async (ctx) => {
  ctx.session = { ...ctx.session, category: "Баг", step: "ask_message" };
  const MESSAGES = getMessages(ctx);
  await ctx.reply(MESSAGES.bugReport, { parse_mode: "HTML" });
});

bot.action("feature_request", async (ctx) => {
  ctx.session = { ...ctx.session, category: "Фича", step: "ask_message" };
  const MESSAGES = getMessages(ctx);
  await ctx.reply(MESSAGES.featureRequest, { parse_mode: "HTML" });
});

bot.action("order_dev", async (ctx) => {
  const MESSAGES = getMessages(ctx);
  await ctx.reply(MESSAGES.orderDev(SUPPORT_CHAT_USERNAME), {
    parse_mode: "HTML",
  });
});

bot.action("choose_lang", async (ctx) => {
  await ctx.reply(
    "Выберите язык / Choose your language / 言語を選択してください / Elige tu idioma / 请选择语言:",
    {
      reply_markup: {
        inline_keyboard: Object.entries(LANGUAGES).map(([code, { name }]) => [
          { text: name, callback_data: `setlang_${code}` },
        ]),
      },
      parse_mode: "HTML",
    },
  );
});

bot.on(["text", "photo", "video", "document"], async (ctx) => {
  if (ctx.session && ctx.session.step === "ask_message") {
    const category = ctx.session.category ?? "unknown";
    const msg = ctx.message as any;
    const message = msg.text ?? msg.caption ?? "";
    const date = new Date().toLocaleString("ru-RU");
    const username = ctx.from?.username ?? ctx.from?.first_name ?? "unknown";
    const status = "new";
    const userId = ctx.from?.id;
    const MESSAGES = getMessages(ctx);
    const fullCaption = MESSAGES.ticketCaption(
      date,
      username,
      category,
      getStatusLabel(status),
      message,
    );

    if (msg.photo && Array.isArray(msg.photo)) {
      const photo = msg.photo[msg.photo.length - 1];
      await ctx.telegram.sendPhoto(NOTIFY_CHAT, photo.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
      });
    } else if (msg.video) {
      await ctx.telegram.sendVideo(NOTIFY_CHAT, msg.video.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
      });
    } else if (msg.document) {
      await ctx.telegram.sendDocument(NOTIFY_CHAT, msg.document.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
      });
    } else {
      await ctx.telegram.sendMessage(NOTIFY_CHAT, fullCaption, {
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: `Статус: ${getStatusLabel(status)}`,
                callback_data: `ticket_status_menu|${status}|${userId}`,
              },
            ],
          ],
        },
        parse_mode: "HTML",
      });
    }

    await ctx.reply(MESSAGES.thanks, { parse_mode: "HTML" });
    ctx.session = { ...ctx.session, step: undefined, category: undefined };
    await ctx.reply(MESSAGES.welcomeCaption, {
      ...mainMenu(ctx),
      parse_mode: "HTML",
    });
  }
});

// Открытие меню изменения статуса
bot.action(/ticket_status_menu\|([^|]+)\|(\d+)/, async (ctx) => {
  const currentStatus = ctx.match[1];
  const userId = ctx.match[2];
  await ctx.answerCbQuery();
  await ctx.editMessageReplyMarkup({
    inline_keyboard: [
      TICKET_STATUSES.filter((s) => s.key !== currentStatus).map((s) => ({
        text: s.label,
        callback_data: `set_ticket_status|${s.key}|${userId}`,
      })),
      [
        {
          text: `Статус: ${getStatusLabel(currentStatus)}`,
          callback_data: `ticket_status_menu|${currentStatus}|${userId}`,
        },
      ],
    ],
  });
});

// Изменение статуса тикета
bot.action(/set_ticket_status\|([^|]+)\|(\d+)/, async (ctx) => {
  const newStatus = ctx.match[1];
  const userId = ctx.match[2];
  // @ts-ignore
  const oldText = ctx.update.callback_query.message.text as string;
  const newText = oldText.replace(
    /Статус: .*/,
    `Статус: ${getStatusLabel(newStatus)}`,
  );
  await ctx.editMessageText(newText, {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: `Статус: ${getStatusLabel(newStatus)}`,
            callback_data: `ticket_status_menu|${newStatus}|${userId}`,
          },
        ],
      ],
    },
  });
  // Оповещение пользователя о смене статуса
  let notifyText = "";
  if (newStatus === "in_progress") {
    notifyText = LANGUAGES["en"].messages.inProgressNotify;
  } else if (newStatus === "closed") {
    notifyText = LANGUAGES["en"].messages.closedNotify;
  }
  if (notifyText && userId) {
    try {
      await ctx.telegram.sendMessage(userId, notifyText, {
        parse_mode: "HTML",
      });
    } catch (e) {
      // ignore if user has blocked bot or can't be reached
    }
  }
  await ctx.answerCbQuery("Статус обновлён");
});

export default bot;

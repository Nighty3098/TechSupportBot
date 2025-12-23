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

config();

const BOT_TOKEN = process.env.BOT_TOKEN!;
const SUPPORT_CHAT_USERNAME = process.env.SUPPORT_CHAT_USERNAME!;
const NOTIFY_CHAT = process.env.NOTIFY_CHAT!;
const WELCOME_IMAGE_URL =
  "https://github.com/Nighty3098/Nighty3098/blob/main/w.jpeg?raw=true";

function ticketCaption(
  date: string,
  username: string,
  category: string,
  status: string,
  message: string,
): string {
  let caption = "📝 <b>New request</b>\n\n";
  caption += `📅 <b>Date:</b> <i>${date}</i>\n`;
  caption += `👤 <b>User:</b> <a href="https://t.me/${username}">@${username}</a>\n`;
  caption += `📂 <b>Category:</b> <i>${category}</i>\n`;
  caption += `🔖 <b>Status:</b> <b>${status}</b>\n`;
  if (message) {
    caption += "💬 <b>Message:</b> <i>" + message + "</i>";
  }
  return caption;
}

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
};

function getUserLang(ctx: MyContext): keyof typeof LANGUAGES {
  if (!ctx.session) return "en";
  return (ctx.session.lang as keyof typeof LANGUAGES) ?? "en";
}

function getMessages(ctx: MyContext) {
  return LANGUAGES[getUserLang(ctx)].messages;
}

bot.action(/setlang_(\w+)/, async (ctx) => {
  const lang = ctx.match[1];
  if (!ctx.session) ctx.session = {};
  if (lang in LANGUAGES) {
    ctx.session.lang = lang;
    await ctx.answerCbQuery("Язык изменён / Language changed");
    const MESSAGES = LANGUAGES[lang as keyof typeof LANGUAGES].messages;
    await ctx.replyWithPhoto(
      { url: WELCOME_IMAGE_URL },
      {
        caption: MESSAGES.welcomeCaption,
        ...mainMenu(ctx as MyContext),
        parse_mode: "HTML",
      },
    );
  } else {
    await ctx.answerCbQuery("Unknown language");
  }
});

bot.start(async (ctx) => {
  const MESSAGES = getMessages(ctx);
  await ctx.replyWithPhoto(
    { url: WELCOME_IMAGE_URL },
    {
      caption: MESSAGES.welcomeCaption,
      ...mainMenu(ctx),
      parse_mode: "HTML",
    },
  );
});

bot.action("to_main", async (ctx) => {
  ctx.session.step = undefined;
  ctx.session.category = undefined;
  const MESSAGES = getMessages(ctx);
  await ctx.editMessageCaption(MESSAGES.welcomeCaption, {
    ...mainMenu(ctx),
    parse_mode: "HTML",
  });
});

bot.action("bug_report", async (ctx) => {
  ctx.session = { ...ctx.session, category: "Bug", step: "ask_message" };
  const MESSAGES = getMessages(ctx);
  await ctx.editMessageCaption(MESSAGES.bugReport, {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [{ text: MESSAGES.backButton, callback_data: "to_main" }],
      ],
    },
  });
});

bot.action("feature_request", async (ctx) => {
  ctx.session = { ...ctx.session, category: "Feature", step: "ask_message" };
  const MESSAGES = getMessages(ctx);
  await ctx.editMessageCaption(MESSAGES.featureRequest, {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [{ text: MESSAGES.backButton, callback_data: "to_main" }],
      ],
    },
  });
});

bot.action("order_dev", async (ctx) => {
  const MESSAGES = getMessages(ctx);
  await ctx.editMessageCaption(MESSAGES.orderDev(SUPPORT_CHAT_USERNAME), {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [{ text: MESSAGES.backButton, callback_data: "to_main" }],
      ],
    },
  });
});

bot.action("choose_lang", async (ctx) => {
  if (!ctx.session) ctx.session = {};
  ctx.session.step = undefined;
  ctx.session.category = undefined;
  const MESSAGES = getMessages(ctx);
  const langButtons = Object.entries(LANGUAGES).map(([code, { name }]) => [
    { text: name, callback_data: `setlang_${code}` },
  ]);
  langButtons.push([{ text: MESSAGES.backButton, callback_data: "to_main" }]);
  await ctx.editMessageCaption(
    "Выберите язык / Choose your language / 言語を選択してください / Elige tu idioma:",
    {
      reply_markup: {
        inline_keyboard: langButtons,
      },
      parse_mode: "HTML",
    },
  );
});

bot.on("message", async (ctx) => {
  if (ctx.session && ctx.session.step === "ask_message") {
    const category = ctx.session.category ?? "unknown";
    const msg = ctx.message as any;
    const message = msg.text || msg.caption || "";
    const date = new Date().toLocaleString("ru-RU");
    const username = ctx.from?.username ?? ctx.from?.first_name ?? "unknown";
    const status = "new";
    const userId = ctx.from?.id;
    const MESSAGES = getMessages(ctx);
    const fullCaption = ticketCaption(
      date,
      username,
      category,
      getStatusLabel(status),
      message,
    );

    if (Array.isArray(msg.photo)) {
      const photo = msg.photo[msg.photo.length - 1];
      await ctx.telegram.sendPhoto(NOTIFY_CHAT, photo.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: `Status: ${getStatusLabel(status)}`,
                callback_data: `ticket_status_menu|${status}|${userId}`,
              },
            ],
          ],
        },
      });
    } else if (msg.video) {
      await ctx.telegram.sendVideo(NOTIFY_CHAT, msg.video.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: `Status: ${getStatusLabel(status)}`,
                callback_data: `ticket_status_menu|${status}|${userId}`,
              },
            ],
          ],
        },
      });
    } else if (msg.document) {
      await ctx.telegram.sendDocument(NOTIFY_CHAT, msg.document.file_id, {
        caption: fullCaption,
        parse_mode: "HTML",
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: `Status: ${getStatusLabel(status)}`,
                callback_data: `ticket_status_menu|${status}|${userId}`,
              },
            ],
          ],
        },
      });
    } else {
      await ctx.telegram.sendMessage(NOTIFY_CHAT, fullCaption, {
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: `Status: ${getStatusLabel(status)}`,
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
    await ctx.replyWithPhoto(
      { url: WELCOME_IMAGE_URL },
      {
        caption: MESSAGES.welcomeCaption,
        ...mainMenu(ctx),
        parse_mode: "HTML",
      },
    );
  }
});

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
          text: `Status: ${getStatusLabel(currentStatus)}`,
          callback_data: `ticket_status_menu|${currentStatus}|${userId}`,
        },
      ],
    ],
  });
});

bot.action(/set_ticket_status\|([^|]+)\|(\d+)/, async (ctx) => {
  const newStatus = ctx.match[1];
  const userId = ctx.match[2];
  // @ts-ignore
  const msg = ctx.update.callback_query.message;
  let oldText: string | undefined = undefined;
  let oldCaption: string | undefined = undefined;
  if (msg && "text" in msg && typeof msg.text === "string") {
    oldText = msg.text;
  }
  if (msg && "caption" in msg && typeof msg.caption === "string") {
    oldCaption = msg.caption;
  }
  const statusLabel = `Status: ${getStatusLabel(newStatus)}`;
  const reply_markup = {
    inline_keyboard: [
      [
        {
          text: statusLabel,
          callback_data: `ticket_status_menu|${newStatus}|${userId}`,
        },
      ],
    ],
  };
  if (oldText) {
    const newText = oldText.replace(/Status: .*/, statusLabel);
    await ctx.editMessageText(newText, {
      reply_markup,
    });
  } else if (oldCaption) {
    const newCaption = oldCaption.replace(/Status: .*/, statusLabel);
    await ctx.editMessageCaption(newCaption, {
      reply_markup,
      parse_mode: "HTML",
    });
  }
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
      // Log the error for debugging but don't throw - user might have blocked bot
      console.warn(`Failed to send status notification to user ${userId}:`, e);
    }
  }
  await ctx.answerCbQuery("Status updated");
});

bot.catch((err, ctx) => {
  console.error("Error:", err);

  if (process.env.DEVS) {
    ctx.telegram.sendMessage(process.env.DEVS, "Error: " + err).catch(() => {});
  }
});

export default bot;

"use strict";
// Файл перемещён в src/locales/messages.zh.ts
Object.defineProperty(exports, "__esModule", { value: true });
exports.messages_zh = void 0;
exports.messages_zh = {
    welcomeCaption: `👋 <b>欢迎使用 <i>TechSupportBot</i>！</b>\n\n✨ <b>我会帮助您联系我们的团队。</b>\n\n<b>请选择下方的选项：</b>`,
    bugReport: '🐞 <b>请描述您发现的错误：</b>',
    featureRequest: '💡 <b>请描述您的想法：</b>',
    orderDev: (supportUsername) => `🛠 <b>如需开发服务，请联系我们：</b> <a href=\"https://t.me/${supportUsername}\">@${supportUsername}</a>`,
    thanks: '🙏 <b>谢谢！</b> 您的请求已<b>发送</b>到<i>技术支持</i>！ ��',
    bugButton: '🐞 报告错误',
    featureButton: '💡 提出想法',
    orderButton: '🛠 需求开发',
    ticketCaption: (date, username, category, status, message) => `📝 <b>新请求</b>\n\n📅 <b>日期:</b> <i>${date}</i>\n👤 <b>用户:</b> <a href=\"https://t.me/${username}\">@${username}</a>\n📂 <b>类别:</b> <i>${category}</i>\n🔖 <b>状态:</b> <b>${status}</b>\n${message ? `💬 <b>消息:</b> <i>${message}</i>` : ''}`,
    langButton: '🌐 语言',
    inProgressNotify: '⏳ <b>您的工单已进入<i>处理中</i>！</b> 请耐心等待回复。🚀',
    closedNotify: '✅ <b>您的工单已<i>关闭</i>。</b> 感谢您的联系！🎉',
};

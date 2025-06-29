"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const bot_1 = __importDefault(require("./bot"));
if (process.env.NODE_ENV === 'development') {
    bot_1.default.launch();
    console.log('Bot started in polling mode');
}
else {
    console.log('Bot not started: use webhook mode (Vercel)');
}

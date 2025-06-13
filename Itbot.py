import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))
PORT = int(os.environ.get("PORT", "8443"))

HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if not HOST:
    HOST = "localhost"

if '\n' in HOST or ' ' in HOST:
    raise ValueError(f"❌ Некорректный HOST: '{HOST}'")

print(f"✅ Webhook URL: https://{HOST}/webhook")

course_text = """ ... твой текст курса ... """

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Хочу на курс", callback_data="sign_up")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_markdown_v2(course_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = user.username or f"id:{user.id}"

    await query.edit_message_text(
        text=f"✅ Спасибо за интерес! Можете написать мне 👉 [@IT_StepUp](https://t.me/IT_StepUp)",
        parse_mode='MarkdownV2'
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"✉️ Новый запрос от @{username} ({user.first_name}) хочет на курс!"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    if HOST == "localhost":
        app.run_polling()
    else:
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"https://{HOST}/webhook"
        )

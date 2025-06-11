import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = os.environ.get("8121925945:AAGzK-Xj4ubzBQoxAoC0YwOZq-ejkDXzmlw")
ADMIN_CHAT_ID = os.environ.get("IT_StepUp")  # твой Telegram user ID
PORT = int(os.environ.get("PORT", "8443"))

course_text = """
🚀 *Летний курс по веб-разработке для подростков (13–16 лет)*  
💻 Научись создавать сайты с нуля — живые уроки в классе!  
🌟 IT — одна из самых востребованных профессий в мире!

📍 *Занятия:* в компьютерной аудитории, за нашими ПК  
🧑‍🏫 *Язык обучения:* русский, опытный преподаватель  
🌐 HTML + CSS + VS Code + GitHub  
📁 Создание мини-сайтов для портфолио  
📡 Публикация проектов онлайн

👨‍👩‍👧 Пока ребёнок учится — у вас есть время на себя!

✅ *Формат:*  
Возраст: 13–16 лет  
12 занятий × 1.5 ч, 2 раза в неделю  
💶 Стоимость: *264 €* за курс  
👥 Мини-группа = максимум практики  
🗓 *Старт:* 1 июля 2025  
📍 *Локация:* Пилайте  
⏳ Мест ограничено!

📩 Нажмите кнопку ниже, чтобы записаться или узнать подробности.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Хочу на курс", callback_data="sign_up")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_markdown_v2(course_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = user.username or f"id:{user.id}"

    # Сообщение пользователю
    await query.edit_message_text(
        text=f"✅ Спасибо за интерес! Можете написать мне 👉 [@IT_StepUp](https://t.me/@IT_StepUp)",
        parse_mode='Markdown'
    )

    # Уведомление админу
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"✉️ Новый запрос от @{username} ({user.first_name}) хочет на курс!"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    )

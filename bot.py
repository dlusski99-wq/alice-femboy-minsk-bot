import os
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    if not DEEPSEEK_API_KEY:
        await update.message.reply_text("❌ API ключ DeepSeek не найден!")
        return

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_text}]
            },
            timeout=30
        )

        data = response.json()

        if "choices" not in data:
            await update.message.reply_text("DeepSeek ошибка:\n" + str(data))
            return

        answer = data["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    # Небольшая задержка, чтобы Railway успел настроить всё
    time.sleep(3)
    
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN не найден!")
        return

    print("🚀 Бот запускается...")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # drop_pending_updates=True решает проблему с конфликтами
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

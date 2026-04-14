import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("🚀 Бот запускается...")
print(f"Проверка TELEGRAM_TOKEN: {'✅' if os.getenv('TELEGRAM_TOKEN') else '❌'}")
print(f"Проверка DEEPSEEK_API_KEY: {'✅' if os.getenv('DEEPSEEK_API_KEY') else '❌'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я бот с DeepSeek. Просто напиши мне сообщение!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        await update.message.reply_text("❌ Ошибка: API ключ DeepSeek не настроен")
        return
    
    await update.message.reply_text("🤔 Думаю...")
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_text}]
            },
            timeout=30
        )
        
        result = response.json()
        
        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text(f"Ошибка: {result}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        print("❌ Ошибка: TELEGRAM_TOKEN не найден!")
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот успешно запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

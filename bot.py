import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ДИАГНОСТИКА ПРИ ЗАПУСКЕ
print("=" * 50)
print("ДИАГНОСТИКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ:")
print(f"TELEGRAM_TOKEN: {'✅ Есть' if os.getenv('TELEGRAM_TOKEN') else '❌ НЕТ'}")
print(f"DEEPSEEK_API_KEY: {'✅ Есть' if os.getenv('DEEPSEEK_API_KEY') else '❌ НЕТ'}")
if os.getenv('DEEPSEEK_API_KEY'):
    key = os.getenv('DEEPSEEK_API_KEY')
    print(f"Длина ключа: {len(key)} символов")
    print(f"Начало ключа: {key[:15]}...")
print("=" * 50)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    if not DEEPSEEK_API_KEY:
        await update.message.reply_text("❌ API ключ DeepSeek не найден в переменных окружения!")
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

async def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN не найден!")
        return

    print("🚀 Запуск бота...")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Ключевое решение: используем drop_pending_updates и читаем обновления вручную
    await app.initialize()
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    
    print("✅ Бот успешно запущен и работает!")
    
    # Держим бота работающим
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Остановка бота...")
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())

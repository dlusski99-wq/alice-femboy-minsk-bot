import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Это комментарий
# Он ничего не делает
# Он ничего не делает
# Его можно вставить куда угодно


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # ===== ДИАГНОСТИКА - покажет все переменные с DeepSeek =====
    print("=== ВСЕ ПЕРЕМЕННЫЕ С DEEPSEEK или API ===")
    for key, value in os.environ.items():
        if "DEEP" in key.upper() or "API" in key.upper():
            preview = value[:20] if value else "None"
            print(f"{key} = {preview}...")
    print("===========================================")
    
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    print("DEEPSEEK_API_KEY =", DEEPSEEK_API_KEY)
    print("Тип переменной:", type(DEEPSEEK_API_KEY))
    print("Длина ключа:", len(DEEPSEEK_API_KEY) if DEEPSEEK_API_KEY else 0)
    # =================================================

    # Проверка: если ключа нет - сразу ошибка
    if not DEEPSEEK_API_KEY:
        await update.message.reply_text("❌ Ошибка: API ключ DeepSeek не найден в переменных окружения!")
        return

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": user_text}
            ]
        }
    )

    data = response.json()

    if "choices" not in data:
        await update.message.reply_text("DeepSeek вернул ошибку:\n" + str(data))
        return

    answer = data["choices"][0]["message"]["content"]
    await update.message.reply_text(answer)


def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # Диагностика для токена Telegram
    print("=== ПРОВЕРКА ТОКЕНА TELEGRAM ===")
    print("TELEGRAM_TOKEN =", TELEGRAM_TOKEN[:10] + "..." if TELEGRAM_TOKEN else "None")
    print("=================================")
    
    if not TELEGRAM_TOKEN:
        print("❌ ОШИБКА: TELEGRAM_TOKEN не найден!")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Бот запущен и готов к работе!")
    app.run_polling()


if __name__ == "__main__":
    main()

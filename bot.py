import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
# Это комментарий
# Он ничего не делает
# Его можно вставить куда угодно


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

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

    # Если DeepSeek вернул ошибку — не падаем
    if "choices" not in data:
        await update.message.reply_text("DeepSeek вернул ошибку:\n" + str(data))
        return

    answer = data["choices"][0]["message"]["content"]
    await update.message.reply_text(answer)


def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()


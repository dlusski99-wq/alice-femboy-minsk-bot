import os

print("=== ДИАГНОСТИКА ПЕРЕМЕННЫХ ===")
print(f"TELEGRAM_TOKEN: {os.getenv('TELEGRAM_TOKEN')}")
print(f"DEEPSEEK_API_KEY: {os.getenv('DEEPSEEK_API_KEY')}")

if os.getenv('TELEGRAM_TOKEN') and os.getenv('DEEPSEEK_API_KEY'):
    print("\n✅ Все переменные найдены!")
else:
    print("\n❌ Какие-то переменные не найдены")

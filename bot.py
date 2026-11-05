import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# Слова, за которые удаляем
BAD_WORDS = ["казино", "ставки", "1xbet", "крипта", "инвест", "заработок", "http", "t.me/"]

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    text = msg.text.lower()
    # Если это админ - не трогаем
    member = await context.bot.get_chat_member(update.effective_chat.id, msg.from_user.id)
    if member.status in ["administrator", "creator"]:
        return
    # Если есть плохое слово - удаляем
    if any(w in text for w in BAD_WORDS):
        try:
            await msg.delete()
        except:
            pass

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))
    print("Бот запущен")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

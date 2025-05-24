from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image
import io
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOB_PATH = "bob.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reply to an image with /bob and I’ll add Bob to it.")

async def add_bob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo = update.message.reply_to_message.photo[-1]
        file = await photo.get_file()
        image_bytes = io.BytesIO()
        await file.download_to_memory(out=image_bytes)
        image_bytes.seek(0)

        background = Image.open(image_bytes).convert("RGBA")
        overlay = Image.open(BOB_PATH).convert("RGBA")

        scale = background.height // 5
        overlay = overlay.resize((scale, scale))
        position = (10, background.height - overlay.height - 10)

        background.paste(overlay, position, overlay)

        result = io.BytesIO()
        result.name = "result.png"
        background.save(result, format="PNG")
        result.seek(0)

        await update.message.reply_photo(photo=result)
    else:
        await update.message.reply_text("Please reply to an image with /bob.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bob", add_bob))
    print("Bot running...")
    app.run_polling()

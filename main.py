from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image
import io
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOB_PATH = "bob.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start command")
    await update.message.reply_text("Reply to an image with /bob and I’ll add Bob to it.")

async def add_bob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Received /bob command")

        if update.message.reply_to_message and update.message.reply_to_message.photo:
            photo = update.message.reply_to_message.photo[-1]
            file = await photo.get_file()
            image_bytes = io.BytesIO()
            await file.download_to_memory(out=image_bytes)
            image_bytes.seek(0)

            background = Image.open(image_bytes).convert("RGBA")

            # Load and resize Bob
            overlay = Image.open(BOB_PATH).convert("RGBA")
            scale = background.height // 3  # Bigger size
            overlay = overlay.resize((scale, scale))

            # Position Bob fully in the bottom-left corner
            position = (0, background.height - overlay.height)

            # Paste Bob
            background.paste(overlay, position, overlay)

            # Save and send result
            result = io.BytesIO()
            result.name = "result.png"
            background.save(result, format="PNG")
            result.seek(0)

            await update.message.reply_photo(photo=result)
        else:
            await update.message.reply_text("Please reply to an image with /bob.")
    except Exception as e:
        print(f"Error in /bob: {e}")
        await update.message.reply_text(f"Something went wrong: {e}")

if __name__ == '__main__':
    print("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bob", add_bob))
    app.run_polling()

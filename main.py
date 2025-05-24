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

        # Check if the command is in reply to a photo
        if update.message.reply_to_message and update.message.reply_to_message.photo:
            photo = update.message.reply_to_message.photo[-1]
            file = await photo.get_file()
            image_bytes = io.BytesIO()
            await file.download_to_memory(out=image_bytes)
            image_bytes.seek(0)

            # Open background image
            background = Image.open(image_bytes).convert("RGBA")

            # Load Bob
            try:
                overlay = Image.open(BOB_PATH).convert("RGBA")
            except Exception as e:
                await update.message.reply_text(f"Error loading bob.png: {e}")
                print(f"Error loading bob.png: {e}")
                return

            # Resize Bob
            scale = background.height // 5
            overlay = overlay.resize((scale, scale))

            # Paste position: bottom-left
            position = (10, background.height - overlay.height - 10)
            background.paste(overlay, position, overlay)

            # Save result to memory
            result = io.BytesIO()
            result.name = "result.png"
            background.save(result, format="PNG")
            result.seek(0)

            # Send back the image
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

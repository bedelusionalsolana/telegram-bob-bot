from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import os
import io

BOB_PATH = "bob.png"  # Path to your overlay image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /bob as a reply to an image to add Bob in the corner!")

async def add_bob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if this command is a reply to a message with a photo
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        # Get the highest resolution photo
        photo = update.message.reply_to_message.photo[-1]
        photo_file = await photo.get_file()
        photo_bytes = io.BytesIO()
        await photo_file.download(out=photo_bytes)
        photo_bytes.seek(0)

        # Open the images
        background = Image.open(photo_bytes).convert("RGBA")
        overlay = Image.open(BOB_PATH).convert("RGBA")

        # Resize overlay if needed
        scale = background.height // 5
        overlay = overlay.resize((scale, scale))

        # Position: bottom left
        position = (10, background.height - overlay.height - 10)

        # Combine
        background.paste(overlay, position, overlay)

        # Save result to bytes
        output = io.BytesIO()
        output.name = "result.png"
        background.save(output, format="PNG")
        output.seek(0)

        # Send result
        await update.message.reply_photo(photo=output)
    else:
        await update.message.reply_text("Please reply to an image with /bob.")

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    TOKEN = "YOUR_BOT_TOKEN_HERE"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bob", add_bob))

    print("Bot is running...")
    app.run_polling()

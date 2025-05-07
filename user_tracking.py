import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
from utils.csv_handler import add_product, get_user_products, delete_user_product
from dotenv import load_dotenv

load_dotenv()

PRODUCT_URL, TARGET_PRICE = range(2)

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(self.token).build()

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(ConversationHandler(
            entry_points=[CommandHandler('track', self.start_tracking)],
            states={
                PRODUCT_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_product_url)],
                TARGET_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_target_price)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        ))
        self.application.add_handler(CommandHandler("list", self.show_list))
        self.application.add_handler(CommandHandler("remove", self.show_list))
        self.application.add_handler(CallbackQueryHandler(self.button_click))
        self.application.add_handler(CommandHandler("cancel", self.cancel))  # global cancel

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("➕ Track Product", callback_data="track")],
            [InlineKeyboardButton("📄 My List", callback_data="list")],
            [InlineKeyboardButton("❌ Remove Product", callback_data="remove")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 *Welcome to Amazon Price Tracker Bot!*\n\n"
            "Use the buttons below or send commands directly:\n"
            "• `/track` - Start tracking\n"
            "• `/list` - View tracked products\n"
            "• `/remove` - Remove a product\n"
            "• `/cancel` - Cancel current operation",
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

    async def start_tracking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("ℹ️ Please provide the product URL:")
        return PRODUCT_URL

    async def get_product_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['product_url'] = update.message.text
        await update.message.reply_text("ℹ️ Now, please provide your target price (in ₹):\n\nYou can /cancel anytime.")
        return TARGET_PRICE

    async def get_target_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            target_price = float(update.message.text)
            user_id = update.effective_user.id
            product_url = context.user_data['product_url']
            add_product(user_id, product_url, target_price)
            await update.message.reply_text(
                f"✅ Tracking started for:\n{product_url}\n\n"
                f"🎯 Target Price: ₹{target_price}"
            )
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("🚫 Invalid price. Please enter a valid number.")
            return TARGET_PRICE

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("❌ Tracking canceled.")
        return ConversationHandler.END

    def sanitize_text(self, text: str) -> str:
        return re.sub(r'([*_`\[\]()])', r'\\\1', text)

    async def show_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        df = get_user_products(user_id)

        if df.empty:
            await update.message.reply_text("ℹ️ You are not tracking any products yet.")
            return

        message = "📋 *Your tracked products:*\n\n"
        keyboard = []

        for _, row in df.iterrows():
            product_url = self.sanitize_text(row['product_url'])
            target_price = self.sanitize_text(str(row['target_price']))

            message += f"🔗 {product_url}\n🎯 Target: ₹{target_price}\n\n"
            keyboard.append([
                InlineKeyboardButton(
                    f"❌ Remove",
                    callback_data=f"remove|{row['product_url']}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == "track":
            await query.message.reply_text("ℹ️ To track a product, use `/track`")
        elif data == "list" or data == "remove":
            user_id = query.from_user.id
            df = get_user_products(user_id)

            if df.empty:
                await query.message.reply_text("ℹ️ You are not tracking any products yet.")
                return

            message = "📋 *Your tracked products:*\n\n"
            keyboard = []

            for _, row in df.iterrows():
                product_url = self.sanitize_text(row['product_url'])
                target_price = self.sanitize_text(str(row['target_price']))
                message += f"🔗 {product_url}\n🎯 Target: ₹{target_price}\n\n"
                keyboard.append([
                    InlineKeyboardButton(
                        f"❌ Remove",
                        callback_data=f"remove|{row['product_url']}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

        elif data.startswith("remove|"):
            product_url = data.split("|", 1)[1]
            user_id = query.from_user.id
            deleted = delete_user_product(user_id, product_url)
            if deleted:
                await query.message.reply_text(f"✅ Removed tracking for:\n{product_url}")
            else:
                await query.message.reply_text("ℹ️ Could not remove the product. Maybe it's already gone?")

            # Refresh list automatically
            await self.show_list(update, context)

    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    bot = BotHandler(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    bot.run()

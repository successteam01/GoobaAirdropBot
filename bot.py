import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logging.error("BOT_TOKEN environment variable not set!")
    exit(1)

def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message with task buttons"""
    user = update.effective_user
    logger.info(f"Start command from {user.id} ({user.username})")
    
    buttons = [
        [
            InlineKeyboardButton("Join Telegram", url="https://t.me/+XjGAPZD62hxhZDNh"),
            InlineKeyboardButton("Follow Twitter", url="https://x.com/RealGoobaCoin"),
        ],
        [InlineKeyboardButton("Follow TikTok", url="https://www.tiktok.com/@realgoobacoin")],
    ]
    
    update.message.reply_text(
        "🚀 Welcome to GoobaCoin Airdrop!\n\n"
        "✅ Complete these tasks:\n"
        "1. Join Telegram group\n"
        "2. Follow Twitter\n"
        "3. Follow TikTok\n"
        "4. Refer friends\n\n"
        "Click the buttons below:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    update.message.reply_text("📝 After completing tasks, send me your Twitter username:")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle all text messages"""
    user = update.effective_user
    text = update.message.text
    logger.info(f"Message from {user.id}: {text}")
    
    # Check if we already have Twitter username
    if "twitter" not in context.user_data:
        # Store Twitter username
        context.user_data["twitter"] = text
        update.message.reply_text("💳 Now send your SOL wallet address:")
    else:
        # Store wallet and send confirmation
        wallet = text
        twitter = context.user_data["twitter"]
        logger.info(f"Collected data: Twitter={twitter}, Wallet={wallet}")
        
        update.message.reply_text(
            "🎉 Weldone! Hope you didn't cheat the system?\n\n"
            "3 SOL will be scheduled to your wallet once:\n"
            "- Your referral count is top 10\n"
            "- The project moons\n\n"
            "⚠️ Note: Only top 10 will be rewarded after launch"
        )
        
        # Clear user data
        context.user_data.clear()

def main() -> None:
    """Start the bot in polling mode"""
    logger.info("Starting bot...")
    logger.info(f"Using token: {TOKEN[:10]}...{TOKEN[-6:]}")
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start polling
    logger.info("Bot started in polling mode")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

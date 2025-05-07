import os
from dotenv import load_dotenv
from user_tracking import BotHandler

# Load environment variables from .env file
load_dotenv()

def main():
    # Ensure the bot token is loaded from the environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return

    # Initialize and run the bot
    bot = BotHandler(token=bot_token)
    bot.run()

if __name__ == "__main__":
    main()

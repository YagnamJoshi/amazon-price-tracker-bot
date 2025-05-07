Amazon Price Tracker Bot 🛒
Overview
The Amazon Price Tracker Bot is a Telegram bot that allows users to track their favorite Amazon products and be notified when the prices drop below their target. With this bot, you can easily monitor prices, track multiple products, and remove products from your list when you're done.

The bot is designed to provide a simple and effective way to track product prices on Amazon without the need to constantly check the website manually. Just provide the product URL, set a target price, and let the bot do the rest!

Key Features:
Track Products: Start tracking a product by providing its Amazon URL and setting a target price.

View Tracked Products: Check your tracked product list at any time and see the target prices.

Remove Products: Easily remove a product from your tracked list if you're no longer interested.

Real-time Updates: The bot will send you updates when the price drops below your target.

Table of Contents
Installation

Usage

Bot Commands

Bot Features

How It Works

Environment Setup

Contributing

License

Made With Love

Thought of the Day

Installation
To run the Amazon Price Tracker Bot locally or on a server, follow the instructions below.

Prerequisites:
Python 3.7+ installed.

A Telegram Bot Token from BotFather.

pip to install Python packages.

Steps to Set Up:
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/amazon-price-tracker-bot.git
cd amazon-price-tracker-bot
Install the required dependencies:
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install required libraries:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory with the following contents:

env
Copy
Edit
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
Run the bot:
To start the bot, simply run the following:

bash
Copy
Edit
python main.py
Your bot will now be live and working. You can interact with it directly on Telegram!

Usage
Start the Bot:
Begin by clicking the /start button. You'll see a welcome message with buttons to interact with the bot.

Track a Product:
Click the Track Product button to begin tracking a product. You'll be asked to provide a product URL and set a target price. The bot will then monitor the price and notify you when the price drops below your set target.

List Tracked Products:
Use the My List button to view a list of all the products you're tracking. You can see the product URLs along with their target prices.

Remove a Product:
If you no longer wish to track a product, click the Remove Product button. You'll be able to remove individual products from your tracked list.

Bot Commands
/start: Initializes the bot and shows available options (Track Product, My List, Remove Product).

/track: Begins tracking a product. You'll be asked to provide the product's URL and a target price.

/list: Displays a list of all tracked products and their target prices.

/remove: Removes a specific product from the tracking list.

Bot Features
Track Products: Add any Amazon product by sharing its URL and setting a target price.

View Tracked Products: List all your tracked products, including the current price and target price.

Remove Products: Remove any tracked products that you no longer wish to monitor.

Real-Time Updates: Receive notifications when the price of a tracked product drops below your target price.

Simple and Intuitive Interface: Easy to use interface through Telegram.

How It Works
User Interaction:
When you first start the bot using /start, it shows a menu with options: "Track Product," "My List," and "Remove Product."

Track a Product:
To track a product, click Track Product, provide the URL of the Amazon product, and set a target price. The bot will then monitor that product.

List Tracked Products:
The My List button shows a list of all the products you're tracking along with their target prices.

Remove Products:
The Remove Product button allows you to delete products from your tracked list.

Price Monitoring:
The bot regularly checks the price of tracked products and sends you an alert when the price drops below your target.

Environment Setup
To configure and run the bot, you'll need the following environment variables:

TELEGRAM_BOT_TOKEN: Your unique Telegram Bot Token from BotFather.

Ensure these are added to your .env file before running the bot.

Contributing
We welcome contributions! If you'd like to contribute to the development of the Amazon Price Tracker Bot, follow these steps:

Fork the repository.

Clone your fork to your local machine.

Create a new branch (git checkout -b feature-branch).

Make your changes and commit them (git commit -m 'Add new feature').

Push the changes to your fork (git push origin feature-branch).

Open a Pull Request for review.

License
This project is open-source and available under the MIT License. See the LICENSE file for details.

Made With Love 💖
This bot was created with passion and care to help you track Amazon product prices and save money efficiently.

Thought of the Day
"A goal without a plan is just a wish." – Antoine de Saint-Exupéry

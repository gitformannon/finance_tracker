import os
import re
import logging
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv


# -------------------------------------------
# Parse the bank message
# -------------------------------------------

def parse_bank_message(message: str) -> dict:
    message = message.strip()
    lines = message.split('\n')
    data = {}

    patterns = {
        'amount': r"^(➖|➕) ([\d.,]+) UZS",
        'commission': r"^⚠️ Комиссия: ([\d.,]+) UZS",
        'epos': r"^📍 (.+)",
        'card_mask': r"^💳 (.+)",
        'date': r"^🕓 (\d{2}:\d{2} \d{2}\.\d{2}\.\d{4})",
        'balance': r"^💰 ([\d.,]+) UZS"
    }

    for line in lines:
        line = line.strip()
        for key, pattern in patterns.items():
            match = re.match(pattern, line)
            if match:
                if key == 'amount':
                    amount = float(match.group(2).replace(',', '').replace('.', '')) / 100
                    data['amount'] = amount
                elif key == 'commission':
                    commission = float(match.group(1).replace(',', '').replace('.', '')) / 100
                    data['commission'] = commission
                elif key == 'epos':
                    data['epos'] = match.group(1)
                elif key == 'card_mask':
                    card_match = re.search(r"\*(\d+)", match.group(1))
                    if card_match:
                        data['card_mask'] = f"*{card_match.group(1)}"
                elif key == 'date':
                    date_obj = datetime.strptime(match.group(1), "%H:%M %d.%m.%Y")
                    date_obj = date_obj.replace(tzinfo=ZoneInfo("Asia/Tashkent"))
                    data['date'] = date_obj.isoformat()
                elif key == 'balance':
                    balance = float(match.group(1).replace(',', '').replace('.', '')) / 100
                    data['balance'] = balance

    # Prepare for future lookup logic
    data['type_id'] = None
    data['card_id'] = None

    return data


# -------------------------------------------
# Send transaction to backend
# -------------------------------------------

def send_transaction_to_backend(data: dict):
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/transactions/")
    response = requests.post(backend_url, json=data)
    if response.status_code == 200:
        logging.info("Transaction successfully added to backend.")
    else:
        logging.error(f"Failed to add transaction: {response.text}")


# -------------------------------------------
# Handle Telegram messages
# -------------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        effective_message = update.effective_message
        if effective_message and effective_message.text:
            message_text = effective_message.text
            transaction_data = parse_bank_message(message_text)
            if transaction_data:
                send_transaction_to_backend(transaction_data)
                await effective_message.reply_text("✅ Transaction recorded successfully!")
            else:
                await effective_message.reply_text("❌ Could not parse the transaction message.")
        else:
            await effective_message.reply_text("Please send a valid text message.")
    except Exception as e:
        logging.error(f"Error in handle_message: {e}", exc_info=True)
        await update.effective_message.reply_text("An error occurred while processing your message.")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling update: {context.error}", exc_info=True)
    if update and update.effective_message:
        await update.effective_message.reply_text("An unexpected error occurred. Please try again later.")


# -------------------------------------------
# Main telegram_bot setup
# -------------------------------------------

load_dotenv()
application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_error_handler(error_handler)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path="webhook",
        webhook_url=os.getenv("WEBHOOK_URL")
    )


# -------------------------------------------
# Start the telegram_bot
# -------------------------------------------

if __name__ == "__main__":
    main()
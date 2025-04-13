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
        'amount': r"^(➖|➕)\s*([\d.,]+)\s*UZS",
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
                        data['card_number'] = f"*{card_match.group(1)}"
                elif key == 'date':
                    date_obj = datetime.strptime(match.group(1), "%H:%M %d.%m.%Y")
                    date_obj = date_obj.replace(tzinfo=ZoneInfo("Asia/Tashkent"))
                    data['date'] = date_obj.isoformat()
                elif key == 'balance':
                    balance = float(match.group(1).replace(',', '').replace('.', '')) / 100
                    data['balance'] = balance

    # Assign type_label if the first line matches specific emoji
    if lines and lines[0].startswith("💸"):
        data['type_label'] = lines[0].strip()

    logging.info(f"🧩 Parsed fields: {data}")

    return data


# -------------------------------------------
# Send transaction to backend
# -------------------------------------------

def send_transaction_to_backend(data: dict):
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/backend/v1/fintracker/transactions/")
    logging.info(f"📡 Sending data to backend at {backend_url}")
    logging.info(f"📦 Payload: {data}")

    payload = {
        "amount": data.get("amount"),
        "epos": data.get("epos"),
        "balance": data.get("balance"),
        "date": data.get("date"),
        "card_number": data.get("card_number"),
        "type_label": data.get("type_label")
    }

    try:
        response = requests.post(backend_url, json=payload)
        logging.info(f"📬 Response status: {response.status_code}")
        logging.info(f"📄 Response body: {response.text}")

        if response.status_code == 200:
            logging.info("✅ Transaction successfully added to backend.")
        else:
            logging.error(f"❌ Failed to add transaction. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.exception(f"💥 Exception occurred while sending to backend: {e}")


# -------------------------------------------
# Handle Telegram messages
# -------------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"📩 Incoming update: {update.to_dict()}")
    try:
        effective_message = update.effective_message
        if effective_message and effective_message.text:
            message_text = effective_message.text
            transaction_data = parse_bank_message(message_text)
            await effective_message.reply_text(f"📩 Received your message: {message_text}")
            logging.info(f"Parsed transaction: {transaction_data}")

            if transaction_data and all(key in transaction_data for key in ['amount', 'epos']):
                try:
                    send_transaction_to_backend(transaction_data)
                    await effective_message.reply_text("✅ Transaction recorded successfully!")
                except Exception as e:
                    logging.error(f"Backend error: {e}")
                    await effective_message.reply_text("❌ Failed to record transaction in backend.")
            else:
                await effective_message.reply_text("❌ Could not parse the transaction message.")
        else:
            await effective_message.reply_text("⚠️ Please send a valid text message.")
    except Exception as e:
        logging.error(f"Error in handle_message: {e}", exc_info=True)
        if update and update.effective_message:
            await update.effective_message.reply_text("🚨 An unexpected error occurred.")


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
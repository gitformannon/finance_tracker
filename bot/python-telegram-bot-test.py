from logging import basicConfig, INFO

import datetime as dtm
import zoneinfo

from telegram.constants import ParseMode
from telegram.ext import MessageHandler, filters, Defaults, Application

basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO
)


async def job(context):
    chat_id = context.job.chat_id
    timezone = context.bot.defaults.tzinfo
    local_now = dtm.datetime.now(timezone)
    utc_now = dtm.datetime.now(dtm.UTC)
    text = f'Running job at {local_now} in timezone {timezone}, which equals {utc_now} UTC.'
    await context.bot.send_message(chat_id=chat_id, text=text)


async def echo(update, context):
    text = update.message.text
    # Send with default parse mode
    await update.message.reply_text(f'<b>{text}</b>')
    # Override default parse mode locally
    await update.message.reply_text(f'*{text}*', parse_mode=ParseMode.MARKDOWN)
    # Send with no parse mode
    await update.message.reply_text(f'*{text}*', parse_mode=None)

    # Schedule job
    context.job_queue.run_once(
        job, dtm.datetime.now() + dtm.timedelta(seconds=1), chat_id=update.effective_chat.id
    )


def main():
    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=zoneinfo.ZoneInfo('Europe/Berlin'))

    application = (
        Application.builder()
        .token("7417801037:AAEIIZnAyVyCgRZ95DofWiJ164kEPH8S7Lg")
        .defaults(defaults)
        .build()
    )

    # on non command text message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
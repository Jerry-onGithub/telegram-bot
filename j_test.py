# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:45:22 2022

@author: Jerry
"""

import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = ''

PORT = int(os.environ.get('PORT', '8443'))
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

ONE, TWO, THREE, FOUR, FIVE = range(5)

def main_handler(update, context):
   #print(update.message.text)
   
    if(words(update.message.text) == True):
        time.sleep(3)
        context.bot.deleteMessage(update.message.chat.id, update.message.message_id)
        update.message.reply_text("@" + update.message.from_user.first_name +", Long messages not allowed. Your message has been removed.")

    else:
        update.message.reply_text(update.message.text)
        
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    #return ONE


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def words(words):
    count = 0
    for phrase in words.split():
        if phrase.isalpha():
            count +=1
        else:
            count = 0
        if count >= 3:
            return True
    return False

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, main_handler))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook('https://j-test-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()
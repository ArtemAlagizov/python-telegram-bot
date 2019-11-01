#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import os
import platform
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram import ParseMode
from io import BytesIO
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Stages
ANSWER, START, NEXT, FINISH = range(4)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN = range(7)



def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_qestionary(update, context):
    """Send message on `/start`."""
    question = 1
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with picture and appended InlineKeyboard
    update.message.reply_photo(photo=open('archetype-test/' + str(question) + '.png', 'rb'), reply_markup=reply_markup)
    # Tell CosversationHandler that we're in State `FIRST` now
    return ANSWER


def next(update, context):
    # Get CallbackQuery from Update
    # Get Bot from CallbackContext
    print("@@@@@@@@@    Entered in NEXT     @@@@@@@")
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id
    question = 20
    print("@@###@#@#@#@#@     Question is   " + str(question) + "       ")
    context.bot.send_photo(chat_id=chat_id, photo=open('archetype-test/' + str(question) + '.png', 'rb'), reply_markup=reply_markup)
    print("@@@@@@@@@    PHOTO UPDATED HAHA     @@@@@@@")
    # update.message.reply_photo(photo=open('archetype-test/' + str(question) + '.png', 'rb'), reply_markup=reply_markup)
    return ANSWER


def one(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write("3;;;;;;;\r\n")
    f.close()
    print("@@@@@@@@@    writen     @@@@@@@")
    next(update, context)

    return ANSWER


def two(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 2 ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";2;;;;;;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    return ANSWER


def three(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 1 ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";;1;;;;;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return ANSWER


def four(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 0 ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";;;0;;;;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    return ANSWER


def five(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 1 ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";;;;1;;;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    return ANSWER


def six(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 2 ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";;;;;2;;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    return ANSWER


def seven(update, context):
    """Show new choice of buttons"""
    keyboard = [
        [InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton("   ", callback_data=str()),
         InlineKeyboardButton(" 3 ", callback_data=str())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    chat_id = query.message.chat_id

    f = open("archetype-test-answers/" + str(chat_id) + "-answers"".txt", "a+")
    f.write(";;;;;;3;\r\n")
    f.close()

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text="Записано",
        reply_markup=reply_markup
    )
    return ANSWER


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Вы прошли опросник. Спасибо! Ваши ответы записаны и будут проанализированы."
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def gettoken(source):
    with open(source, 'r') as file:
        token = file.read().replace('\n', '')
    return token


def file_len(fname):
    with open(fname) as f:
        for i in enumerate(f):
            pass
    return i + 1


def main():
    # Create the Updater and pass it your bot's token.

    updater = Updater(gettoken("tokens/getmethroughbot-token"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the `pattern parameter to pass CallbackQueryies with specific
    # data pattern to the corresponding ha`ndlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_qestionary)],
        states={
            ANSWER: [CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                     CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                     CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                     CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
                     CallbackQueryHandler(five, pattern='^' + str(FIVE) + '$'),
                     CallbackQueryHandler(six, pattern='^' + str(SIX) + '$'),
                     CallbackQueryHandler(seven, pattern='^' + str(SEVEN) + '$')],
            NEXT: [CallbackQueryHandler(next, pattern='^' + str() + '$')],
            FINISH: [CallbackQueryHandler(end, pattern='^' + str() + '$')]
        },
        fallbacks=[CommandHandler('start', start_qestionary)]
    )

    # Add conversationhandler to dispatcher it will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

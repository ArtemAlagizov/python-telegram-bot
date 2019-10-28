#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from datetime import datetime, date, time
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

intro_choice_1 = u'Изучить новую теорию'
intro_choice_2 = u'Сформулировать конкретные шаги в развитии карьеры'
intro_choice_3 = u'Понять как работает система'
intro_choice_4 = u'Лучше узнать себя'

intro_reply_1 = u'Отлично! За эти 10 дней ты познакомишься с 4х-частной моделью описания корпоративных культур и ' \
                u'профессий. С ее помощью ты сможешь сформулировать стратегию следующих шагов в своей карьере '
intro_reply_2 = u'Супер! За эти 10 дней ты получишь понятный и работающий инструмент для развития в карьере. Ты ' \
                u'поймешь, в чем твои сильные стороны и где сможешь добиться максимальных результатов! '
intro_reply_3 = u'Прекрасно! За эти 10 дней ты узнаешь на примере 4частной модели, какие бывают корпоративные ' \
                u'культуры и виды профессий, и как это сочетание влияет на развитие твоей карьеры '
intro_reply_4 = u'Замечательно! За эти 10 дней ты лучше узнаешь, какие компании и корпоративные культуры тебе ' \
                u'подходят, а какие противопоказаны; в чем область твоих талантов, и как ты можешь их применить! '

intro_questionary_reply_keyboard = [[intro_choice_1, intro_choice_2],
                                    [intro_choice_3, intro_choice_4]]

intro_markup = ReplyKeyboardMarkup(intro_questionary_reply_keyboard, one_time_keyboard=True)
intro_end_markup = ReplyKeyboardMarkup([], one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def intro_choice_1_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_1, reply_markup=intro_end_markup)
    return ConversationHandler.END


def intro_choice_2_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_2, reply_markup=intro_end_markup)
    return ConversationHandler.END


def intro_choice_3_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_3, reply_markup=intro_end_markup)
    return ConversationHandler.END


def intro_choice_4_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_4, reply_markup=intro_end_markup)
    return ConversationHandler.END


def start(update, context):
    reply_text = "Привет, рада тебя приветствовать на нашем марафоне! "
    if context.user_data:
        reply_text += " You already told me your {}. Why don't you tell me something more " \
                      "about yourself? Or change enything I " \
                      "already know.".format(", ".join(context.user_data.keys()))
    else:
        reply_text += " Расскажи, что тебя интересует в первую очередь"
    update.message.reply_text(reply_text, reply_markup=intro_markup)

    add_jobs(update, context)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text.lower()
    context.user_data['choice'] = text
    if context.user_data.get(text):
        reply_text = 'Your {}, I already know the following ' \
                     'about that: {}'.format(text, context.user_data[text])
    else:
        reply_text = 'Your {}? Yes, I would love to hear about that!'.format(text)
    update.message.reply_text(reply_text)

    return TYPING_REPLY


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(update, context):
    text = update.message.text
    category = context.user_data['choice']
    context.user_data[category] = text.lower()
    del context.user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on "
                              "something.".format(facts_to_str(context.user_data)),
                              reply_markup=markup)

    return CHOOSING


def show_data(update, context):
    update.message.reply_text("This is what you already told me:"
                              "{}".format(facts_to_str(context.user_data)))


def done(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(context.user_data)))
    return ConversationHandler.END


def execute_job(context):
    job = context.job
    context.bot.send_message(job.context, text='job done!')


def add_jobs(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        d = date(2019, 10, 28)
        t = time(20, 57)
        due = datetime.combine(d, t)

        # Add job to queue and stop current one if there is a timer already
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(execute_job, due, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text('Job is set in the queue...')

    except (IndexError, ValueError):
        update.message.reply_text('something gone wrong')


def remove_job(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def gettoken(source):
    with open(source, 'r') as file:
        token = file.read().replace('\n', '')
    return token


def get_chat_id(update, context):
    chat_id = update.message.chat_id
    return chat_id


def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='conversationbot')
    updater = Updater(gettoken("tokens/getmethroughbot-token"), persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice),
                       MessageHandler(Filters.regex(intro_choice_1),
                                      intro_choice_1_callback),
                       MessageHandler(Filters.regex(intro_choice_2),
                                      intro_choice_2_callback),
                       MessageHandler(Filters.regex(intro_choice_3),
                                      intro_choice_3_callback),
                       MessageHandler(Filters.regex(intro_choice_4),
                                      intro_choice_4_callback),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="my_conversation",
        persistent=True
    )

    dp.add_handler(conv_handler)

    show_data_handler = CommandHandler('show_data', show_data)
    dp.add_handler(show_data_handler)
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

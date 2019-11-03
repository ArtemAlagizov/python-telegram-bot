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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence, CallbackQueryHandler)

import logging
import abc

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

START_CHOOSING, DEFAULT_CHOOSING, TYPING_REPLY, TYPING_CHOICE, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN = range(11)


intro_choice_1 = u'Изучить новую теорию'
intro_choice_2 = u'Сформулировать конкретные шаги в развитии карьеры'
intro_choice_3 = u'Понять как работает система'
intro_choice_4 = u'Лучше узнать себя'

intro_reply_button_1 = u'Отлично! За эти 10 дней ты познакомишься с 4х-частной моделью описания корпоративных культур и ' \
                u'профессий. С ее помощью ты сможешь сформулировать стратегию следующих шагов в своей карьере '
intro_reply_button_2 = u'Супер! За эти 10 дней ты получишь понятный и работающий инструмент для развития в карьере. Ты ' \
                u'поймешь, в чем твои сильные стороны и где сможешь добиться максимальных результатов! '
intro_reply_button_3 = u'Прекрасно! За эти 10 дней ты узнаешь на примере 4частной модели, какие бывают корпоративные ' \
                u'культуры и виды профессий, и как это сочетание влияет на развитие твоей карьеры '
intro_reply_button_4 = u'Замечательно! За эти 10 дней ты лучше узнаешь, какие компании и корпоративные культуры тебе ' \
                u'подходят, а какие противопоказаны; в чем область твоих талантов, и как ты можешь их применить! '

default_reply_button_1 = u'Пройти тест'
default_reply_button_2 = u'xxx'
default_reply_button_3 = u'Help FAQ'
default_reply_button_4 = u'Задать вопрос автору'

broadcast_1_reply = u'Начинается подкаст 1 ({}), не пропусти!'
broadcast_2_reply = u'Начинается подкаст 2 ({}), не пропусти!'
broadcast_3_reply = u'Начинается подкаст 3 ({}), не пропусти!'
broadcast_4_reply = u'Начинается подкаст 4 ({}), не пропусти!'
broadcast_5_reply = u'Начинается подкаст 5 ({}), не пропусти!'

intro_questionary_reply_keyboard = [[intro_choice_1, intro_choice_2],
                                    [intro_choice_3, intro_choice_4]]
default_facilitator_keyboard = [[default_reply_button_1, default_reply_button_2],
                                [default_reply_button_3, default_reply_button_4]]

intro_markup = ReplyKeyboardMarkup(intro_questionary_reply_keyboard, one_time_keyboard=True)
default_markup = ReplyKeyboardMarkup(default_facilitator_keyboard, one_time_keyboard=True)

# job_due_1 = datetime.combine(date(2019, 11, 7), time(11, 00))
# job_due_2 = datetime.combine(date(2019, 11, 7), time(19, 00))
# job_due_3 = datetime.combine(date(2019, 11, 7), time(20, 00))
# job_due_4 = datetime.combine(date(2019, 11, 8), time(13, 00))
# job_due_5 = datetime.combine(date(2019, 11, 8), time(19, 00))
# job_due_6 = datetime.combine(date(2019, 11, 9), time(11, 00))
# job_due_7 = datetime.combine(date(2019, 11, 10), time(11, 00))
# job_due_8 = datetime.combine(date(2019, 11, 10), time(18, 00))
# job_due_9 = datetime.combine(date(2019, 11, 10), time(19, 00))
# job_due_10 = datetime.combine(date(2019, 11, 12), time(19, 00))
# job_due_11 = datetime.combine(date(2019, 11, 13), time(11, 00))
# job_due_12 = datetime.combine(date(2019, 11, 13), time(19, 00))
# job_due_13 = datetime.combine(date(2019, 11, 14), time(19, 00))
# job_due_14 = datetime.combine(date(2019, 11, 15), time(11, 00))
# job_due_15 = datetime.combine(date(2019, 11, 15), time(15, 00))
# job_due_16 = datetime.combine(date(2019, 11, 15), time(19, 00))
# job_due_17 = datetime.combine(date(2019, 11, 16), time(11, 00))
# job_due_18 = datetime.combine(date(2019, 11, 16), time(13, 00))
# job_due_19 = datetime.combine(date(2019, 11, 16), time(19, 00))
# job_due_20 = datetime.combine(date(2019, 11, 17), time(13, 00))
# job_due_21 = datetime.combine(date(2019, 11, 17), time(19, 00))

job_due_base_1 = 20
job_due_base_2 = 00

job_due_1 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2))
job_due_2 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2))
job_due_3 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2))
job_due_4 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2))
job_due_5 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 2))
job_due_6 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 3))
job_due_7 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 4))
job_due_8 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 5))
job_due_9 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 6))
job_due_10 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 7))
job_due_11 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 8))
job_due_12 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 9))
job_due_13 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 10))
job_due_14 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 11))
job_due_15 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 12))
job_due_16 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 13))
job_due_17 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 14))
job_due_18 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 15))
job_due_19 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 16))
job_due_20 = datetime.combine(date(2019, 11, 2), time(job_due_base_1, job_due_base_2 + 17))


def intro_choice_1_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_1, reply_markup=default_markup)
    start_user_profile(update, context)
    return DEFAULT_CHOOSING


def intro_choice_2_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_2, reply_markup=default_markup)
    start_user_profile(update, context)
    return DEFAULT_CHOOSING


def intro_choice_3_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_3, reply_markup=default_markup)
    start_user_profile(update, context)
    return DEFAULT_CHOOSING


def intro_choice_4_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_4, reply_markup=default_markup)
    start_user_profile(update, context)
    return DEFAULT_CHOOSING


def broadcast_1(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(broadcast_1_reply, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def broadcast_2(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(broadcast_2_reply, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def broadcast_3(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(broadcast_3_reply, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def broadcast_4(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(broadcast_4_reply, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def broadcast_5(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(broadcast_5_reply, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def execute_job_1(context):
    job = context.job
    context.bot.send_message(job.context, text='job 1 done!')


def execute_job_2(context):
    job = context.job
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    question = 1
    context.bot.sendPhoto(job.context,
                          photo=open('archetype-test/' + str(question) + '.png', 'rb'),
                          caption='job 2 done',
                          reply_markup=inline_reply_markup)


def execute_job_3(context):
    job = context.job
    context.bot.sendPoll(
        job.context,
        question="В каком типе компании вы бы сейчас хотели работать?",
        options=['Культура достижений', 'Культура отношений', 'Культура знаний', 'Культура правил']
        , reply_markup=None
    )


def execute_job_4(context):
    job = context.job
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
    context.bot.sendMessage(job.context, text='[Job 4 is done](https://t.me/) *Всем привет, Это карточка опросника*\n'
                                              '[Fuck me](https://t.me/) _ë-мобиль ХYú комментарий_ \n'
                                              '`На сколько утверждение относится к  `'
                                              '`тебе / свойственно тебе?            `\n\n'
                                              '`  23                                `\n'
                                              '` ___________________________ `\n'
                                              '`|             |             |`\n'
                                              '`|    Перед    | Я принимаю  |`\n'
                                              '`|  принятием  |   решение   |`\n'
                                              '`|  решения я  | достаточно  |`\n'
                                              '`|  тщательно  |   быстро    |`\n'
                                              '`| продумываю  |             |`\n'
                                              '`|             |             |`\n'
                                              '`|_____________|_____________|`\n'
                                              '`                                    `\n\n',
                            parse_mode='Markdown', reply_markup=reply_markup)


def execute_job_5(context):
    job = context.job


def execute_job_6(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 6 done!')


def execute_job_7(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 7 done!')


def execute_job_8(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 8 done!')


def execute_job_9(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 9 done!')


def execute_job_10(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 10 done!')


def execute_job_11(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 11 done!')


def execute_job_12(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 12 done!')


def execute_job_13(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 13 done!')


def execute_job_14(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 14 done!')


def execute_job_15(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 15 done!')


def execute_job_16(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 16 done!')


def execute_job_17(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 17 done!')


def execute_job_18(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 18 done!')


def execute_job_19(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 19 done!')


def execute_job_20(context):
    job = context.job
    #context.bot.send_message(job.context, text='job 20 done!')


def add_user_jobs(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds

        new_job_1 = context.job_queue.run_once(execute_job_1, job_due_1, context=chat_id)
        context.chat_data['job'] = new_job_1

        new_job_2 = context.job_queue.run_once(execute_job_2, job_due_2, context=chat_id)
        context.chat_data['job'] = new_job_2

        new_job_3 = context.job_queue.run_once(execute_job_3, job_due_3, context=chat_id)
        context.chat_data['job'] = new_job_3

        new_job_4 = context.job_queue.run_once(execute_job_4, job_due_4, context=chat_id)
        context.chat_data['job'] = new_job_4

        new_job_5 = context.job_queue.run_once(execute_job_5, job_due_5, context=chat_id)
        context.chat_data['job'] = new_job_5

        new_job_6 = context.job_queue.run_once(execute_job_6, job_due_6, context=chat_id)
        context.chat_data['job'] = new_job_6

        new_job_7 = context.job_queue.run_once(execute_job_7, job_due_7, context=chat_id)
        context.chat_data['job'] = new_job_7

        new_job_8 = context.job_queue.run_once(execute_job_8, job_due_8, context=chat_id)
        context.chat_data['job'] = new_job_8

        new_job_9 = context.job_queue.run_once(execute_job_9, job_due_9, context=chat_id)
        context.chat_data['job'] = new_job_9

        new_job_10 = context.job_queue.run_once(execute_job_10, job_due_10, context=chat_id)
        context.chat_data['job'] = new_job_10

        new_job_11 = context.job_queue.run_once(execute_job_11, job_due_11, context=chat_id)
        context.chat_data['job'] = new_job_11

        new_job_12 = context.job_queue.run_once(execute_job_12, job_due_12, context=chat_id)
        context.chat_data['job'] = new_job_12

        new_job_13 = context.job_queue.run_once(execute_job_13, job_due_13, context=chat_id)
        context.chat_data['job'] = new_job_13

        new_job_14 = context.job_queue.run_once(execute_job_14, job_due_14, context=chat_id)
        context.chat_data['job'] = new_job_14

        new_job_15 = context.job_queue.run_once(execute_job_15, job_due_15, context=chat_id)
        context.chat_data['job'] = new_job_15

        new_job_16 = context.job_queue.run_once(execute_job_16, job_due_16, context=chat_id)
        context.chat_data['job'] = new_job_16

        new_job_17 = context.job_queue.run_once(execute_job_17, job_due_17, context=chat_id)
        context.chat_data['job'] = new_job_17

        new_job_18 = context.job_queue.run_once(execute_job_18, job_due_18, context=chat_id)
        context.chat_data['job'] = new_job_18

        new_job_19 = context.job_queue.run_once(execute_job_19, job_due_19, context=chat_id)
        context.chat_data['job'] = new_job_19

        new_job_20 = context.job_queue.run_once(execute_job_20, job_due_20, context=chat_id)
        context.chat_data['job'] = new_job_20

        update.message.reply_text('attempt: jobs to be sent in the queue...')

    except (IndexError, ValueError):
        update.message.reply_text('attempt:  something gone wrong while setting jobs On')


def remove_job(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active jobs yet')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('job removed')


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    reply_text = "Привет, рада тебя приветствовать на нашем марафоне! "
    if context.user_data:
        reply_text += " You already told me your {}. Why don't you tell me something more " \
                      "about yourself? Or change enything I " \
                      "already know.".format(", ".join(context.user_data.keys()))
    else:
        reply_text += " Расскажи, что тебя интересует в первую очередь"
    update.message.reply_text(reply_text, reply_markup=intro_markup)

    return START_CHOOSING


def default_choice(update, context):
    text = update.message.text.lower()
    context.user_data['choice'] = text
    if context.user_data.get(text):
        reply_text = 'Your {}, I already know the following ' \
                     'about that: {}'.format(text, context.user_data[text])
    else:
        reply_text = 'Your {}? Yes, I would love to hear about that!'.format(text)
    update.message.reply_text(reply_text)

    return TYPING_REPLY


def start_user_profile(update, context):
    add_user_jobs(update, context)


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
                              reply_markup=default_markup)

    return DEFAULT_CHOOSING


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




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def gettoken(source):
    with open(source, 'r') as file:
        token = file.read().replace('\n', '')
    return token
default_facilitator_keyboard = [[u'Пройти тест', u''],
                                [u'Help FAQ', u'Вопрос автору']]

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='conversationbot_persistence_log')
    updater = Updater(gettoken("tokens/getmethroughbot-token"), persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            DEFAULT_CHOOSING: [MessageHandler(Filters.regex(default_reply_button_1),
                                      default_choice),
                       MessageHandler(Filters.regex(default_reply_button_2),
                                      default_choice),
                       MessageHandler(Filters.regex(default_reply_button_3),
                                      default_choice),
                       MessageHandler(Filters.regex(default_reply_button_4),
                                      default_choice),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice),
                       ],
            START_CHOOSING: [MessageHandler(Filters.regex(intro_choice_1),
                                              intro_choice_1_callback),
                               MessageHandler(Filters.regex(intro_choice_2),
                                              intro_choice_2_callback),
                               MessageHandler(Filters.regex(intro_choice_3),
                                              intro_choice_3_callback),
                               MessageHandler(Filters.regex(intro_choice_4),
                                              intro_choice_4_callback),
                               ],
            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           default_choice),
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
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
from datetime import datetime, date, time
from telegram import ReplyKeyboardMarkup
from uuid import uuid4
import pickle
import os.path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence, CallbackQueryHandler)
import logging, telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Callback data
START_CHOOSING, DEFAULT_CHOOSING, TYPING_REPLY, TYPING_CHOICE, PATH_ONE, PATH_TWO, ONE, TWO, THREE, FOUR, FIVE, SIX, \
SEVEN, HW_YES, HW_NO, HW_A, HW_B, HW_C, HW_D, QUESTIONARY, REMINDER_LOOP_LEVEL, AUTHOR, EMPTY, GOTO_GROUP = range(24)

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

job_due_base_1 = 14
job_due_base_2 = 00

ob_due_base_3 = 11
job_due_base_4 = 7
job_due_base_5 = 2019

job_due_1 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_2 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2
                                                                                       + 2))
job_due_3 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2
                                                                                       + 1))
job_due_4 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2
                                                                                       + 3))
job_due_5 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_6 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_7 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_8 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_9 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_10 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_11 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_12 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_13 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_14 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_15 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_16 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_17 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_18 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_19 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
job_due_20 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))

intro_choice_1 = u'Изучить новую теорию'
intro_choice_2 = u'Сформулировать конкретные шаги в развитии карьеры'
intro_choice_3 = u'Понять как работает система'
intro_choice_4 = u'Лучше узнать себя'

intro_reply_button_1 = u'Отлично! За эти 10 дней ты познакомишься с 4х-частной моделью описания корпоративных культур' \
                       u' и профессий. С ее помощью ты сможешь сформулировать стратегию следующих шагов в своей карьере'
intro_reply_button_2 = u'Супер! За эти 10 дней ты получишь понятный и работающий инструмент для развития в карьере. ' \
                       u'Ты поймешь, в чем твои сильные стороны и где сможешь добиться максимальных результатов! '
intro_reply_button_3 = u'Прекрасно! За эти 10 дней ты узнаешь на примере 4частной модели, какие бывают корпоративные ' \
                       u'культуры и виды профессий, и как это сочетание влияет на развитие твоей карьеры '
intro_reply_button_4 = u'Замечательно! За эти 10 дней ты лучше узнаешь, какие компании и корпоративные культуры тебе ' \
                       u'подходят, а какие противопоказаны; в чем область твоих талантов, и как ты можешь их применить!'

default_reply_button_1 = 'Diagnostics'
default_reply_button_2 = 'Materials'
default_reply_button_3 = 'FAQ'
default_reply_button_4 = 'Ask author'  # вопрос автору

intro_questionary_reply_keyboard = [[intro_choice_1, intro_choice_2],
                                    [intro_choice_3, intro_choice_4]]
default_facilitator_keyboard = [[default_reply_button_1, default_reply_button_2],
                                [default_reply_button_3, default_reply_button_4]]

intro_markup = ReplyKeyboardMarkup(intro_questionary_reply_keyboard, one_time_keyboard=True)
default_markup = ReplyKeyboardMarkup(default_facilitator_keyboard, one_time_keyboard=True)


def empty(context):
    aaa = 1


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def intro_choice_1_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_1, reply_markup=default_markup)
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_2_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_2, reply_markup=default_markup)
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_3_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_3, reply_markup=default_markup)
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_4_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_4, reply_markup=default_markup)
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def start_questionary(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    selected = query.data
    stage_data = selected.split(",")
    append_answers_database(chat_id, stage_data[1], stage_data[0])
    question = int(stage_data[1]) + 1
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE) + "," + str(question)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX) + "," + str(question)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN) + "," + str(question))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendPhoto(chat_id,
                  photo=open('archetype-test/' + str(question) + '.png', 'rb'),
                  caption='Выберите, в какой степени это свойственно вам...',
                  reply_markup=inline_reply_markup
                  )
    return QUESTIONARY


def next_questionare(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    selected = query.data
    stage_data = selected.split(",")
    append_answers_database(chat_id, stage_data[1], stage_data[0])
    question = int(stage_data[1]) + 1
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE) + "," + str(question)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX) + "," + str(question)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN) + "," + str(question))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    if question == 31:
        questionary_finish_flag_database(chat_id)
        bot.send_message(
            chat_id=chat_id,
            text="Тест завершен. Результаты будут получены после окончания марафона.",
            reply_markup=None
        )
        return DEFAULT_CHOOSING
    else:
        bot.sendPhoto(chat_id,
                      photo=open('archetype-test/' + str(question) + '.png', 'rb'),
                      caption='Выберите, в какой степени это свойственно вам...',
                      reply_markup=inline_reply_markup
                      )
        return QUESTIONARY


def default_choice_questionary(update, context):
    text = update.message.text.lower()
    context.user_data['choice'] = text
    reply_text = 'Сначала завершите заполнение анкеты'
    update.message.reply_text(reply_text)

    return QUESTIONARY


def questionary_finish_flag_database(chat_id):
    os.rename(r'database/questionary/questionary_' + str(chat_id), r'database/questionary/questionary_' + str(chat_id)
              + '_finished')


def append_answers_database(chat_id, question, choice):
    f = open('database/questionary/questionary_' + str(chat_id), "a")
    f.write("Question: " + str(question) + " choice: " + str(choice) + "\n")
    f.close()


def homework_dialog_2_yes(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_a = u'Помни о будущем, соблюдай правила'
    text_reply_b = u'Главное, чтобы нам было хорошо вместе'
    text_reply_c = u'Истина в познании'
    text_reply_d = u'Побеждает сильнейший'
    text_reply_yes = u'Отлично! Если хочешь посмотреть еще раз материалы, они тут [ссыль]\n' \
                     u'Напоминаю, что есть домашнее задание по архетипу Воина [ссыль]\n'
    text_reply_quest = u'Как думаешь, какая фраза характеризует человека с архетипом Воина? (один из вариантов ' \
                       u'правильный) '
    keyboard_second_stage = [
        [InlineKeyboardButton(text_reply_a, callback_data=str(HW_A))],
        [InlineKeyboardButton(text_reply_b, callback_data=str(HW_B))],
        [InlineKeyboardButton(text_reply_c, callback_data=str(HW_C))],
        [InlineKeyboardButton(text_reply_d, callback_data=str(HW_D))]
    ]
    reply_markup_2 = InlineKeyboardMarkup(keyboard_second_stage)
    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_yes,
        reply_markup=None
    )

    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_quest,
        reply_markup=reply_markup_2
    )

    return REMINDER_LOOP_LEVEL


def homework_dialog_2_no(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_no = u'А зря! Там я рассказываю про первый архетип, культуре которого соответствуют такие компании' \
                    u'как McKinsey, PwC, Северсталь и другие. Ссылка'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Обязательно посмотри позже!",
        reply_markup=default_markup
    )
    set_reminder(update, context)

    return DEFAULT_CHOOSING


def homework_dialog_3_correct(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_yes = u'Супер! Все правильно :)'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_yes,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="До следующего урока.. :)",
        reply_markup=default_markup
    )

    return DEFAULT_CHOOSING


def homework_dialog_3_incorrect(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_no = u'Не совсем верно... другая фраза лучше описывает человека с архетипом Воина'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Если будет время, послушай этот отрывок [ссыль] До следующего урока.. :)",
        reply_markup=default_markup
    )
    return DEFAULT_CHOOSING


def set_reminder(update, context):
    query = update.callback_query
    print("Reminder set")
    context.job_queue.run_once(job_2_reminder, job_due_2, context=query.message.chat_id)


def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    chat_id = user.id
    logger.info("User %s started the conversation.", user.first_name)

    reply_text = u'Привет, ID' + str(chat_id) + u', рада тебя приветствовать на нашем марафоне! '
    if context.user_data:
        reply_text += u'Мы уже знакомы {}. Продолжим?'.format(', '.join(context.user_data.keys()))
    else:
        reply_text += u' Расскажи, что тебя интересует в первую очередь'
    update.message.reply_text(reply_text, reply_markup=intro_markup)
    return START_CHOOSING


def start_user_queue(update, context):
    chat_id = update.message.chat_id
    print("  Job: " + str(1))
    context.job_queue.run_once(job_1, job_due_1, context=chat_id)
    print("  Job: " + str(3))
    context.job_queue.run_once(job_3, job_due_3, context=chat_id)
    print("  Job: " + str(4))
    context.job_queue.run_once(job_4, job_due_4, context=chat_id)
    print(" All jobs in the queue  ")


def job_1(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Ты уже прослушал *новый урок*? [ссылка](https://t.me/) \n'
    keyboard_first_stage = [
        [InlineKeyboardButton(u'Да', callback_data=str(HW_YES)),
         InlineKeyboardButton(u'Нет', callback_data=str(HW_NO))],
    ]
    reply_markup_1 = InlineKeyboardMarkup(keyboard_first_stage)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=reply_markup_1
    )


def job_2_reminder(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Напоминаю о прошедшем уроке. Когда мы общались вчера, ты еще не прослушал его.' \
                    u'Найди все же несколько минут и послушай. Он полезный :)\n'

    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def job_3(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Job 3 done'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def job_4(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Job 4 done'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def ask_author(update, context):
    reply_text = 'Вы можете задать любой вопрос авторам марафона. Что вас интересует?'
    update.message.reply_text(reply_text)

    return AUTHOR


def send_question_to_author(update, context):
    user = update.message.from_user
    from_chat_id = update.message.chat_id
    message_id = update.message.message_id
    user_id = user.id
    resend_text = '*Вопрос от участника*\n' + str(user.first_name) + ' ' + str(user.last_name) + '\n' +\
                  'ID' + str(user_id)
    bot = context.bot
    bot.send_message(
        chat_id='-272961482',
        parse_mode='Markdown',
        text=resend_text,
        reply_markup=None
    )
    bot.forward_message(
        chat_id='-272961482',
        from_chat_id=from_chat_id,
        disable_notification=False,
        message_id=message_id

    )
    reply_text = 'Спасибо за вопрос! Мы постараемся оперативно ответить.'
    update.message.reply_text(reply_text)

    return DEFAULT_CHOOSING


def faq_button_pressed(update, context):
    reply_text = 'Функционал бота:'
    update.message.reply_text(reply_text, reply_markup=default_markup)
    return DEFAULT_CHOOSING


def materials_button_pressed(update, context):
    reply_text = 'Все материалы данного курса находятся в группе Карьерный гайд.Архетипы.'
    keyboard = [
        [InlineKeyboardButton("Посмотреть материалы", url='https://t.me/joinchat/AB1pthBFD8pPFvYE6NgN3A',
                              callback_data=str(GOTO_GROUP))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(reply_text, reply_markup=inline_reply_markup)
    return DEFAULT_CHOOSING


def go_through_questionary(update, context):
    user = update.message.from_user
    chat_id = user.id
    question = 1
    keyboard = [
        [InlineKeyboardButton(" 3 ", callback_data=str(ONE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(TWO) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(THREE) + "," + str(question)),
         InlineKeyboardButton(" 0 ", callback_data=str(FOUR) + "," + str(question)),
         InlineKeyboardButton(" 1 ", callback_data=str(FIVE) + "," + str(question)),
         InlineKeyboardButton(" 2 ", callback_data=str(SIX) + "," + str(question)),
         InlineKeyboardButton(" 3 ", callback_data=str(SEVEN) + "," + str(question))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)

    if os.path.exists('database/questionary/questionary_' + str(chat_id) + '_finished'):
        message_text = u'Вы уже заполнили анкету'
        update.message.reply_text(message_text, reply_markup=default_markup)
        return DEFAULT_CHOOSING
    else:
        message_text = u'Анкета! Пожалуйста ответьте на 30 вопросов. В каждом вопросе есть два аспекта, ' \
                       u'между которыми предстоит сделать выбор. При этом важно отметить, в какой степени.'
        update.message.reply_text(message_text, reply_markup=default_markup)
        update.message.reply_photo(photo=open('archetype-test/' + str(question) + '.png', 'rb'),
                                   caption='Выберите, в какой степени это свойственно вам...',
                                   reply_markup=inline_reply_markup)
        append_answers_database(chat_id, "started", "started")
        return QUESTIONARY



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


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')


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


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


def show_data(update, context):
    update.message.reply_text("This is what you already told me:"
                              "{}".format(facts_to_str(context.user_data)))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def gettoken(source):
    with open(source, 'r') as file:
        token = file.read().replace('\n', '')
    return token


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(gettoken("tokens/getmethroughbot-token"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start,
                                     pass_job_queue=True,
                                     pass_chat_data=True)],
        states={
            DEFAULT_CHOOSING: [MessageHandler(Filters.regex(default_reply_button_1),
                                              go_through_questionary,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               MessageHandler(Filters.regex(default_reply_button_2),
                                              materials_button_pressed,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               MessageHandler(Filters.regex(default_reply_button_3),
                                              faq_button_pressed,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               MessageHandler(Filters.regex(default_reply_button_4),
                                              ask_author,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               MessageHandler(Filters.regex('^Something else...$'),
                                              custom_choice,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               CallbackQueryHandler(homework_dialog_2_yes, pattern='^' + str(HW_YES) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(homework_dialog_2_no, pattern='^' + str(HW_NO) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(ONE) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(TWO) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(THREE) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(FOUR) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(FIVE) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(SIX) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_questionary, pattern='^' + str(SEVEN) + '[,]',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True)],
            START_CHOOSING: [MessageHandler(Filters.regex(intro_choice_1),
                                            intro_choice_1_callback,
                                            pass_job_queue=True,
                                            pass_chat_data=True),
                             MessageHandler(Filters.regex(intro_choice_2),
                                            intro_choice_2_callback,
                                            pass_job_queue=True,
                                            pass_chat_data=True),
                             MessageHandler(Filters.regex(intro_choice_3),
                                            intro_choice_3_callback,
                                            pass_job_queue=True,
                                            pass_chat_data=True),
                             MessageHandler(Filters.regex(intro_choice_4),
                                            intro_choice_4_callback,
                                            pass_job_queue=True,
                                            pass_chat_data=True),
                             ],
            TYPING_REPLY: [MessageHandler(Filters.text, received_information),
                           ],
            TYPING_CHOICE: [MessageHandler(Filters.text, default_choice),
                            ],
            AUTHOR: [MessageHandler(Filters.text, send_question_to_author)
                     ],
            QUESTIONARY: [MessageHandler(Filters.regex(default_reply_button_1),
                                         default_choice_questionary,
                                         pass_job_queue=True,
                                         pass_chat_data=True),
                          MessageHandler(Filters.regex(default_reply_button_2),
                                         default_choice_questionary,
                                         pass_job_queue=True,
                                         pass_chat_data=True),
                          MessageHandler(Filters.regex(default_reply_button_3),
                                         default_choice_questionary,
                                         pass_job_queue=True,
                                         pass_chat_data=True),
                          MessageHandler(Filters.regex(default_reply_button_4),
                                         default_choice_questionary,
                                         pass_job_queue=True,
                                         pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(ONE) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(TWO) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(THREE) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(FOUR) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(FIVE) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(SIX) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True),
                          CallbackQueryHandler(next_questionare, pattern='^' + str(SEVEN) + '[,]',
                                               pass_job_queue=True,
                                               pass_chat_data=True)],
            REMINDER_LOOP_LEVEL: [CallbackQueryHandler(homework_dialog_3_incorrect, pattern='^' + str(HW_A) + '$'),
                                  CallbackQueryHandler(homework_dialog_3_incorrect, pattern='^' + str(HW_B) + '$'),
                                  CallbackQueryHandler(homework_dialog_3_incorrect, pattern='^' + str(HW_C) + '$'),
                                  CallbackQueryHandler(homework_dialog_3_correct, pattern='^' + str(HW_D) + '$')]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add conversationhandler to dispatcher it will be used for handling
    # updates
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

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
SEVEN, HW_YES_1, HW_NO_1, HW_YES_2, HW_NO_2, HW_YES_3, HW_NO_3, HW_YES_4, HW_NO_4, HW_A_1, HW_B_1, HW_C_1, HW_D_1, \
HW_A_2, HW_B_2, HW_C_2, HW_D_2, HW_A_3, HW_B_3, HW_C_3, HW_D_3, HW_A_4, HW_B_4, HW_C_4, HW_D_4, \
QUESTIONARY, REMINDER_LOOP_LEVEL, AUTHOR, EMPTY, GOTO_GROUP, GOTO_VISUAL_1, GOTO_VISUAL_2, GETTING_VOICE = range(45)

job_due_1 = datetime.combine(date(2019, 11, 8), time(12, 00))
job_due_2 = datetime.combine(date(2019, 11, 8), time(13, 00))
job_due_3 = datetime.combine(date(2019, 11, 8), time(19, 30))
job_due_4 = datetime.combine(date(2019, 11, 9), time(11, 00))
job_due_5 = datetime.combine(date(2019, 11, 10), time(18, 00))
job_due_6 = datetime.combine(date(2019, 11, 10), time(18, 1))
job_due_7 = datetime.combine(date(2019, 11, 10), time(20, 00))
job_due_8 = datetime.combine(date(2019, 11, 11), time(20, 00))
job_due_9 = datetime.combine(date(2019, 11, 13), time(11, 00))
job_due_10 = datetime.combine(date(2019, 11, 13), time(11, 1))
job_due_11 = datetime.combine(date(2019, 11, 14), time(19, 30))
job_due_12 = datetime.combine(date(2019, 11, 14), time(20, 00))
job_due_13 = datetime.combine(date(2019, 11, 15), time(11, 00))
job_due_14 = datetime.combine(date(2019, 11, 16), time(11, 30))
job_due_15 = datetime.combine(date(2019, 11, 16), time(15, 00))
job_due_16 = datetime.combine(date(2019, 11, 16), time(20, 00))
job_due_17 = datetime.combine(date(2019, 11, 19), time(11, 00))

job_due_base_1 = 23
job_due_base_2 = 10

ob_due_base_3 = 11
job_due_base_4 = 7
job_due_base_5 = 2019

#job_due_1 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_2 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_3 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_4 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_5 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_6 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_7 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_8 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_9 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_10 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_11 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_12 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_13 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_14 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_15 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_16 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))
#job_due_17 = datetime.combine(date(job_due_base_5, ob_due_base_3, job_due_base_4), time(job_due_base_1, job_due_base_2))

question_group_id = '-382184251'# -382184251 #-272961482
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
default_hw_button = 'Home work'
default_hw_button_1 = 'Home work 1'
default_hw_button_3 = 'Home work 3'
default_hw_button_5 = 'Home work 5'
default_hw_button_7 = 'Home work 7'
default_hw_button_9 = 'Home work 9'
default_hw_button_10 = 'Home work 10'
default_hw_button_11 = 'Home work 11'

intro_questionary_reply_keyboard = [[intro_choice_1, intro_choice_2],
                                    [intro_choice_3, intro_choice_4]]
default_facilitator_keyboard = [[default_reply_button_1, default_reply_button_2],
                                [default_reply_button_3, default_reply_button_4]]
default_hw_keyboard = [[default_reply_button_1, default_reply_button_2],
                       [default_reply_button_3, default_reply_button_4],
                       [default_hw_button]]
default_hw_keyboard_1 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_1]]
default_hw_keyboard_3 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_3]]
default_hw_keyboard_5 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_5]]
default_hw_keyboard_7 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_7]]
default_hw_keyboard_9 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_9]]
default_hw_keyboard_10 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_10]]
default_hw_keyboard_11 = [[default_reply_button_1, default_reply_button_2],
                         [default_reply_button_3, default_reply_button_4],
                         [default_hw_button_11]]

intro_markup = ReplyKeyboardMarkup(intro_questionary_reply_keyboard, one_time_keyboard=True)
default_markup = ReplyKeyboardMarkup(default_facilitator_keyboard, one_time_keyboard=True)
default_hw_markup = ReplyKeyboardMarkup(default_hw_keyboard, one_time_keyboard=True)
default_hw_markup_1 = ReplyKeyboardMarkup(default_hw_keyboard_1, one_time_keyboard=True)
default_hw_markup_3 = ReplyKeyboardMarkup(default_hw_keyboard_3, one_time_keyboard=True)
default_hw_markup_5 = ReplyKeyboardMarkup(default_hw_keyboard_5, one_time_keyboard=True)
default_hw_markup_7 = ReplyKeyboardMarkup(default_hw_keyboard_7, one_time_keyboard=True)
default_hw_markup_9 = ReplyKeyboardMarkup(default_hw_keyboard_9, one_time_keyboard=True)
default_hw_markup_10 = ReplyKeyboardMarkup(default_hw_keyboard_10, one_time_keyboard=True)
default_hw_markup_11 = ReplyKeyboardMarkup(default_hw_keyboard_11, one_time_keyboard=True)


def empty(context):
    aaa = 1


def if_hw_due(hw, chat_id):
    if os.path.exists('database/text/hw_' + str(hw) + '_id_' + str(chat_id) + '_finished'):
        return False
    else:
        return True


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def intro_choice_1_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_1, reply_markup=default_markup)
    chat_id = update.message.chat_id
    context.user_data['id'] = str(chat_id)
    write_hw_text(chat_id, 0, "done 1")
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_2_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_2, reply_markup=default_markup)
    chat_id = update.message.chat_id
    context.user_data['id'] = str(chat_id)
    write_hw_text(chat_id, 0, "done 2")
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_3_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_3, reply_markup=default_markup)
    chat_id = update.message.chat_id
    context.user_data['id'] = str(chat_id)
    write_hw_text(chat_id, 0, "done 3")
    start_user_queue(update, context)

    return DEFAULT_CHOOSING


def intro_choice_4_callback(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    update.message.reply_text(intro_reply_button_4, reply_markup=default_markup)
    chat_id = update.message.chat_id
    context.user_data['id'] = str(chat_id)
    write_hw_text(chat_id, 0, "done 4")
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
            text="Тест завершен. Отлично! К результатам оценки мы вернемся чуть позже",
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


###############################################################################################

def dialog_1_yes(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_a = u'Помни о будущем, соблюдай правила'
    text_reply_b = u'Главное, чтобы нам было хорошо вместе'
    text_reply_c = u'Побеждает сильнейший'
    text_reply_d = u'Истина в познании'
    text_reply_yes = u'Отлично!'
    text_reply_quest = u'Задание 2. Как думаешь, какая фраза характеризует человека с архетипом Мага? ' \
                       u'(один из вариантов правильный)'
    keyboard_second_stage = [
        [InlineKeyboardButton(text_reply_a, callback_data=str(HW_A_1))],
        [InlineKeyboardButton(text_reply_b, callback_data=str(HW_B_1))],
        [InlineKeyboardButton(text_reply_c, callback_data=str(HW_C_1))],
        [InlineKeyboardButton(text_reply_d, callback_data=str(HW_D_1))]
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


def dialog_1_no(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_no = u'А зря! Там я рассказываю про первый архетип, и первые студенты уже ответили на задания'
    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Обязательно послушай позже!",
        reply_markup=default_markup
    )

    write_hw_text(query.message.chat_id, 2, "no")
    set_reminder_1(update, context)

    return DEFAULT_CHOOSING


def dialog_1_correct(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_yes = u'Супер! Все правильно :)'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_yes,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 2, "correct")

    return DEFAULT_CHOOSING


def dialog_1_incorrect(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_no = u'Не совсем верно... другая фраза лучше описывает человека с архетипом Мага'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_no,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 2, "incorrect")
    return DEFAULT_CHOOSING


#####################################################################################

def dialog_2_yes(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_a = u'Материальные достижения, имеющиеся ресурсы'
    text_reply_b = u'Социальное положение, статус'
    text_reply_c = u'Эмоциональный контакт, нравится-не нравится'
    text_reply_d = u'Глубина экспертизы и знаний'
    text_reply_yes = u'Отлично!'
    text_reply_quest = u'Задание 4. На что обращает внимание в коммуникации с другим человеком человек с ' \
                       u'архетипом Любящего?'
    keyboard_second_stage = [
        [InlineKeyboardButton(text_reply_a, callback_data=str(HW_A_2))],
        [InlineKeyboardButton(text_reply_b, callback_data=str(HW_B_2))],
        [InlineKeyboardButton(text_reply_c, callback_data=str(HW_C_2))],
        [InlineKeyboardButton(text_reply_d, callback_data=str(HW_D_2))]
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


def dialog_2_no(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_no = u'А мы тем временем готовим отчет для тебя, и будем рады его отправить. ' \
                    u'Для этого нужно выполнить задания!'
    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Обязательно послушай позже!",
        reply_markup=default_markup
    )
    write_hw_text(query.message.chat_id, 4, "no")
    set_reminder_2(update, context)

    return DEFAULT_CHOOSING


def dialog_2_correct(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_yes = u'Отлично! Все верно :)'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_yes,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 4, "correct")
    return DEFAULT_CHOOSING


def dialog_2_incorrect(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_no = u'Не точно... Люди с архетипом Любящего сфокусированы на другом'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_no,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 4, "incorrect")
    return DEFAULT_CHOOSING


######################################################################################

def dialog_3_yes(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_a = u'Жизнь – это подиум, и надо выглядеть ярко на нем'
    text_reply_b = u'Делай что должен, и будь что будет'
    text_reply_c = u'Когда я в потоке, забываю счет времени'
    text_reply_d = u'Можно найти лучшее решение, давайте обсудим еще'
    text_reply_yes = u'Отлично!'
    text_reply_quest = u'Задание 6. Какая фраза лучше всего описывает человека с архетипом Воина?'
    keyboard_second_stage = [
        [InlineKeyboardButton(text_reply_a, callback_data=str(HW_A_3))],
        [InlineKeyboardButton(text_reply_b, callback_data=str(HW_B_3))],
        [InlineKeyboardButton(text_reply_c, callback_data=str(HW_C_3))],
        [InlineKeyboardButton(text_reply_d, callback_data=str(HW_D_3))]
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


def dialog_3_no(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_no = u'Нам очень жаль, что тебе не удалось найти время. Мы подготовили полезный контент для тебя.'
    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Обязательно послушай позже!",
        reply_markup=default_markup
    )
    write_hw_text(query.message.chat_id, 6, "no")
    set_reminder_3(update, context)

    return DEFAULT_CHOOSING


def dialog_3_correct(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_yes = u'Замечательно! Все верно :)'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_yes,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 6, "correct")
    return DEFAULT_CHOOSING


def dialog_3_incorrect(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_no = u'Не совсем верно... другая фраза лучше описывает человека с архетипом Воина'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_no,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 6, "incorrect")
    return DEFAULT_CHOOSING


########################################################################################

def dialog_4_yes(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_a = u'Инновационность, глубина и детализация решений'
    text_reply_b = u'Эмоц. поддержка в ситуациях стресса и кризиса'
    text_reply_c = u'Умение конкурировать и достигать целей в срок'
    text_reply_d = u'Лидерство, системность, забота о подчиненных'
    text_reply_yes = u'Отлично!'
    text_reply_quest = u'Задание 8. В чем особенно хороши люди с архетипом Монарха?'
    keyboard_second_stage = [
        [InlineKeyboardButton(text_reply_a, callback_data=str(HW_A_4))],
        [InlineKeyboardButton(text_reply_b, callback_data=str(HW_B_4))],
        [InlineKeyboardButton(text_reply_c, callback_data=str(HW_C_4))],
        [InlineKeyboardButton(text_reply_d, callback_data=str(HW_D_4))]
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


def dialog_4_no(update, context):
    query = update.callback_query
    bot = context.bot
    text_reply_no = u'Ок. Это твое решение :)'
    bot.send_message(
        chat_id=query.message.chat_id,
        text=text_reply_no,
        reply_markup=None
    )
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Но я все же советую послушать его, когда будет время.",
        reply_markup=default_markup
    )
    write_hw_text(query.message.chat_id, 8, "no")
    set_reminder_4(update, context)

    return DEFAULT_CHOOSING


def dialog_4_correct(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_yes = u'Превосходно :)'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_yes,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 8, "correct")
    return DEFAULT_CHOOSING


def dialog_4_incorrect(update, context):
    query = update.callback_query
    bot = context.bot
    text_response_reply_no = u'Не совсем... Таланты Монарха лежат в другой области'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text_response_reply_no,
        reply_markup=None
    )
    write_hw_text(query.message.chat_id, 8, "incorrect")
    return DEFAULT_CHOOSING


##########################################################################################

def set_reminder_1(update, context):
    query = update.callback_query
    print("Reminder 1 set")
    context.job_queue.run_once(job_7, job_due_7, context=query.message.chat_id)


def set_reminder_2(update, context):
    query = update.callback_query
    print("Reminder 2 set")
    context.job_queue.run_once(job_8, job_due_8, context=query.message.chat_id)


def set_reminder_3(update, context):
    query = update.callback_query
    print("Reminder 3 set")
    context.job_queue.run_once(job_12, job_due_12, context=query.message.chat_id)


def set_reminder_4(update, context):
    query = update.callback_query
    print("Reminder 4 set")
    context.job_queue.run_once(job_16, job_due_16, context=query.message.chat_id)


#####################################################################################

def start_visual_1(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    context.bot.sendVoice(chat_id,
                          voice=open('voice-messages/visualization/v1.ogg', 'rb'),
                          caption='ВИЗУАЛИЗАЦИЯ - успешный день',
                          reply_markup=default_hw_markup_10
                          )
    return DEFAULT_CHOOSING


def start_visual_2(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    context.bot.sendVoice(chat_id,
                          voice=open('voice-messages/visualization/v2.ogg', 'rb'),
                          caption='ВИЗУАЛИЗАЦИЯ - хобби',
                          reply_markup=default_hw_markup_11
                          )
    return DEFAULT_CHOOSING


def voice_received_1(update, context):
    # voice = update.message.voice
    reply_text = 'Благодарю! Мы тем временем готовим подробный отчет :)'

    update.message.reply_text(reply_text)
    return DEFAULT_CHOOSING


################################################################################################

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
    context.job_queue.run_once(job_1, job_due_1, context=chat_id)
    context.job_queue.run_once(job_2, job_due_2, context=chat_id)
    context.job_queue.run_once(job_3, job_due_3, context=chat_id)
    context.job_queue.run_once(job_4, job_due_4, context=chat_id)
    context.job_queue.run_once(job_5, job_due_5, context=chat_id)
    context.job_queue.run_once(job_6, job_due_6, context=chat_id)
    context.job_queue.run_once(job_9, job_due_9, context=chat_id)
    context.job_queue.run_once(job_10, job_due_10, context=chat_id)
    context.job_queue.run_once(job_11, job_due_11, context=chat_id)
    context.job_queue.run_once(job_13, job_due_13, context=chat_id)
    context.job_queue.run_once(job_14, job_due_14, context=chat_id)
    context.job_queue.run_once(job_15, job_due_15, context=chat_id)
    context.job_queue.run_once(job_17, job_due_17, context=chat_id)

    print(" All jobs in the queue  ")


def job_1(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Когда будет возможность выделить 5 минут, пройдите оценку \n(кнопка Diagnostics)'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def job_2(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Будет круто, если ты пройдешь опрос до следующего занятия.'
    if os.path.exists('database/questionary/questionary_' + str(chat_id) + '_finished'):
        empty(context)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=init_question,
            reply_markup=default_markup
        )


def job_3(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! И первое задание марафона. Приведи пример героя фильма или книги или публичную личность' \
                    u' с ведущим архетипом МАГА.'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_hw_markup_1
    )


def job_4(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Ты уже прослушал новый урок?'
    keyboard_first_stage = [
        [InlineKeyboardButton(u'Да', callback_data=str(HW_YES_1)),
         InlineKeyboardButton(u'Нет', callback_data=str(HW_NO_1))],
    ]
    reply_markup_1 = InlineKeyboardMarkup(keyboard_first_stage)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=reply_markup_1
    )


def job_5(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Задание 3: Приведи пример героя фильма или книги или публичную личность с' \
                    u' ведущим архетипом Любящего.'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_hw_markup_3
    )


def job_6(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Ты уже прослушал новый урок?'
    keyboard_first_stage = [
        [InlineKeyboardButton(u'Да', callback_data=str(HW_YES_2)),
         InlineKeyboardButton(u'Нет', callback_data=str(HW_NO_2))],
    ]
    reply_markup_1 = InlineKeyboardMarkup(keyboard_first_stage)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=reply_markup_1
    )


def job_7(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Напоминание! Тебя ждет урок по архетипу МАГА. Обязательно послушай'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )

def job_8(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Напоминание! Тебя ждет урок по архетипу ЛЮБЯЩЕГО. Обязательно послушай'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )

def job_9(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Задание 5 марафона. Приведи пример героя фильма или книги или публичную ' \
                    u'личность с ведущим архетипом ВОИНА.'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_hw_markup_5
    )


def job_10(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Ты уже послушал новый эфир?'
    keyboard_first_stage = [
        [InlineKeyboardButton(u'Да', callback_data=str(HW_YES_3)),
         InlineKeyboardButton(u'Нет', callback_data=str(HW_NO_3))],
    ]
    reply_markup_1 = InlineKeyboardMarkup(keyboard_first_stage)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=reply_markup_1
    )


def job_11(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Задание 7 марафона. Приведи пример героя фильма или книги или публичную ' \
                    u'личность с ведущим архетипом ВОИНА.'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_hw_markup_7
    )


def job_12(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Напоминание! Тебя ждет урок по архетипу ВОИНА. Обязательно послушай'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def job_13(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Привет! Ты уже послушал новый эфир?'
    keyboard_first_stage = [
        [InlineKeyboardButton(u'Да', callback_data=str(HW_YES_4)),
         InlineKeyboardButton(u'Нет', callback_data=str(HW_NO_4))],
    ]
    reply_markup_1 = InlineKeyboardMarkup(keyboard_first_stage)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=reply_markup_1
    )


def job_14(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = 'Задание 9. Вспомни, пожалуйста, компании в которых ты работал, если уже был профессиональный ' \
                    'опыт. Если не было официальной работы, возможно, у тебя был опыт в молодежной организации ' \
                    'или группе.'
    question_1 = 'А теперь подумай, какие из них были самые продуктивные для тебя - где ты чувствовал себя на своем' \
                 ' месте. Что тебе нравилось в них? Выбери 3 (из предложенных вариантов)'
    question_2 = 'Какие из них были самые деструктивные для тебя - где или когда ты был уверен, что место не ' \
                 'твое. Что тебя беспокоило в них? Выбери не 3 (из предложенных вариантов)'
    choice_1_1 = '*1* Осведомленность о новых трендах / инновациях, аккумулирование информации.\n'
    choice_1_2 = '*2* Повышенное внимание к деталям и нюансам, способность замечать вещи, которые не видят другие, ' \
                 'стремление познать суть вещей, «докопаться до истины».\n'
    choice_1_3 = '*3* Нацеленность на эффективность и победу, быстрое принятие решений даже в условиях ' \
                 'неопределенности\n'
    choice_1_4 = '*4* Фокус на практической стороне задачи, ярко выражена готовность отвечать за собственную работу ' \
                 '/ собственный вклад.\n'
    choice_1_5 = '*5* Приятная и доверительная атмосфера в команде. Ценность личности и комфортного взаимодействия.\n'
    choice_1_6 = '*6* Спонтанное и творческое проявление себя и своих способностей дается легко и с удовольствием.\n'
    choice_1_7 = '*7* приветствуется создание новых идей, идеалов и таких возможностей, каких раньше никогда не было.\n'
    choice_1_8 = '*8* Оптимизм, способность представить вещи в позитивном ключе и умение «заразить», вовлечь, ' \
                 'воодушевить окружающих.\n'
    choice_2_1 = '*1* Избегание личного контакта для решения ситуации, стремление "отстранится", свести взаимодействие' \
                 'к формальности.\n'
    choice_2_2 = '*2* Акцент на негативных сценариях, поиск недостатков, подозрительность к возможностям и хорошим ' \
                 'событиям / ситуациям.\n'
    choice_2_3 = '*3* Построение барьеров, проведение границ между "своими" и "чужими", разделение на "лагери".\n'
    choice_2_4 = '*4* Излишняя конкуренция, борьба, сравнение с целью доказать, кто прав / кто выиграл/ кто лучше.\n'
    choice_2_5 = '*5* Повышенная чувствительность к происходящим ситуациям / событиям, излишняя эмоциональность.\n'
    choice_2_6 = '*6* Неспособность проявить себя независимо/ самостоятельно, стремление зависеть, ' \
                 '"слиться" с коллективом.\n'
    choice_2_7 = '*7* Стремление идеализировать и приукрашать возможности, предлагать грандиозные планы ' \
                 'в ущерб реальности.\n'
    choice_2_8 = '*8* Желание произвести впечатление/ эффект, показать себя в лучшем свете, привлечь, ' \
                 'продемонстрировать достоинства.\n'
    options_1 = choice_1_1 + choice_1_2 + choice_1_3 + choice_1_4 + choice_1_5 + choice_1_6 + choice_1_7 + choice_1_8
    options_2 = choice_2_1 + choice_2_2 + choice_2_3 + choice_2_4 + choice_2_5 + choice_2_6 + choice_2_7 + choice_2_8
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        parse_mode='Markdown',
        reply_markup=default_hw_markup_9
    )
    bot.send_message(
        chat_id=chat_id,
        text=question_1,
        parse_mode='Markdown',
        reply_markup=default_hw_markup_9
    )
    bot.send_message(
        chat_id=chat_id,
        text=options_1,
        parse_mode='Markdown',
        reply_markup=default_hw_markup_9
    )
    bot.send_message(
        chat_id=chat_id,
        text=question_2,
        parse_mode='Markdown',
        reply_markup=default_hw_markup_9
    )
    bot.send_message(
        chat_id=chat_id,
        text=options_2,
        parse_mode='Markdown',
        reply_markup=default_hw_markup_9
    )


def job_15(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'И задание 10. Это будет визуализация. Давай попробуем :) Выдели себе 10 минут, когда тебя ' \
                    u'никто не будет беспокоить. Сядь удобно и нажми на кнопку ВИЗУАЛИЗАЦИЯ'
    keyboard = [
        [InlineKeyboardButton("Получить визуализацию", callback_data=str(GOTO_VISUAL_1))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=inline_reply_markup
    )


def job_16(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'Напоминание! Тебя ждет урок по архетипу МОНАРХА. Обязательно послушай'
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=default_markup
    )


def job_17(context):
    job = context.job
    chat_id = job.context
    bot = context.bot
    init_question = u'И задание 11. Это снова визуализация. Надеемся, тебе понравилась прошлая :) Выдели себе 10' \
                    u' минут, когда тебя никто не будет беспокоить. Сядь удобно и нажми на кнопку ВИЗУАЛИЗАЦИЯ'
    keyboard = [
        [InlineKeyboardButton("Получить визуализацию", callback_data=str(GOTO_VISUAL_2))]
    ]
    inline_reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text=init_question,
        reply_markup=inline_reply_markup
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
    resend_text = '*Вопрос от участника*\n' + str(user.first_name) + ' ' + str(user.last_name) + '\n' + \
                  'ID' + str(user_id)
    bot = context.bot
    bot.send_message(
        chat_id=question_group_id,
        parse_mode='Markdown',
        text=resend_text,
        reply_markup=None
    )
    bot.forward_message(
        chat_id=question_group_id,
        from_chat_id=from_chat_id,
        disable_notification=False,
        message_id=message_id

    )
    reply_text = 'Спасибо за вопрос! Мы постараемся оперативно ответить.'
    update.message.reply_text(reply_text)

    return DEFAULT_CHOOSING


def faq_button_pressed(update, context):
    reply_text = '*Функционал бота:*\n' \
                 '*1* Кнопка Diagnostics запускает анкету на определение вашего ведущего архетипа\n' \
                 '*2* Кнопка Materials предоставляет ссылку на группу, в которой по мере прохождения курса ' \
                 'появляются все материалы\n' \
                 '*3* Кнопка Ask author позвляет задать вопрос автору (бот сам отправит его)\n\n' \
                 'При возникновении любых технических вопросов - обращайтесь к Timur Shagiakhmetov (участнк группы)\n' \
                 'Бот сейчас в бета версии, поэтому не судите строго :)\n'
    update.message.reply_text(reply_text, parse_mode='Markdown', reply_markup=default_markup)
    return DEFAULT_CHOOSING


def materials_button_pressed(update, context):
    reply_text = 'Все материалы данного курса находятся в группе Карьерный гайд.Архетипы.'
    keyboard = [
        [InlineKeyboardButton("Посмотреть материалы", url='https://t.me/joinchat/AB1ptlhsh4xOm4bcNbzlOg',
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
    reply_text = 'Напишите ответ'
    update.message.reply_text(reply_text)

    return TYPING_REPLY


def received_information(update, context):
    print("start receiving")
    text = update.message.text
    now = datetime.now()
    user_id = context.user_data['id']

    if (now.day == 8) or (now.day == 9) or ((now.day == 10) and (now.hour < 18)):
        print("HW 1")
        write_hw_text(user_id, 1, text)
    elif ((now.day == 10) and (now.hour >= 18)) or (now.day == 11) or (now.day == 12) or \
            ((now.day == 13) and (now.hour < 11)):
        print("HW 3")
        write_hw_text(user_id, 3, text)
    elif ((now.day == 13) and (now.hour >= 11)) or ((now.day == 14) and (now.hour < 19)):
        print("HW 5")
        write_hw_text(user_id, 5, text)
    elif ((now.day == 14) and (now.hour >= 19)) or (now.day == 15) or ((now.day == 16) and (now.hour < 11)):
        print("HW 7")
        write_hw_text(user_id, 7, text)
    elif (now.day == 16) and (now.hour >= 11) and (now.hour < 15):
        print("HW 9")
        write_hw_text(user_id, 9, text)
    elif ((now.day == 16) and (now.hour >= 15)) or (now.day == 17) or (now.day == 18) or \
            ((now.day == 19) and (now.hour < 11)):
        print("HW 10")
        write_hw_text(user_id, 10, text)
    elif ((now.day == 19) and (now.hour >= 11)) or (now.day == 20):
        print("HW 11")
        write_hw_text(user_id, 11, text)
    elif now.day == 7:
        print("HW test today 7")
        write_hw_text(user_id, 150, text)
    else:
        print("something with homework timetable")

    update.message.reply_text("Спасибо!", reply_markup=default_markup)

    return DEFAULT_CHOOSING


def write_hw_text(chat_id, hw, text):
    f = open('database/text/hw_id_' + str(chat_id) + '_finished', "a")
    f.write(str(hw) + ' Задание: ' + str(text) + "\n")
    f.close()


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
                               MessageHandler(Filters.regex(default_hw_button),
                                              default_choice,
                                              pass_job_queue=True,
                                              pass_chat_data=True),
                               CallbackQueryHandler(dialog_1_yes, pattern='^' + str(HW_YES_1) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_1_no, pattern='^' + str(HW_NO_1) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_2_yes, pattern='^' + str(HW_YES_2) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_2_no, pattern='^' + str(HW_NO_2) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_3_yes, pattern='^' + str(HW_YES_3) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_3_no, pattern='^' + str(HW_NO_3) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_4_yes, pattern='^' + str(HW_YES_4) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(dialog_4_no, pattern='^' + str(HW_NO_4) + '$',
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
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_visual_1, pattern='^' + str(GOTO_VISUAL_1) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True),
                               CallbackQueryHandler(start_visual_2, pattern='^' + str(GOTO_VISUAL_2) + '$',
                                                    pass_job_queue=True,
                                                    pass_chat_data=True)
                               ],
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
            REMINDER_LOOP_LEVEL: [CallbackQueryHandler(dialog_1_incorrect, pattern='^' + str(HW_A_1) + '$'),
                                  CallbackQueryHandler(dialog_1_incorrect, pattern='^' + str(HW_B_1) + '$'),
                                  CallbackQueryHandler(dialog_1_incorrect, pattern='^' + str(HW_C_1) + '$'),
                                  CallbackQueryHandler(dialog_1_correct, pattern='^' + str(HW_D_1) + '$'),
                                  CallbackQueryHandler(dialog_2_incorrect, pattern='^' + str(HW_A_2) + '$'),
                                  CallbackQueryHandler(dialog_2_incorrect, pattern='^' + str(HW_B_2) + '$'),
                                  CallbackQueryHandler(dialog_2_correct, pattern='^' + str(HW_C_2) + '$'),
                                  CallbackQueryHandler(dialog_2_incorrect, pattern='^' + str(HW_D_2) + '$'),
                                  CallbackQueryHandler(dialog_3_incorrect, pattern='^' + str(HW_A_3) + '$'),
                                  CallbackQueryHandler(dialog_3_correct, pattern='^' + str(HW_B_3) + '$'),
                                  CallbackQueryHandler(dialog_3_incorrect, pattern='^' + str(HW_C_3) + '$'),
                                  CallbackQueryHandler(dialog_3_incorrect, pattern='^' + str(HW_D_3) + '$'),
                                  CallbackQueryHandler(dialog_4_incorrect, pattern='^' + str(HW_A_4) + '$'),
                                  CallbackQueryHandler(dialog_4_incorrect, pattern='^' + str(HW_B_4) + '$'),
                                  CallbackQueryHandler(dialog_4_incorrect, pattern='^' + str(HW_C_4) + '$'),
                                  CallbackQueryHandler(dialog_4_correct, pattern='^' + str(HW_D_4) + '$')
                                  ]
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

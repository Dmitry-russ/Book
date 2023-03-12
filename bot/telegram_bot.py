import logging
import os
import sys

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler, Updater, MessageHandler,
                          Filters, CallbackQueryHandler)

from consts import (TRAIN_ENDPOINT, MAI_ENDPOINT, USER_ENDPOINT, USERS,
                    CASE_ENDPOINT, MAI_NEXT_ENDPOINT)
from getapi import get_token, check_train, finde_mai, finde_case
from utils import check_user, send_me_messege

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
MY_CHAT_ID = os.getenv('MY_CHAT_ID')

# декоратор на проверку времени токена перед запуском запрсов???
API_TOKEN = get_token(USER_ENDPOINT, USER, PASSWORD)

logger = logging.getLogger()


def wake_up(update, context):
    """Приветствие при запуске."""

    chat_id = update.effective_chat.id
    name = update.message.chat.first_name
    username = update.effective_chat.username

    check_user(update, context, USERS)

    context.bot.send_message(
        chat_id=chat_id,
        text=f'{name} привет! Введи номер поезда. '
             f'Только цифры (к примеру: 001) - '
             f'я выведу три последние инспекци.',
    )
    messege = f'User {username}, {chat_id} is starting bot.'
    logging.info(messege)
    send_me_messege(context, MY_CHAT_ID, messege)


def error_handler(update, context):
    """Обработка ошибок."""
    username = update.effective_chat.username
    messege_for_me = f'Ошибка: {str(context.error)}\n Пользователь: {username}'
    messege = 'Ошибка обработки запроса. Обратитесь к администратору.'
    user_chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=user_chat_id,
                             text=messege)
    send_me_messege(context, MY_CHAT_ID, messege_for_me)


def have_massege(update, context):
    """Обработка входящего сообщения."""
    chat_id = update.effective_chat.id
    text = update.message.text

    username = update.effective_chat.username
    messege_for_me = f'Пользователь {username}, {chat_id} запросил: {text}'
    send_me_messege(context, MY_CHAT_ID, messege_for_me)

    trains = check_train(TRAIN_ENDPOINT, API_TOKEN, text)
    if trains is None or len(trains) < 1:
        context.bot.send_message(
            chat_id=chat_id,
            text='Поезд не найден.')
        return
    if len(trains) > 1:
        keyboard: list = []
        for train in trains:
            serial_slug = train.get('serial').get('slug')
            serial_serial = train.get('serial').get('serial')
            train_number = train.get('number')
            keyboard.append([InlineKeyboardButton(
                f"{serial_serial}-{train_number}",
                callback_data=f'{serial_slug} {train_number}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id,
                                 text="Выберете поезд:",
                                 reply_markup=reply_markup)
        return
    if len(trains) == 1:
        serial_slug = trains[0].get('serial').get('slug')
        serial_serial = trains[0].get('serial').get('serial')
        text = f'{serial_slug} {text}'
        result_messege, reply_markup = finde_mai(MAI_ENDPOINT,
                                                 MAI_NEXT_ENDPOINT,
                                                 API_TOKEN,
                                                 text, )
        context.bot.send_message(
            chat_id=chat_id,
            text=result_messege)
        context.bot.send_message(chat_id=chat_id,
                                 text='Вывести замечания по поезду:',
                                 reply_markup=reply_markup)


def button(update, context):
    """Обработка действий нажатия кнопки."""
    chat_id = update.effective_chat.id
    query = update.callback_query
    text = query.data
    if 'case' not in text:
        result_messege, reply_markup = finde_mai(MAI_ENDPOINT,
                                                 MAI_NEXT_ENDPOINT,
                                                 API_TOKEN,
                                                 text, )
        context.bot.send_message(chat_id=chat_id, text=result_messege)
        context.bot.send_message(chat_id=chat_id,
                                 text='Вывести замечания по поезду:',
                                 reply_markup=reply_markup)
        return
    result_messege = finde_case(CASE_ENDPOINT, API_TOKEN, text)
    context.bot.send_message(chat_id=chat_id, text=result_messege)


def check_tokens() -> bool:
    """Проверка наличия переменных в окружении."""

    return all([TELEGRAM_BOT_TOKEN, USER, PASSWORD])


def main():
    """Основная логика работы бота."""

    if not check_tokens():
        logging.critical('There is no data in the environment. '
                         'The function is stopped.')
        raise sys.exit()
    logging.info('Main function is strating.')

    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, have_massege))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.log',
        format=(
            '%(asctime)s, %(levelname)s, %(message)s,'
            '%(name)s, %(funcName)s, %(lineno)d'),
        filemode='a',
    )
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(message)s,'
        '%(name)s, %(funcName)s, %(lineno)d')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    main()

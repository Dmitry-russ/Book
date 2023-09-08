import logging
import os
import sys

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler, Updater, MessageHandler,
                          Filters, CallbackQueryHandler)

from botengine import summerwinter, metrolog, measurement
from consts import (TRAIN_ENDPOINT, MAI_ENDPOINT, USER_ENDPOINT, USERS,
                    CASE_ENDPOINT, MAI_NEXT_ENDPOINT, TRAIN_ALL_ENDPOINT,
                    METROLOG_ENDPOINT, CERTIFICATES_ENDPOINT)
from getapi import (get_token, check_train,
                    finde_mai, finde_case, get_metrolog,
                    get_measurement, get_photo, get_certificates, get_file)
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
    logging.info(f'Пользователь {username} пытается запустить бот.')
    check_user(update, context, USERS)

    context.bot.send_message(
        chat_id=chat_id,
        text=f'{name} привет! Введи номер поезда. '
             f'Только цифры (к примеру: 001) - '
             f'я найду поезда под этим номером и предложу '
             f'вывести по ним три последние инспекции '
             f'или продолжить поиск по базе систем измерения. '
             f'Если я не найду поездов по предложенному номеру, '
             f'то продолжу поиск'
             f' по базе систем измерения автоматически. Поиск в базе ведется'
             f' по полям "описание" и "серийный номер".'
             f'\n\nДоступные отчеты:'
             f'\n/summer - отчет по переводам в лето'
             f'\n/winter - отчет по переводам в зиму'
             f'\n/30days - отчет по 30 суткам',
    )
    messege = f'Пользователь {username}, чат {chat_id}, запустил бот.'
    logging.info(messege)
    send_me_messege(context, MY_CHAT_ID, messege)


def error_handler(update, context):
    """Обработка ошибок."""
    username = update.effective_chat.username
    messege_for_me = f'Ошибка: {str(context.error)}\n Пользователь: {username}'
    messege = ('Ошибка обработки запроса. '
               'Обратитесь к администратору или попробуйте еще раз.')
    if str(context.error) == 'Timed out':
        messege = 'Ошибка Timed out. Повторите запрос.'
    user_chat_id = update.effective_chat.id
    logging.critical(f'{messege_for_me}')
    context.bot.send_message(chat_id=user_chat_id,
                             text=messege)
    send_me_messege(context, MY_CHAT_ID, messege_for_me)


def have_massege(update, context):
    """Обработка входящего сообщения."""
    chat_id = update.effective_chat.id
    text = update.message.text

    username = update.effective_chat.username
    logging.info(f'Пользователь {username}, чат {chat_id}, запросил: {text}')

    if '/' in text:
        data = text.replace('/', '')
        result = get_measurement(METROLOG_ENDPOINT, API_TOKEN, data)
        messege, reply_markup = measurement(result)
        if reply_markup:
            context.bot.send_message(
                chat_id=chat_id,
                text=messege,
                reply_markup=reply_markup, )
        else:
            messege += ' Фото не найдено.'
            context.bot.send_message(
                chat_id=chat_id,
                text=messege, )
        return
    trains = check_train(TRAIN_ENDPOINT, API_TOKEN, text)
    if trains is not None and len(trains) > 0:
        keyboard: list = []
        for train in trains:
            serial_slug = train.get('serial').get('slug')
            serial_serial = train.get('serial').get('serial')
            train_number = train.get('number')
            keyboard.append([InlineKeyboardButton(
                f"{serial_serial}-{train_number}",
                callback_data=f'{serial_slug} {train_number}')])
        keyboard.append([InlineKeyboardButton(
            "Продолжить поиск по метрологии",
            callback_data=f'продолжить {text}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id,
                                 text="Выбрать поезд или продолжить поиск СИ.",
                                 reply_markup=reply_markup)
        return
    if trains is None or len(trains) < 1:
        context.bot.send_message(
            chat_id=chat_id,
            text='Поезд не найден, продолжаю поиск по метрологии.')

    result = get_metrolog(METROLOG_ENDPOINT, API_TOKEN, text)
    result_text = metrolog(result)
    context.bot.send_message(
        chat_id=chat_id,
        text=result_text)

    # if len(trains) == 1:
    #     serial_slug = trains[0].get('serial').get('slug')
    #     serial_serial = trains[0].get('serial').get('serial')
    #     text = f'{serial_slug} {text}'
    #     result_messege, reply_markup = finde_mai(MAI_ENDPOINT,
    #                                              MAI_NEXT_ENDPOINT,
    #                                              API_TOKEN,
    #                                              text, )
    #     context.bot.send_message(
    #         chat_id=chat_id,
    #         text=result_messege)
    #     context.bot.send_message(chat_id=chat_id,
    #                              text='Вывести замечания по поезду:',
    #                              reply_markup=reply_markup)


def summer(update, context):
    """Функция отчет по лету."""

    logging.info(f'Пользователь {update.effective_chat.username},'
                 f'чат {update.effective_chat.id}, запросил: лето')

    text = 'summer'
    summerwinter(update, context, text,
                 TRAIN_ALL_ENDPOINT, MAI_ENDPOINT, API_TOKEN)


def days30(update, context):
    """Функция отчет по 30 суткам."""
    logging.info(f'Пользователь {update.effective_chat.username},'
                 f'чат {update.effective_chat.id}, '
                 f'запросил: 30 суточный отчет')
    text = '30days'
    summerwinter(update, context, text,
                 TRAIN_ALL_ENDPOINT, MAI_ENDPOINT, API_TOKEN)


def winter(update, context):
    """Функция отчет по зиме."""

    logging.info(f'Пользователь {update.effective_chat.username},'
                 f'чат {update.effective_chat.id}, запросил: лето')

    text = 'winter'
    summerwinter(update, context, text,
                 TRAIN_ALL_ENDPOINT, MAI_ENDPOINT, API_TOKEN)


def button(update, context):
    """Обработка действий нажатия кнопки."""
    chat_id = update.effective_chat.id
    query = update.callback_query
    text = query.data

    if 'продолжить' in text:
        textchange = text.split()
        data = textchange[1]
        result = get_metrolog(METROLOG_ENDPOINT, API_TOKEN, data)
        result_text = metrolog(result)
        context.bot.send_message(
            chat_id=chat_id,
            text=result_text)
        return

    if 'metrolog' in text:
        file = get_photo(text, API_TOKEN)
        context.bot.send_photo(chat_id, file)
        return

    if 'поиск сертификата' in text:
        textchange = text.split()
        id = int(textchange[2])
        certificates = get_certificates(id, CERTIFICATES_ENDPOINT, API_TOKEN)
        if len(certificates) == 0:
            context.bot.send_message(
                chat_id=chat_id,
                text='Сертификаты не найдены')
        for cert in certificates:
            url = cert.get('file')
            file = get_file(url, API_TOKEN)
            context.bot.send_document(chat_id, file)
        return

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
    updater.dispatcher.add_handler(CommandHandler('summer', summer))
    updater.dispatcher.add_handler(CommandHandler('winter', winter))
    updater.dispatcher.add_handler(CommandHandler('30days', days30))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, have_massege))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='log.log',
        format=(
            '%(asctime)s, %(levelname)s, %(message)s,'
            '%(name)s, %(funcName)s, %(lineno)d'),
        filemode='a',
    )
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(message)s,'
        '%(name)s, %(funcName)s, %(lineno)d')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    main()

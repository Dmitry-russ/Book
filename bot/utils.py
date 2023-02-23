from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def check_user(update, context, USERS):
    username = update.effective_chat.username
    name = update.message.chat.first_name
    chat_id = update.effective_chat.id
    if username not in USERS:
        context.bot.send_message(
            chat_id=chat_id,
            text=f'{name} привет! Пользователь не найден. '
                 f'Доступ запрещен.', )
        return False
    return True


def case_buttons(serial_serial, train_number, serial_slug,):
    keyboard: list = []
    keyboard.append([InlineKeyboardButton(
                f"{serial_serial}-{train_number}",
                callback_data=f'{serial_slug} {train_number} case')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def send_me_messege(context, MY_CHAT_ID, messege):
    context.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=messege,
    )


def check_token_time(previos_date):
    pass

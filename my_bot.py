from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode

# Создаем обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот компании KIVI. Для начала работы отправьте команду /checkin. Так же помни, что мы можем запросить отправить свою геолокацию, но мы доверяем тебе и не хотим разряжать батарею твоего телефона - по этому отправлять геолокацию не обязательно - достаточно фотографии в торговом зале.")

# Создаем объект updater и регистрируем обработчики команд и сообщений
updater = Updater(token='5881314782:AAEkrF5O0s7HWGJANYPtCZAboP_POZ3fRvw', use_context=True)
dp = updater.dispatcher

# создаем клавиатуру с кнопками для ответа
reply_keyboard = [['/checkin', '/checkout', KeyboardButton('Отправить геолокацию', request_location=True)]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# функция для обработки команды /checkin
def checkin(update, context):
    # запрашиваем у пользователя отправить фотографию и геолокацию
    update.message.reply_text("Отправь фотографию, что бы мы увидели, что ты на работе. Геолокацию отправлять пока не обязательно мы тебе доверям, но помни - мы можем попросить сделать это в любой момент", reply_markup=markup)
    # отправляем сообщение о приходе на работу в канал
    user = update.effective_user
    if user:
        context.bot.send_message(chat_id='-1001985737833', text=f"{user.username} пришел на работу")

# функция для обработки команды /checkout
def checkout(update, context):
    # запрашиваем у пользователя отправить фотографию и геолокацию
    update.message.reply_text("Отправь свою фотографию, что бы мы увидели твое счастливое лицо даже после такого рабочего дня ))", reply_markup=markup)
    # отправляем сообщение об уходе с работы в канал
    user = update.effective_user
    if user:
        context.bot.send_message(chat_id='-1001985737833', text=f"{user.username} покинул счастливым рабочее место")

# функция для обработки полученной фотографии
def handle_photo(update, context):
    # получаем фотографию и отправляем сообщение с подтверждением получения
    photo = update.message.photo[-1]
    photo_file = context.bot.get_file(photo.file_id)
    photo_file.download(f"{photo.file_id}.jpg")
    update.message.reply_text("Фотографию мы получили. Вижу ты не очень счастлив :))")
    # отправляем фотографию в канал
    context.bot.send_photo(chat_id='-1001985737833', photo=photo_file.file_id)

# функция для обработки полученной геолокации
def handle_location(update, context):
    # получаем геолокацию и отправляем сообщение с подтверждением получения
    location = update.message.location
    update.message.reply_text("Мы теперь знаем где ты находишься ))")
    # отправляем геолокацию в канал
    context.bot.send_location(chat_id='-1001985737833', latitude=location.latitude, longitude=location.longitude)

# функция для обработки ошибок
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# создаем объект updater и регистрируем обработчики команд и сообщений
updater = Updater(token='5881314782:AAEkrF5O0s7HWGJANYPtCZAboP_POZ3fRvw', use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler('checkin', checkin))
dp.add_handler(CommandHandler('checkout', checkout))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
dp.add_handler(MessageHandler(Filters.location, handle_location))
dp.add_error_handler(error)

# запускаем бота
updater.start_polling()
updater.idle()

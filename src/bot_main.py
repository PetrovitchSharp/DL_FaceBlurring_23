import configparser
import os

from aiogram import Bot, Dispatcher, executor, types

from models import DetectronBlurringModel


# Config parser
config = configparser.ConfigParser()
config.read("src/settings.ini")

# Telegram API token
TOKEN = config['Telegram']['token']

# Path to blurring model
MODEL_PATH = config['Models']['model_path']

# Path to model's config
CONFIG_PATH = config['Models']['config_path']

# Bot initialization
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

model = DetectronBlurringModel.load_model(
        CONFIG_PATH,
        MODEL_PATH)

@dispatcher.message_handler(commands='start')
async def print_start_message(message: types.Message) -> None:
    '''
    Print message on bot start

    Args:
        message: Input message
    '''
    await message.answer('\
        Добро пожаловать! Данный бот поможет вам анонимизировать ваши фото:\n\
        вам всего лишь нужно отправить любое фото боту\
        и он вернет вам фото с неразличимым лицом\n\n\
        P.s. Бот не хранит ваши фото на постоянной\
        основе и удаляет их после обработки\
    ')


@dispatcher.message_handler()
async def reply_any_message(message: types.Message) -> None:
    '''
    Print reply to non-handled messages

    Args:
        message: Input message
    '''
    await message.answer('\
        К сожалению, я не знаю такой команды.\n\
        Я умею лишь обрабатывать ваши фото))\
    ')


@dispatcher.message_handler(content_types=[types.ContentType.PHOTO])
async def blur_photo(message: types.Message) -> None:
    '''
    Blur photo from telegram message

    Args:
        message: Input message
    '''
    photo = message.photo[-1]

    await photo.download(destination_file='photos/photo.jpg')

    anonimized_path = model.blur_image('photos/photo.jpg')

    await message.answer_photo(
        photo=types.InputFile(anonimized_path),
        caption='Вот твое анонимизированное фото'
    )

    os.remove('photos/photo.jpg')
    os.remove('photos/blurred_photo.jpg')


if __name__ == '__main__':
    # Bot starting
    executor.start_polling(dispatcher, skip_updates=True)

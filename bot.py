from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Empire_of_Movies.settings')
import django
django.setup()
from users.models import CustomUser
import hashlib

from django.conf import settings
apiKey = settings.TELEGRAM_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=apiKey, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to Empire of Movies! If you want to link with your account,\
    please follow the instruction on the website!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='This is not recognized')

def login(update, context):
    args_array = ' '.join(context.args).split(' ')
    website_id = args_array[0]
    entered_otp = args_array[1]
    try:
        if (CustomUser.objects.get(username=website_id)):
            telegram_id = update.message.chat.username
            chat_id = update.message.chat.id
            if (CustomUser.objects.filter(telegram_id=telegram_id).count() > 0):
                context.bot.send_message(chat_id=update.effective_chat.id, text="You need to logout from your previous telegram by sending /logout")
            else:
                user = CustomUser.objects.get(username=website_id)
                real_otp = user.OTP
                if (real_otp == int(entered_otp)):
                    user.telegram_id = telegram_id
                    user.chat_id = chat_id
                    user.save()
                    context.bot.send_message(chat_id=update.effective_chat.id, text="You are logged in")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="You entered the wrong OTP")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You entered a wrong username")

def logout(update, context):
    telegram_id = update.message.chat.username
    if (CustomUser.objects.get(telegram_id=telegram_id)):
        user = CustomUser.objects.get(telegram_id=telegram_id)
        user.telegram_id = None
        user.chat_id = None
        user.save()
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are logged out")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not logged in")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

import requests


def telegram_bot_sendtext(chat_id, bot_message, link):

    bot_token = apiKey
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message + ' ' + link

    response = requests.get(send_text)

    return response.json()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

login_handler = CommandHandler('login', login)
dispatcher.add_handler(login_handler)

logout_handler = CommandHandler('logout', logout)
dispatcher.add_handler(logout_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

# updater.idle()
import telebot
import os
import h5py
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #конфликт с видюхой убирает ошибки
from auth_data import token #токен бота в отдельном файле
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from config import *
from functions import *
from telebot import types


def telegram_bot(token):
    bot = telebot.TeleBot(token) #создание объекта бот


    @bot.message_handler(commands=["start"])
    def start_message(message):            #чтобы мы отправляли нужному пользователю, а не случайному, текст
        bot.send_message(message.chat.id, "Привет!!!\nМеня зовут Кагуя v3.0 и я буду твоим помощником в анализе данных\nотправь /info, чтобы узнать что я умею ;)")


    @bot.message_handler(commands=["info"])
    def info(message):
        bot.send_message(message.chat.id, "вот все что я умею:\n1. photo - сегментация объектов на фото\n2. video - сегментация объектов на видео\n3. translate - считываю текст с фото и отправляю вам\n"
                                          "4. anime - поиск аниме по названию(ru/en) \n5. manga - поиск манги по названию(ru/en)\n6. Если вам хочется с кем-то погооврить, то введите команду \"talk\", чтобы узнать больше\n"
                                          "7. спасибо - Если вы хотите поблагодарить меня напишите любое сообщение со словом \"спасибо\"")

    @bot.message_handler(commands=["talk"])
    def talk(message):
        bot.send_message(message.chat.id,"Если вы хотите просто пообщаться со мной, то вы можете написать мне сообщение. Я умею понимать по контексту такие задачи как:\"время\", \"рассказать анекдот\" и \"что посмотреть\" \n\n(вам не обязательно вводить слово в слово\n\n"
                                         "Данная функция находоится в стадии разработки, поэтому может не всегда выдавать корректные значения по причине того, что работает на техналогии нечеткого сравнения fuzzywuzzy.\nВ дальнейшем я буду работать на технологии ruGPT-3 для еще более точного понимания вас и поддержки диалога даже без команд!!!\n\n"
                                         "Так же в будущем я хочу научитсья распознавать вашу речь о отвечать вам!!!\n\nС уважением Кагуя и ее разработчик @sader_went")


    @bot.message_handler(commands=["manga"])
    def manga_send(message):  # чтобы мы отправляли нужному пользователю, а не случайному, текст
        try:
            mesg = bot.send_message(message.chat.id, 'Скажи примерное название аниме, которое ты хочешь найти и я постараюсь тебе помочь или \"stop\" чтобы выйти')
            bot.register_next_step_handler(mesg, manga)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


    @bot.message_handler(commands=["anime"])
    def anime_send(message):  # чтобы мы отправляли нужному пользователю, а не случайному, текст
        try:
            mesg = bot.send_message(message.chat.id, 'Скажи примерное название аниме, которое ты хочешь найти и я постараюсь тебе помочь или \"stop\" чтобы выйти')
            bot.register_next_step_handler(mesg, anime)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


    @bot.message_handler(commands=["photo"])
    def photo_send(message):
        try:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Всё", callback_data='all')
            item2 = types.InlineKeyboardButton("Люди", callback_data='person')
            item3 = types.InlineKeyboardButton("Машины", callback_data='car')
            item4 = types.InlineKeyboardButton("Автобусы", callback_data='bus')
            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выберите категорию объектов, которые хотите найти', reply_markup=markup)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


    @bot.message_handler(commands=["video"])
    def video_send(message):
        try:
            markup1 = types.InlineKeyboardMarkup(row_width=2)

            item1 = types.InlineKeyboardButton("Всё", callback_data='allv')
            item2 = types.InlineKeyboardButton("Люди", callback_data='personv')
            item3 = types.InlineKeyboardButton("Машины", callback_data='carv')
            item4 = types.InlineKeyboardButton("Автобусы", callback_data='busv')
            markup1.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выберите категорию объектов, которые хотите найти', reply_markup=markup1)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


    @bot.message_handler(commands=["translate"])
    def translation(message):
        try:
            mesg = bot.send_message(message.chat.id, 'Отправь мне фото из которого нужно получить текст или \"stop\" чтобы выйти')
            bot.register_next_step_handler(mesg, translate)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.message:
            global cl
            if call.data == "all":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Всё\".\nОтправьте мне фото для обработки или \"stop\" чтобы выйти')
                cl = "all"
                bot.register_next_step_handler(mesg, photo, cl)

            elif call.data == "person":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Люди\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "person"
                bot.register_next_step_handler(mesg, photo, cl)

            elif call.data == "car":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Машины\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "car"
                bot.register_next_step_handler(mesg, photo, cl)

            elif call.data == "bus":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Автобусы\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "bus"
                bot.register_next_step_handler(mesg, photo, cl)

            elif call.data == "allv":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Всё\".\nОтправьте мне фото для обработки или \"stop\" чтобы выйти')
                cl = "allv"
                bot.register_next_step_handler(mesg, video, cl)

            elif call.data == "personv":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Люди\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "personv"
                bot.register_next_step_handler(mesg, video, cl)

            elif call.data == "carv":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Машины\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "carv"
                bot.register_next_step_handler(mesg, video, cl)

            elif call.data == "busv":
                mesg = bot.send_message(call.message.chat.id,'Вы выбрали категорию \"Автобусы\".\nОтправь мне фото для обработки или \"stop\" чтобы выйти')
                cl = "busv"
                bot.register_next_step_handler(mesg, video, cl)


    #####################просто ассистент просто текст##############################################################
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        book = message.text.lower()  # сообщение от пользователя

        s = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)
        accuracy = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)[0][1]  # точность

        if accuracy >= 53:
            #bot.send_message(message.chat.id, f"{s[0][-1]} {accuracy}")

            if s[0][-1] == "ctime":
                bot.send_message(message.chat.id, f"Московское время: {time()}")

            elif s[0][-1] == "joke":
                bot.send_message(message.chat.id, f" {joke()}")

            elif s[0][-1] == "watch":
                bot.send_message(message.chat.id,
                                 f"можешь тут глянуть ;) \n https://myanimelist.net/topanime.php?type=airing")

        elif book.find('спасибо') != -1:
            bot.send_message(message.chat.id,
                             "Спасибо!!! Я очень рада работать с вами!!! Давайте совершенствоваться вместе!!!")
        else:
            bot.send_message(message.chat.id,
                             f"Я... я не знаю такой команды... Проверь команды через /info") #{s[0][-1]} {accuracy}

################################################################################################################################################


    bot.polling() #постоянно спрашиваем у сервера не написал ли нам кто


if __name__ == '__main__':
    telegram_bot(token)
# -*- coding: cp1251 -*-
#файл в кодировке cp1251
import telebot
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #конфликт с видюхой убирает ошибки
from auth_data import token #токен бота в отдельном файле
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from config import *
from functions import *
from telebot import types

from transformers import GPT2LMHeadModel, GPT2Tokenizer
model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"

tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path).cpu()

def telegram_bot(token):
    while True:
        try:
            bot = telebot.TeleBot(token) #создание объекта бот

            @bot.message_handler(commands=["start"])
            def start_message(message):            #чтобы мы отправляли нужному пользователю, а не случайному, текст
                bot.send_message(message.chat.id, "Привет!!!\nМеня зовут Кагуя v4.0 и я буду твоим помощником в анализе данных\nотправь /info, чтобы узнать что я умею ;)")


            @bot.message_handler(commands=["info"])
            def info(message):
                bot.send_message(message.chat.id, "вот все что я умею:\n1. photo - сегментация объектов на фото\n2. video - сегментация объектов на видео\n3. translate - считываю текст с фото и отправляю вам\n"
                                                  "4. anime - поиск аниме по названию(ru/en) \n5. manga - поиск манги по названию(ru/en)\n6. Если вам хочется с кем-нибудь погооврить, то введите команду \"talk\", чтобы узнать больше\n")

            @bot.message_handler(commands=["talk"])
            def talk(message):
                bot.send_message(message.chat.id, "Если вы хотите просто пообщаться со мной, то вы можете написать мне сообщение. Я умею понимать по слова по контексту, говорить время и рассказывать анекдоты.\n"
                                                  "Я работаю на технологии ruGPT-3 от сбербанка модель large для более точного анализа текста.это техналогия пока не развита до максимума и находится в стадии разрботки, однако уже я могу довольно неплохо продолжать предложени, рекомендовать аниме и и вести диалго с вами"
                                                  "\nв дальнейшем моя работа будет еще точнее и лучше, поэтому следите за моими обновлениями и пишите по вопросами моего создателю @sader_went в телеграмм")


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
                    item4 = types.InlineKeyboardButton("STOP", callback_data='stop')
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
                    item4 = types.InlineKeyboardButton("STOP", callback_data='stop')
                    markup1.add(item1, item2, item3, item4)

                    bot.send_message(message.chat.id, 'Выберите категорию объектов, которые хотите найти', reply_markup=markup1)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


            @bot.message_handler(commands=["translate"])
            def translation(message):
                try:
                    mesg = bot.send_message(message.chat.id, 'Отправь мне фото из которого нужно получить текст.Постаарайстесь повернуть текст горизонтально, чтобы получить более точное распознование текста. Введите \"stop\" чтобы выйти')
                    bot.register_next_step_handler(mesg, translate)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


            @bot.callback_query_handler(func=lambda call: True)
            def callback(call):
                if call.message:
                    global cl
                    if call.data == "all":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Всё\".\nОтправьте мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "all"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "person":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Люди\".\nОтправь мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "person"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "car":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Машины\".\nОтправь мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "car"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "stop":
                        bot.send_message(call.message.chat.id, 'Ну, значит не судьба')

                    elif call.data == "allv":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Всё\".\nОтправьте мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "allv"
                        bot.register_next_step_handler(mesg, video, cl)

                    elif call.data == "personv":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Люди\".\nОтправь мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "personv"
                        bot.register_next_step_handler(mesg, video, cl)

                    elif call.data == "carv":
                        mesg = bot.send_message(call.message.chat.id, 'Вы выбрали категорию \"Машины\".\nОтправь мне фото (не в виде документа) для обработки или \"stop\" чтобы выйти')
                        cl = "carv"
                        bot.register_next_step_handler(mesg, video, cl)



            #####################просто ассистент просто текст##############################################################
            @bot.message_handler(content_types=["text"])
            def send_text(message):
                try:
                    book = message.text.lower()  # сообщение от пользователя

                    s = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)
                    accuracy = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)[0][1]  # точность

                    if accuracy >= 53:
                        # bot.send_message(message.chat.id, f"{s[0][-1]} {accuracy}")

                        if s[0][-1] == "ctime":
                            bot.send_message(message.chat.id, f"Московское время: {time()}")

                        elif s[0][-1] == "joke":
                            bot.send_message(message.chat.id, f" {joke()}")

                    #elif book.find('спасибо') != -1:
                        #bot.send_message(message.chat.id,
                                         #"Спасибо!!! Я очень рада работать с вами!!! Давайте совершенствоваться вместе!!!")
                    else:

                        input_ids = tokenizer.encode(book, return_tensors="pt").cpu()

                        out = model.generate(
                            input_ids.cpu(),
                            no_repeat_ngram_size=2,  # не более 2 повторений подряд
                            min_lenght=2,
                            max_length=60,
                            do_sample=True,  # открытие свободы генерации
                            temperature=0.8, #насколько часто алгоритм будет выдвать значения с НЕ самым высоким коэфицентом
                            num_beams=3,# на сколько шагов вперед будет просчитываться наилучший результат. ест много ресурсов, но зато текст получается более осмысленный
                            Early_stopping=True,  # если выше найден лучший путь прерыывается
                            # max_time=5.0, #время на обработку
                        )
                        generated_text = list(map(tokenizer.decode, out))[0]
                        print(list(map(tokenizer.decode, out)))
                        len_book = len(book)
                        res_str = generated_text[:0] + generated_text[len_book+1:]
                        res_one_answer = res_str[:res_str.find('<s>')]
                        print(res_one_answer)
                        bot.send_message(message.chat.id, res_one_answer)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "Ой... что-то пошло не так...")

            ################################################################################################################################################
            @bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "voice"])
            def random_response(message):  # ответ на рандомные сообщения
                bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIL2mMsRD7S3mJQmyn0PBpU1Sfd6G6iAAJ1DAACGDCqBXYpfjEye2igKQQ')
                bot.send_message(message.chat.id, 'Выглядит интересно, но я не знаю что это')

            bot.polling() #постоянно спрашиваем у сервера не написал ли нам кто


        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    telegram_bot(token)
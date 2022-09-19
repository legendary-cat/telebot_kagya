import pyjokes
from googletrans import Translator
import datetime
import telebot
import os
import h5py
import easyocr
import pixellib
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #конфликт с видюхой убирает ошибки
from pixellib.instance import instance_segmentation
from auth_data import token #токен бота в отдельном файле
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from config import *
from AnilistPython import Anilist
from googletrans import Translator
from telebot import types


bot = telebot.TeleBot(token)

def time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")


def joke():
    translator = Translator()
    joke = pyjokes.get_joke()
    joke_result = translator.translate(joke, dest='ru')
    return joke_result.text


@bot.message_handler(content_types=['text'])
def manga(message):

    tp = message.content_type

    book = message.text.lower()  # сообщение от пользователя

    if tp != 'text':
        bot.send_message(message.chat.id, "Вы ввели не верных тип данных, попробуйте снова")

    elif book == 'stop':
        bot.send_message(message.chat.id, "Значит в другой раз ")

    else:
        try:
            anilist = Anilist()
            name = message.text.lower()
            translator = Translator()
            data = translator.translate(name, dest='en').text
            try:
                manga_dict = anilist.get_manga(data)
            except Exception as ex:
                bot.send_message(message.chat.id, "К сожалению я не могу найти это аниме :(")
                return  # чтобы дальше не выполнять программу

            status = translator.translate(manga_dict.get('release_status'), dest='ru').text
            about = translator.translate(manga_dict.get('desc'), dest='ru').text
            itog = f"Манга - {manga_dict.get('name_romaji')} \n{manga_dict.get('starting_time')} - {manga_dict.get('ending_time')}\nСтатус : {status} \nОписание: {about}"
            bot.send_message(message.chat.id, itog)

        except Exception as ex:
            print(ex)
            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


@bot.message_handler(content_types=['text'])
def anime(message):
    tp = message.content_type

    book = message.text.lower()  # сообщение от пользователя

    if book == 'stop':
        bot.send_message(message.chat.id, "Значит в другой раз ")
    elif tp != 'text':
        bot.send_message(message.chat.id, "Вы ввели не верных тип данных, попробуйте снова")
    else:
        try:
            anilist = Anilist()
            name = message.text.lower()
            translator = Translator()
            data = translator.translate(name, dest='en').text
            try:
                anime_dict = anilist.get_anime(data)

            except Exception as ex:
                bot.send_message(message.chat.id, "К сожалению я не могу найти это аниме :(")
                return # чтобы дальше не выполнять программу

            status = translator.translate(anime_dict.get('airing_status'), dest='ru').text
            about = translator.translate(anime_dict.get('desc'), dest='ru').text

            itog = f"Аниме - {anime_dict.get('name_romaji')} \n{anime_dict.get('starting_time')} - {anime_dict.get('ending_time')}\nВсего {anime_dict.get('airing_episodes')} серий\nСтатус : {status} \nОписание: {about}"
            bot.send_message(message.chat.id, itog)
        except Exception as ex:
            print(ex)

            bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


@bot.message_handler(content_types=['photo', "text"])
def translate(message):

    tp = message.content_type

    if tp == 'text':
        book = message.text.lower()  # сообщение от пользователя
        if book == 'stop':
            bot.send_message(message.chat.id, "Ничего страшного, значит в другой раз")
            return
        else:
            bot.send_message(message.chat.id, "Такой функции нет, попробуйте снова")
            return

    elif tp != 'photo':
        bot.send_message(message.chat.id, "Вы ввели не верных тип данных :(")
        return

    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'files/' + file_info.file_path  # куда сохранится
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "обрабатываю...")
        ############################################################################################### обработка фото
        reader = easyocr.Reader(["ru", "en"])
        result = reader.readtext(src, detail=0, paragraph=True)
        os.remove(src)
        ################################################################отправка пользователю результатов
        for line in result:
            bot.send_message(message.chat.id, line)

    except Exception as ex:
        print(ex)
        bot.send.message(message.chat.id, "Ой... что-то пошло не так...")



@bot.message_handler(content_types=['photo', "text"])
def photo(message, cl):
    tp = message.content_type

    if tp == 'text':
        book = message.text.lower()  # сообщение от пользователя
        if book == 'stop':
            bot.send_message(message.chat.id, "Ничего страшного, значит в другой раз")
            return
        else:
            bot.send_message(message.chat.id, "Такой функции нет, попробуйте снова")
            return

    elif tp != 'photo':
        bot.send_message(message.chat.id, "Вы ввели не верных тип данных :(")
        return

    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'files/' + file_info.file_path #куда сохранится
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "обрабатываю...")
        ############################################################################################### обработка фото
        segment_image = instance_segmentation()  # создаем объект класса
        segment_image.load_model("E:\www\mask_rcnn_coco.h5")

        target_classes = segment_image.select_target_classes()
        if cl == "person":
            target_classes = segment_image.select_target_classes(person=True)  # выбираем только конкретные типы объектов

        elif cl == "car":
            target_classes = segment_image.select_target_classes(car=True)  # выбираем только конкретные типы объектов

        elif cl == "bus":
            target_classes = segment_image.select_target_classes(bus=True)  # выбираем только конкретные типы объектов

        output_file = 'end/' + file_info.file_path

        if cl != "all":
            result = segment_image.segmentImage(
                image_path=src,
                output_image_name=output_file,
                segment_target_classes=target_classes,
                show_bboxes=True  # квадрат вокруг модели
            )
        else:
            result = segment_image.segmentImage(
                image_path=src,
                output_image_name=output_file,
                show_bboxes=True  # квадрат вокруг модели
            )

        new_file.close()
        os.remove(src)#удаляю обработанный файл
        # print(result[0]["scores"])
        object_count = len(result[0]["scores"])#информация в консоли для себя
        print(f"найдено объектов заданного типа: {object_count} ")
        ################################################################отправка пользователю результатов

        img = open(output_file, 'rb')
        bot.send_photo(message.chat.id, img, caption=f"найдено всего {object_count} объектов(ов)")
        img.close()
        os.remove(output_file)
        bot.send_message(message.chat.id, 'готова слушать вас ;)')

    except Exception as ex:
        print(ex)
        bot.send.message(message.chat.id, "Ой... что-то пошло не так...")


@bot.message_handler(content_types=['video', "text"])
def video(message, cl):

    tp = message.content_type

    if tp == 'text':
        book = message.text.lower()  # сообщение от пользователя
        if book == 'stop':
            bot.send_message(message.chat.id, "Ничего страшного, значит в другой раз")
            return
        else:
            bot.send_message(message.chat.id, "Такой функции нет, попробуйте снова")
            return

    elif tp != 'video':
        bot.send_message(message.chat.id, "Вы ввели не верных тип данных :(")
        return

    try:
        file_info = bot.get_file(message.video.file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        src ='files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Это может занять какое-то время. можешь пока сходить за чайком ;)")
        ############################################################################################### обработка видео

        output_file = 'end/' + file_info.file_path

        segment_video = instance_segmentation()
        segment_video.load_model("mask_rcnn_coco.h5")

        target_classes = segment_video.select_target_classes()

        if cl == "personv":
            target_classes = segment_video.select_target_classes(person=True)  # выбираем только конкретные типы объектов

        elif cl == "carv":
            target_classes = segment_video.select_target_classes(car=True)  # выбираем только конкретные типы объектов

        elif cl == "busv":
            target_classes = segment_video.select_target_classes(bus=True)  # выбираем только конкретные типы объектов

        output_file = 'end/' + file_info.file_path

        if cl != "allv":
            result = segment_video.process_video(
                src,
                frames_per_second=10,  # fps
                show_bboxes=True,
                segment_target_classes=target_classes,
                output_video_name=output_file
            )
        else:
            result = segment_video.process_video(
                src,
                frames_per_second=10,  # fps
                show_bboxes=True,
                output_video_name=output_file)

        new_file.close()
        os.remove(src)  # удаляю обработанный файл
        ################################################################отправка пользователю результатов
        object_count = len(result[0]["scores"])  # информация в консоли для себя
        print(f"найдено объектов заданного типа: {object_count} ")

        video = open(output_file, 'rb')

        bot.send_video(message.chat.id, video)

        bot.send_message(message.chat.id, 'подождите пару секунд...')
        video.close()
        os.remove(output_file)
        bot.send_message(message.chat.id, 'готова слушать вас ;)')

    except Exception as ex:
        print(ex)
        bot.send.message(message.chat.id, "Ой... что-то пошло не так...")

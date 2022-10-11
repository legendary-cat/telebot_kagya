# -*- coding: cp1251 -*-
#���� � ��������� cp1251
import telebot
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #�������� � ������� ������� ������
from auth_data import token #����� ���� � ��������� �����
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
            bot = telebot.TeleBot(token) #�������� ������� ���

            @bot.message_handler(commands=["start"])
            def start_message(message):            #����� �� ���������� ������� ������������, � �� ����������, �����
                bot.send_message(message.chat.id, "������!!!\n���� ����� ����� v4.0 � � ���� ����� ���������� � ������� ������\n������� /info, ����� ������ ��� � ���� ;)")


            @bot.message_handler(commands=["info"])
            def info(message):
                bot.send_message(message.chat.id, "��� ��� ��� � ����:\n1. photo - ����������� �������� �� ����\n2. video - ����������� �������� �� �����\n3. translate - �������� ����� � ���� � ��������� ���\n"
                                                  "4. anime - ����� ����� �� ��������(ru/en) \n5. manga - ����� ����� �� ��������(ru/en)\n6. ���� ��� ������� � ���-������ ����������, �� ������� ������� \"talk\", ����� ������ ������\n")

            @bot.message_handler(commands=["talk"])
            def talk(message):
                bot.send_message(message.chat.id, "���� �� ������ ������ ���������� �� ����, �� �� ������ �������� ��� ���������. � ���� �������� �� ����� �� ���������, �������� ����� � ������������ ��������.\n"
                                                  "� ������� �� ���������� ruGPT-3 �� ��������� ������ large ��� ����� ������� ������� ������.��� ���������� ���� �� ������� �� ��������� � ��������� � ������ ���������, ������ ��� � ���� �������� ������� ���������� ����������, ������������� ����� � � ����� ������ � ����"
                                                  "\n� ���������� ��� ������ ����� ��� ������ � �����, ������� ������� �� ����� ������������ � ������ �� ��������� ����� ��������� @sader_went � ���������")


            @bot.message_handler(commands=["manga"])
            def manga_send(message):  # ����� �� ���������� ������� ������������, � �� ����������, �����
                try:
                    mesg = bot.send_message(message.chat.id, '����� ��������� �������� �����, ������� �� ������ ����� � � ���������� ���� ������ ��� \"stop\" ����� �����')
                    bot.register_next_step_handler(mesg, manga)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")


            @bot.message_handler(commands=["anime"])
            def anime_send(message):  # ����� �� ���������� ������� ������������, � �� ����������, �����
                try:
                    mesg = bot.send_message(message.chat.id, '����� ��������� �������� �����, ������� �� ������ ����� � � ���������� ���� ������ ��� \"stop\" ����� �����')
                    bot.register_next_step_handler(mesg, anime)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")


            @bot.message_handler(commands=["photo"])
            def photo_send(message):
                try:
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("��", callback_data='all')
                    item2 = types.InlineKeyboardButton("����", callback_data='person')
                    item3 = types.InlineKeyboardButton("������", callback_data='car')
                    item4 = types.InlineKeyboardButton("STOP", callback_data='stop')
                    markup.add(item1, item2, item3, item4)

                    bot.send_message(message.chat.id, '�������� ��������� ��������, ������� ������ �����', reply_markup=markup)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")


            @bot.message_handler(commands=["video"])
            def video_send(message):
                try:
                    markup1 = types.InlineKeyboardMarkup(row_width=2)

                    item1 = types.InlineKeyboardButton("��", callback_data='allv')
                    item2 = types.InlineKeyboardButton("����", callback_data='personv')
                    item3 = types.InlineKeyboardButton("������", callback_data='carv')
                    item4 = types.InlineKeyboardButton("STOP", callback_data='stop')
                    markup1.add(item1, item2, item3, item4)

                    bot.send_message(message.chat.id, '�������� ��������� ��������, ������� ������ �����', reply_markup=markup1)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")


            @bot.message_handler(commands=["translate"])
            def translation(message):
                try:
                    mesg = bot.send_message(message.chat.id, '������� ��� ���� �� �������� ����� �������� �����.�������������� ��������� ����� �������������, ����� �������� ����� ������ ������������� ������. ������� \"stop\" ����� �����')
                    bot.register_next_step_handler(mesg, translate)

                except Exception as ex:
                    print(ex)
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")


            @bot.callback_query_handler(func=lambda call: True)
            def callback(call):
                if call.message:
                    global cl
                    if call.data == "all":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"��\".\n��������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "all"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "person":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"����\".\n������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "person"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "car":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"������\".\n������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "car"
                        bot.register_next_step_handler(mesg, photo, cl)

                    elif call.data == "stop":
                        bot.send_message(call.message.chat.id, '��, ������ �� ������')

                    elif call.data == "allv":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"��\".\n��������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "allv"
                        bot.register_next_step_handler(mesg, video, cl)

                    elif call.data == "personv":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"����\".\n������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "personv"
                        bot.register_next_step_handler(mesg, video, cl)

                    elif call.data == "carv":
                        mesg = bot.send_message(call.message.chat.id, '�� ������� ��������� \"������\".\n������� ��� ���� (�� � ���� ���������) ��� ��������� ��� \"stop\" ����� �����')
                        cl = "carv"
                        bot.register_next_step_handler(mesg, video, cl)



            #####################������ ��������� ������ �����##############################################################
            @bot.message_handler(content_types=["text"])
            def send_text(message):
                try:
                    book = message.text.lower()  # ��������� �� ������������

                    s = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)
                    accuracy = process.extract(book, VA_CMD_LIST, limit=3, scorer=fuzz.token_set_ratio)[0][1]  # ��������

                    if accuracy >= 53:
                        # bot.send_message(message.chat.id, f"{s[0][-1]} {accuracy}")

                        if s[0][-1] == "ctime":
                            bot.send_message(message.chat.id, f"���������� �����: {time()}")

                        elif s[0][-1] == "joke":
                            bot.send_message(message.chat.id, f" {joke()}")

                    #elif book.find('�������') != -1:
                        #bot.send_message(message.chat.id,
                                         #"�������!!! � ����� ���� �������� � ����!!! ������� ������������������ ������!!!")
                    else:

                        input_ids = tokenizer.encode(book, return_tensors="pt").cpu()

                        out = model.generate(
                            input_ids.cpu(),
                            no_repeat_ngram_size=2,  # �� ����� 2 ���������� ������
                            min_lenght=2,
                            max_length=60,
                            do_sample=True,  # �������� ������� ���������
                            temperature=0.8, #��������� ����� �������� ����� ������� �������� � �� ����� ������� �����������
                            num_beams=3,# �� ������� ����� ������ ����� �������������� ��������� ���������. ��� ����� ��������, �� ���� ����� ���������� ����� �����������
                            Early_stopping=True,  # ���� ���� ������ ������ ���� ������������
                            # max_time=5.0, #����� �� ���������
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
                    bot.send.message(message.chat.id, "��... ���-�� ����� �� ���...")

            ################################################################################################################################################
            @bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "voice"])
            def random_response(message):  # ����� �� ��������� ���������
                bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIL2mMsRD7S3mJQmyn0PBpU1Sfd6G6iAAJ1DAACGDCqBXYpfjEye2igKQQ')
                bot.send_message(message.chat.id, '�������� ���������, �� � �� ���� ��� ���')

            bot.polling() #��������� ���������� � ������� �� ������� �� ��� ���


        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    telegram_bot(token)
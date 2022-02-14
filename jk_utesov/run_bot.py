import os

from telebot import TeleBot, types
import telebot
from datetime import datetime

os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"

import django
django.setup()

from apartments.models import Resident, Apartment
from passes.models import PassCars, PassPeople
from registration.models import ResidentRequest


TOKEN = '1955357191:AAGQfa6eUqn1RrIRpsST2JW6AMELJIfyN-o'
DB_URL = "postgresql://apartadmin:1234509876@localhost:5432/postgres"

bot = TeleBot(TOKEN)

now = datetime.now()

keyboard_pass = types.InlineKeyboardMarkup()
button_pass_guest = types.InlineKeyboardButton("Пропуск на гостя", callback_data='guest')
button_pass_car = types.InlineKeyboardButton("Пропуск на автомобиль", callback_data='auto')
keyboard_pass.add(button_pass_guest, button_pass_car)

keyboard_yes_no = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
keyboard_yes_no.row('Да', 'Нет')

keyboard_guest = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
keyboard_guest.row('Курьер')

hideBoard = types.ReplyKeyboardRemove()


def send_message(chat_id, text):
    bot.send_message(chat_id, text, reply_markup=keyboard_pass)


@bot.message_handler(content_types=['text'])
def start_message(message):
    try:
        result = Resident.objects.get(chat_id=message.chat.id)
    except:
        try:
            result = ResidentRequest.objects.get(chat_id=message.chat.id)
            bot.send_message(message.chat.id, 'Ваша заявка на регистрацию пока не рассмотрена. '
                                                  'Дождитесь уведомления о регистрации.')
        except:
            bot.send_message(message.chat.id, 'Для начала давайте зарегистрируемся')
            bot.send_message(message.chat.id, 'Введите ваше имя')
            bot.register_next_step_handler(message, registration_name)
    else:
        bot.send_message(message.chat.id, 'Какой пропуск вам требуется?', reply_markup=keyboard_pass)


@bot.callback_query_handler(func=lambda call: call.data in ['auto', 'guest'])
def callback_pass(call):
    number_apartment = Resident.objects.get(chat_id=call.message.chat.id).number_apartment_id
    if call.message:
        if call.data == 'auto':
            bot.send_message(call.message.chat.id, 'Введите марку ожидаемого автомобиля')
            bot.register_next_step_handler(call.message, get_number_car, number_apartment)
    if call.message:
        if call.data == 'guest':
            bot.send_message(call.message.chat.id, 'Введите имя ожидаемого гостя или нажмите на кнопку "курьер"',
                             reply_markup=keyboard_guest)
            bot.register_next_step_handler(call.message, get_name_guest, number_apartment)


@bot.message_handler(commands=['get_pass_car'])
def get_number_car(message, number_apartment):
    model_car = message.text
    bot.send_message(message.chat.id, text="Введите номер ожидаемого автомобиля в виде трех цифр")
    bot.register_next_step_handler(message, get_exam_car, number_apartment, model_car)


def get_exam_car(message, number_apartment, model_car):
    number_car = message.text
    bot.reply_to(message, text=f"Автомобиль: {model_car} Номер: {number_car}. Все верно?", reply_markup=keyboard_yes_no)
    bot.register_next_step_handler(message, get_pass_car, number_apartment, model_car, number_car)


def get_pass_car(message, number_apartment, model_car, number_car):
    if message.text.lower() == 'да':
        PassCars.objects.create(model_car=model_car,
                                number_car=number_car,
                                number_apartment=Apartment.objects.get(pk=number_apartment))
        bot.send_message(message.chat.id, text=f"Заявка отправлена")
        bot.send_message(message.chat.id, text='Какой пропуск вам требуется?', reply_markup=keyboard_pass)
    else:
        bot.reply_to(message, text=f"Ладно,  в другой раз кто-нибудь приедет")
        bot.send_message(message, text='Какой пропуск вам требуется?', reply_markup=keyboard_pass)


@bot.message_handler(commands=['get_pass_guest'])
def get_name_guest(message, number_apartment):
    if message.text == 'Курьер':
        name_guest = message.text
        bot.send_message(message.chat.id, text=f"Пропуск для курьера. Все верно?",
                         reply_markup=keyboard_yes_no)
    else:
        name_guest = message.text
        bot.send_message(message.chat.id, text=f"Пропуск на имя: {name_guest}. Все верно?", reply_markup=keyboard_yes_no)
    bot.register_next_step_handler(message, get_pass_guest, number_apartment, name_guest)


def get_pass_guest(message, number_apartment, name_guest):
    if message.text.lower() == 'да':
        PassPeople.objects.create(number_apartment=Apartment.objects.get(pk=number_apartment),
                                  name_of_guest=name_guest)
        bot.send_message(message.chat.id, text=f"Заявка отправлена")
        bot.send_message(message.chat.id, text='Какой пропуск вам требуется?', reply_markup=keyboard_pass)
    else:
        bot.reply_to(message, text=f"Ладно, в другой раз кого-нибудь пригласите", reply_markup=keyboard_pass)


@bot.message_handler(commands=['registration'])
def registration_name(message):
    reg_name = message.text
    bot.send_message(message.chat.id, text="Введите вашу фамилию")
    bot.register_next_step_handler(message, registration_surname, reg_name)


def registration_surname(message, reg_name):
    reg_surname = message.text
    bot.send_message(message.chat.id, text="Введите номер вашей квартиры")
    bot.register_next_step_handler(message, registration_appart, reg_name, reg_surname)


def registration_appart(message, reg_name, reg_surname):
    reg_app = message.text
    bot.send_message(message.chat.id, text="Введите номер телефона в 10-значном формате без знаков препинания")
    bot.register_next_step_handler(message, registration_phone, reg_name, reg_surname, reg_app)


def registration_phone(message, reg_name, reg_surname, reg_app):
    reg_phone = message.text
    bot.reply_to(message,
                 text=f"Имя: {reg_name} Фамилия: {reg_surname} "
                      f"Номер квартиры: {reg_app} "
                      f"Номер телефона: +7 {reg_phone[:3]} {reg_phone[3:6]} {reg_phone[6:8]} {reg_phone[8:]}. "
                      f"Все верно?", reply_markup=keyboard_yes_no)
    bot.register_next_step_handler(message, registration_final, reg_name, reg_surname, reg_app, reg_phone)


def registration_final(message, reg_name, reg_surname, reg_app, reg_phone):
    if message.text.lower() == 'да':
        ResidentRequest.objects.create(name=reg_name,
                                       surname=reg_surname,
                                       number_apartment=reg_app,
                                       contact=reg_phone,
                                       chat_id=message.chat.id)
        bot.reply_to(message, text=f"Заявка отправлена. Об обработке заявке будет сообщено дополнительно")
    else:
        bot.reply_to(message, text=f"Ладно, ничего записывать не буду")


if __name__ == '__main__':
    bot.polling(none_stop=True)



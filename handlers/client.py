from aiogram import types, Dispatcher
from create_bot import bot, ADMINS, e_mail, e_pass, adress_to, abonent
import smtplib
from datetime import datetime
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext

from keyboards.client_kb import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Data_statesGroup(StatesGroup):
    cold_water = State()
    hot_water = State()
    e_day = State()
    e_night = State()


async def start_command_client(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет, {message.from_user.first_name}!\n'
                             f'Я бот для отправки показаний счетчиков в управляющую компанию.',
                             reply_markup=get_enter_data()
                             )
        await message.delete()


async def enter_data_command(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Холодная вода:',
                             reply_markup=get_send_data()
                             )
        await Data_statesGroup.cold_water.set()
        await message.delete()


async def cold_water(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id

        await message.reply("Горячая вода:")
        await Data_statesGroup.next()


async def send_e_mail_message(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        mgs = MIMEMultipart()
        mgs['From'] = e_mail
        mgs['To'] = adress_to
        mgs['Subject'] = f'Абонент: {abonent}. Показания за {datetime.now().month} месяц.'
        body = (f'Горячая вода: \n'
                f'Холодная вода\n'
                f'Электричество день:\n'
                f'Электричество ночь:')
        mgs.attach(MIMEText(body, 'plain'))
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.starttls()
        smtpObj.login(e_mail, e_pass)
        smtpObj.send_message(mgs)
        smtpObj.quit()
        await message.answer('Показания отправлены!')
        await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])
    dp.register_message_handler(enter_data_command, commands=['ввести_показания'])
    dp.register_message_handler(send_e_mail_message, commands=['отправить_показания'])

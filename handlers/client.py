from aiogram import types, Dispatcher
from create_bot import bot, ADMINS, e_mail, e_pass, adress_to, abonent
import smtplib
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext

from keyboards.client_kb import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

months = ['январь', 'февраль', 'март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь']

class Data_statesGroup(StatesGroup):
    month = State()
    cold_water = State()
    hot_water = State()
    e_day = State()
    e_night = State()
    finish = State()


async def start_command_client(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f"Привет, {message.from_user.first_name}!\n"
                             f"Я бот для отправки показаний счетчиков в управляющую компанию.")

        await message.answer("Для ввода показаний нажми /enter_data",
                             reply_markup=get_enter_data())
        await message.delete()


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        if state is None:
            return
        await message.reply("Действие отменено!",
                            reply_markup=get_enter_data())

        await state.finish()


async def enter_data_command(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f"Месяц:",
                             reply_markup=get_cancel()
                             )
        await Data_statesGroup.month.set()
        await message.delete()


async def enter_month(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['month'] = message.text
        await message.answer("Горячая вода:")
        await Data_statesGroup.next()

async def cheack_month(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        if not message.text.isalpha() or message.text.lower() not in months:
            await message.reply("Это не месяц!")

async def cold_water(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['cold_water'] = message.text

        await message.answer("Холодная вода:")
        await Data_statesGroup.next()


async def hot_water(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['hot_water'] = message.text

        await message.answer("Электричество день:")
        await Data_statesGroup.next()


async def electricity_day(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['electricity_day'] = message.text

        await message.answer("Электричество ночь:")
        await Data_statesGroup.next()


async def electricity_night(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['electricity_night'] = message.text
            data['body'] = f"Горячая вода: {data['cold_water']}\n" \
                           f"Холодная вода: {data['hot_water']}\n" \
                           f"Электричество день: {data['electricity_day']}\n" \
                           f"Электричество ночь: {data['electricity_night']}"
    await message.answer(f"{data['body']}\n"
                        f"Для отправки нажми /send_message",
                        reply_markup=get_send_data())
    await Data_statesGroup.next()


async def send_e_mail_message(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            print(data['month'])
            mgs = MIMEMultipart()
            mgs['From'] = e_mail
            mgs['To'] = adress_to
            mgs['Subject'] = f"Абонент: {abonent}. Показания за {data['month']}."
            body = data['body']
            mgs.attach(MIMEText(body, 'plain'))
            smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
            smtpObj.starttls()
            smtpObj.login(e_mail, e_pass)
            smtpObj.send_message(mgs)
            smtpObj.quit()
            await message.answer('Показания отправлены!',
                                 reply_markup=get_enter_data())
            await message.delete()
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])
    dp.register_message_handler(cancel_command, commands=['cancel'], state="*")
    dp.register_message_handler(enter_data_command, commands=['enter_data'])
    dp.register_message_handler(enter_month, state=Data_statesGroup.month)
    dp.register_message_handler(cheack_month, state=Data_statesGroup.month)
    dp.register_message_handler(cold_water, state=Data_statesGroup.cold_water)
    dp.register_message_handler(hot_water, state=Data_statesGroup.hot_water)
    dp.register_message_handler(electricity_day, state=Data_statesGroup.e_day)
    dp.register_message_handler(electricity_night, state=Data_statesGroup.e_night)
    dp.register_message_handler(send_e_mail_message, commands=['send_message'], state=Data_statesGroup.finish)

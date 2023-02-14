from aiogram import types, Dispatcher
from create_bot import bot, ADMINS, e_mail, e_pass
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def start_command_client(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет, {message.from_user.first_name}!',
                             )
        await message.delete()


async def send_e_mail_message(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        addr_from = e_mail
        addr_to = 'nikitakaravaev@mail.ru'
        mgs = MIMEMultipart()
        mgs['From'] = addr_from
        mgs['To'] = addr_to
        mgs['Subject'] = 'Тест_Тема'
        body = (f'Тест_содержание')
        mgs.attach(MIMEText(body, 'plain'))
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.starttls()
        smtpObj.login(addr_from, e_pass)
        smtpObj.send_message(mgs)
        smtpObj.quit()
        await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])
    dp.register_message_handler(send_e_mail_message, commands=['send_e_mail_message'])

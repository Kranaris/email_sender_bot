from aiogram import Bot, Dispatcher
from config import load_config
from aiogram.contrib.fsm_storage.memory import MemoryStorage



config = load_config('.env')
bot_token = config.tg_bot.token
ADMINS = config.tg_bot.admin_ids
e_mail = config.tg_bot.e_mail
e_pass = config.tg_bot.e_pass
adress_to = config.tg_bot.adress_to
abonent = config.tg_bot.abonent

storage = MemoryStorage()
bot = Bot(bot_token)
dp = Dispatcher(bot, storage=storage)
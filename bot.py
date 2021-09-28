from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

urgent_list = []
temporary_list = []
longterm_list = []

name_shop = ""
type_shop = ""
name = ""

btn_add = KeyboardButton("add shop")
start_menu = ReplyKeyboardMarkup().add(btn_add)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id,'Hello',reply_markup=start_menu)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Цей бот буде показувати список покупок,які потрібно купити їх є три види:\n\n1 Термінові\n2 Тимчасові\n3 Довгосрочні")

@dp.message_handler(commands=['add_shop'])
async def help_command(message: types.Message):
    await message.reply("name shop")


@dp.message_handler()
async def echo_message(msg: types.Message):
	global name
	if not name:
		name = msg.text
		print(name)
	if not name_shop:
		name_shop = msg.text
		print(name)
	if not type_shop:
		type_shop = msg.text
		print(name)
    #await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)
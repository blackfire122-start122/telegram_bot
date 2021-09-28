from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import markup as nav

import mysql.connector

db = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "tytpassword",
	port="3306",
	database="shop_list",
)

cursor = db.cursor()
# cursor.execute("CREATE DATABASE shop_list")
# cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), user_id INT UNIQUE)")


# sql = "FROM users SELECT "
# cursor.execute(sql)
# db.commit()
# print(cursor.rowcount)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

urgent_list = []
temporary_list = []
longterm_list = []

type_shop_to_ask = False
name_to_ask = False
name_shop_ask = False

type_shop = ""
name = ""

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	global name_to_ask
	if not name_to_ask:
		await bot.send_message(message.from_user.id,'Привіт твоє імя')
		name_to_ask = True

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
	await message.reply("Цей бот буде показувати список покупок, які\
		потрібно купити їх є три види:\n\n1 Термінові - urgent\n2 Тимчасові-temporary_list\n3 Довгосрочні-longterm_list")

@dp.message_handler(commands=['shop'])
async def help_command(message: types.Message):
	global shop_to_ask
	await bot.send_message(message.from_user.id,"what shop",reply_markup=nav.shop_menu)

@dp.message_handler()
async def echo_message(msg: types.Message):
	global name
	global name_to_ask,type_shop_to_ask,name_shop_ask
	global name_shop,type_shop
	if name_to_ask and not name:
		name = msg.text

		sql = "INSERT INTO users (username,user_id) VALUES('" + name + "', " + str(msg.from_user.id) + ")"
		cursor.execute(sql)
		db.commit()
		await bot.send_message(msg.from_user.id,'реєстрація пройшла успішно')

		print("new user",name)

	elif msg.text == "add shop":
		type_shop_to_ask = True
		await bot.send_message(msg.from_user.id,"тип покупки",reply_markup=nav.shop_type)
	
	elif msg.text == "wath all shop":
			all_shop = "urgent\n\t•"+"\n\t•".join(urgent_list)+"\ntemporary\n\t•"+"\n\t•".join(temporary_list)+"\nlong-term\n\t•"+"\n\t•".join(longterm_list)
			await bot.send_message(msg.from_user.id,all_shop)

	elif msg.text == "wath urgent shop":
			all_shop = "urgent\n\t•"+"\n\t•".join(urgent_list)
			await bot.send_message(msg.from_user.id,all_shop)

	elif msg.text == "wath temporary shop":
			all_shop = "temporary\n\t•"+"\n\t•".join(temporary_list)
			await bot.send_message(msg.from_user.id,all_shop)

	elif msg.text == "wath long-term shop":
			all_shop = "long-term\n\t•"+"\n\t•".join(longterm_list)
			await bot.send_message(msg.from_user.id,all_shop)

	elif type_shop_to_ask:
		type_shop = msg.text
		type_shop_to_ask = False
		name_shop_ask = True
		await bot.send_message(msg.from_user.id,"покупка")


	elif name_shop_ask:
		if type_shop =="urgent":
			urgent_list.append(msg.text+" -- "+name)
		elif type_shop=="temporary":
			temporary_list.append(msg.text+name)
		elif type_shop=="long-term":
			longterm_list.append(msg.text+name)
		else:
			pass
		name_shop_ask = False
		print("new shop",name,type_shop)
		await bot.send_message(msg.from_user.id,"покупку " + msg.text + " додано як " + type_shop + "")

if __name__ == '__main__':
	executor.start_polling(dp)

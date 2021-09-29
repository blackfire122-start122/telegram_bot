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

cursor = db.cursor(buffered=True)

# cursor.execute("CREATE DATABASE shop_list")
# cursor.execute("CREATE TABLE urgent_shop (urgent_shop VARCHAR(255), username VARCHAR(255))")
# cursor.execute("CREATE TABLE temporary_shop (temporary_shop VARCHAR(255), username VARCHAR(255))")
# cursor.execute("CREATE TABLE longterm_shop (longterm_shop VARCHAR(255), username VARCHAR(255))")

# sql = "TRUNCATE TABLE users"
# cursor.execute(sql)
# db.commit()

# sql = "TRUNCATE TABLE urgent_shop"
# cursor.execute(sql)
# db.commit()

# sql = "TRUNCATE TABLE temporary_shop"
# cursor.execute(sql)
# db.commit()

# sql = "TRUNCATE TABLE longterm_shop"
# cursor.execute(sql)
# db.commit()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

type_shop_to_ask = False
name_to_ask = False
name_shop_ask = False
delete_shop_to_ask = False
name_delete_shop_to_ask = False

send_mes_shop_add = True
type_shop = ""
name = ""

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	global name, name_to_ask
	try:
		sql = "SELECT * FROM users WHERE user_id = " + str(message.from_user.id) + ";"
		cursor.execute(sql)
		db.commit()
	except:
		pass
	data_req = cursor.fetchone()
	if not data_req:
		id = 0
	else:
		id = data_req[2]
	if not name_to_ask and id !=message.from_user.id:
		await bot.send_message(message.from_user.id,'Привіт твоє імя')
		name_to_ask = True
	else:
		name = data_req[1]
		await bot.send_message(message.from_user.id,'Ви вже зареєстровані як '+name, reply_markup=nav.shop_menu)
		
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
	global name_to_ask,type_shop_to_ask,name_shop_ask,delete_shop_to_ask,name_delete_shop_to_ask
	global name_shop,type_shop,send_mes_shop_add
	if name_to_ask and not name:
		name = msg.text
		try:
			sql = "INSERT INTO users (username,user_id) VALUES('" + name + "', " + str(msg.from_user.id) + ")"
			cursor.execute(sql)
			db.commit()
			await bot.send_message(msg.from_user.id,'Реєстрація пройшла успішно',reply_markup=nav.shop_menu)
		except:
			await bot.send_message(msg.from_user.id,'Ви вже зареєстровані',reply_markup=nav.shop_menu)
		print("new user",name)
	elif not name:
		await bot.send_message(msg.from_user.id,'Зареєструйтесь',reply_markup=nav.btn_start_main)

	elif msg.text == "add shop":
		type_shop_to_ask = True
		await bot.send_message(msg.from_user.id,"тип покупки",reply_markup=nav.shop_type)
	
	elif msg.text == "delete shop":
		delete_shop_to_ask = True
		await bot.send_message(msg.from_user.id,"тип видаляємої покупки",reply_markup=nav.shop_type)
	
	elif msg.text == "wath all shop":
		try:
			sql = "SELECT * FROM urgent_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		all_shop = "urgent\n"
		for i in data_req:
			all_shop+='\t• '+i[0]+'--'+i[1]+"\n"
		try:
			sql = "SELECT * FROM temporary_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		all_shop += "temporary\n"
		for i in data_req:
			all_shop+='\t• '+i[0]+'--'+i[1]+"\n"
		try:
			sql = "SELECT * FROM longterm_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		all_shop += "longterm\n"
		for i in data_req:
			all_shop+='\t• '+i[0]+'--'+i[1]+"\n"

		await bot.send_message(msg.from_user.id,all_shop)

	elif msg.text == "wath urgent shop":
		try:
			sql = "SELECT * FROM urgent_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		urgent_shop = "urgent\n"
		for i in data_req:
			urgent_shop+='\t• '+i[0]+'--'+i[1]+"\n"
		await bot.send_message(msg.from_user.id,urgent_shop)

	elif msg.text == "wath temporary shop":
		try:
			sql = "SELECT * FROM temporary_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		temporary_shop = "temporary\n"
		for i in data_req:
			temporary_shop+='\t• '+i[0]+'--'+i[1]+"\n"
		await bot.send_message(msg.from_user.id,temporary_shop)

	elif msg.text == "wath long-term shop":
		try:
			sql = "SELECT * FROM longterm_shop;"
			cursor.execute(sql)
			db.commit()
			data_req = cursor.fetchall()
		except:
			pass
		longterm_shop = "longterm\n"
		for i in data_req:
			longterm_shop+='\t• '+i[0]+'--'+i[1]+"\n"
		await bot.send_message(msg.from_user.id,longterm_shop)

	elif type_shop_to_ask:
		type_shop = msg.text
		type_shop_to_ask = False
		name_shop_ask = True
		await bot.send_message(msg.from_user.id,"Імя покупки")

	elif delete_shop_to_ask:
		delete_shop_to_ask = False
		name_delete_shop_to_ask = True
		type_shop = msg.text
		await bot.send_message(msg.from_user.id,"Імя видаляємої покупки")

	elif name_shop_ask:
		send_mes_shop_add = True
		try:
			sql = "INSERT INTO "+type_shop+"_shop ("+type_shop+"_shop,username) VALUES('" + msg.text + "', '" + name + "')"
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print(e)
			await bot.send_message(msg.from_user.id,"Покупку " + msg.text + "не додано помилка")
			send_mes_shop_add = False
		name_shop_ask = False
		if send_mes_shop_add:
			print("new shop",msg.text,name,type_shop)
			await bot.send_message(msg.from_user.id,"Покупку " + msg.text + " додано як " + type_shop + "",reply_markup=nav.shop_menu)

	elif name_delete_shop_to_ask:
		name_delete_shop_to_ask = False
		try:
			sql = "DELETE FROM "+type_shop+"_shop WHERE "+type_shop+"_shop = '"+msg.text+"'"
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print(e)
			await bot.send_message(msg.from_user.id,"Покупку " + msg.text + "не видалено помилка")
			send_mes_shop_add = False
		if cursor.rowcount:
			print("Покупку " + msg.text + " видалено" + name)
			await bot.send_message(msg.from_user.id,"Покупку " + msg.text + " видалено ", reply_markup=nav.shop_menu)
		else:
			await bot.send_message(msg.from_user.id,"Покупку " + msg.text + " не знайдено ", reply_markup=nav.shop_menu)

if __name__ == '__main__':
	executor.start_polling(dp)
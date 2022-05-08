from aiogram import Bot, Dispatcher, executor, types
from config import *
from db import *
from markup import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

def login_required(user):
	return True if User.get(name=user.first_name,telegram_id=user.id) else False

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
	user = types.User.get_current()
	if not login_required(user):User(name=user.first_name,telegram_id=user.id).save()
	await message.answer(Welcome,reply_markup=show_add_delete_kb)

@dp.message_handler(commands='help')
async def help(message: types.Message):
	user = types.User.get_current()
	if not login_required(user):
		await message.answer(Not_login)
		return
	await message.answer(Help)

@dp.message_handler(state=['GetName:'+i for i in add_types_shop.values()])
async def add_shop(message: types.Message,state: FSMContext):
	user = types.User.get_current()
	if not login_required(user):
		await message.answer(Not_login)
		return

	state_type = await state.get_state()
	state_type = state_type.split(":")[1]

	type_s = Type.get(type=state_type)[0][0]
	Shop(name=message.text,type=type_s,user=user.id).save()

	await state.finish()
	await message.answer("Added "+message.text+" "+state_type)

@dp.message_handler(state='DeleteShop')
async def add_shop(message: types.Message,state: FSMContext):
	user = types.User.get_current()
	if not login_required(user):
		await message.answer(Not_login)
		return

	if Shop.get(name=message.text):
		Shop.delete(name=message.text)

		await state.finish()
		await message.answer("Deleted "+message.text,reply_markup=show_add_delete_kb)
	else:
		await state.finish()
		await message.answer("There is no such purchase: "+message.text,reply_markup=show_add_delete_kb)


@dp.message_handler()
async def Messages(message: types.Message,state: FSMContext):
	user = types.User.get_current()
	if not login_required(user):
		await message.answer(Not_login)
		return

	if message.text in add_types_shop.keys():
		await message.answer(Get_name_shop)
		await state.set_state('GetName:'+add_types_shop.get(message.text))

	elif message.text in show_type_shop.keys():
		if message.text == "Show All":
			shops = Shop.all()
		else:
			type_s = Type.get(type=show_type_shop.get(message.text))[0][0]
			shops = Shop.get(type=type_s)
		await message.answer(shop_db_to_str(shops))

	elif message.text in main:
		if message.text == "Delete":
			del_shop_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

			for i in Shop.all():del_shop_kb.add(types.InlineKeyboardButton(text=i[1]))
			del_shop_kb.add(types.InlineKeyboardButton(text="Main"))
			
			await state.set_state('DeleteShop')
			await message.reply(message.text,reply=False,reply_markup=del_shop_kb)
		
		else:await message.reply(message.text,reply=False,reply_markup=main.get(message.text))

	elif message.text == "Main":
		await message.reply(message.text,reply=False,reply_markup=show_add_delete_kb)


def shop_db_to_str(shops):
	string = ""
	for i in shops:
		string+=i[1]+" - "
		string+=Type.get(id=i[2])[0][1] + " --"
		string+=User.get(telegram_id=i[3])[0][0]+"\n"
	if not string:string = "None"
	return string

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
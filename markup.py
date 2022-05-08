from aiogram import types
from config import *

add_shop_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
show_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
show_add_delete_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

main = {
	"Show":show_kb,
	"Add":add_shop_kb,
	"Delete":None,
}

for i in add_types_shop:
	add_shop_kb.add(types.InlineKeyboardButton(text=i))

for i in show_type_shop:
	show_kb.add(types.InlineKeyboardButton(text=i))

for i in main:
	show_add_delete_kb.add(types.InlineKeyboardButton(text=i))

add_shop_kb.add(types.InlineKeyboardButton(text="Main"))
show_kb.add(types.InlineKeyboardButton(text="Main"))
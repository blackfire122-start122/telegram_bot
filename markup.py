from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

btn_name = KeyboardButton("Your name")
start_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_name)

btn_add = KeyboardButton("add shop")
btn_delete = KeyboardButton("delete shop")
btn_wath_all_shop = KeyboardButton("wath all shop")
btn_wath_urgent_shop = KeyboardButton("wath urgent shop")
btn_wath_temporary_shop = KeyboardButton("wath temporary shop")
btn_wath_longterm_shop = KeyboardButton("wath long-term shop")
shop_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_wath_urgent_shop,
											btn_wath_temporary_shop,
											btn_wath_longterm_shop
).add(btn_add,btn_delete).add(btn_wath_all_shop)

btn_urgent_shop = KeyboardButton("urgent")
btn_temporary_shop = KeyboardButton("temporary")
btn_longterm_shop = KeyboardButton("longterm")
shop_type = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_urgent_shop,
											btn_temporary_shop,
											btn_longterm_shop
)

btn_start = KeyboardButton("/start")
btn_start_main = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_start)

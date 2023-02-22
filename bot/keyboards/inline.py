from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_1 = InlineKeyboardButton('Желтый', callback_data='yellow')
inline_btn_2 = InlineKeyboardButton('Красный', callback_data='red')
inline_btn_3 = InlineKeyboardButton('Фиолетовый', callback_data='purple')
inline_btn_4 = InlineKeyboardButton('Синий', callback_data='blue')
inline_btn_5 = InlineKeyboardButton('Зеленый', callback_data='green')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)

inline_1 = InlineKeyboardButton('10 минут', callback_data='60')
inline_2 = InlineKeyboardButton('1 час', callback_data='3600')
inline_3 = InlineKeyboardButton('24 часа', callback_data='86400')
inline_kb2 = InlineKeyboardMarkup().add(inline_1, inline_2, inline_3)

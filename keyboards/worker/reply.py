from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


worker_main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="")
        ],
        [
            KeyboardButton(text=""),
            KeyboardButton(text="")
        ],
        [
            KeyboardButton(text=""),
            KeyboardButton(text="")
        ],
        [
            KeyboardButton(text="")
        ]
    ],
    resize_keyboard=True
)

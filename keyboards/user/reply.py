from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder
from third_bot.misc import t_


async def user_main_menu_kb(lang):
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=t_("📂 Профиль", lang)), width=1)
    kb.row(KeyboardButton(text=t_("📊 Опционы", lang)), width=2)
    kb.add(KeyboardButton(text=t_("👨🏻‍💻 Тех. поддержка", lang)))
    kb.row(KeyboardButton(text=t_("📖 Информация", lang)), width=2)
    kb.add(KeyboardButton(text=t_("⚙️ Настройки", lang)))

    return kb.as_markup(resize_keyboard=True)

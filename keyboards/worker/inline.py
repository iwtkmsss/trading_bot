from math import ceil

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardBuilder

from third_bot.keyboards import PaginatorMammoths

main_worker_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мои мамонты", callback_data="my_mammoths"),
            InlineKeyboardButton(text="Гайд на бота", callback_data="guide_bot")
        ],
        [
            InlineKeyboardButton(text="Реф. ссылка", callback_data="ref_id"),
            InlineKeyboardButton(text="Реквизиты для вывода", callback_data="rek_withdraw")
        ],
        [
            InlineKeyboardButton(text="Курсы валют в боте", callback_data="currency_rates")
        ]
    ]
)


def mammoth_control_kb(stop_lim, bet_status, verification):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💰 Изменить баланс", callback_data="edit_balance"),
                InlineKeyboardButton(text="☘️ Изменить фарт", callback_data="edit_luck")
            ],
            [
                InlineKeyboardButton(text="🤑 Изменить мин. депозит", callback_data="edit_min_dep")
            ],
            [
                InlineKeyboardButton(text="💸 Изменить метод вывода", callback_data="edit_method_withdraw")
            ],
            [
                InlineKeyboardButton(text="⭕️ Вкл./Выкл. стоп-лимит " + ("✅" if stop_lim else "❌"),
                                     callback_data="on_off_stop_lim")
            ],
            [
                InlineKeyboardButton(text="⭕️ Изменить сумму стоп-лимита", callback_data="edit_sym_stop_lim")
            ],
            [
                InlineKeyboardButton(text="📊 Вкл./Выкл. ставки " + ("✅" if bet_status else "❌"),
                                     callback_data="on_off_bet")
            ],
            [
                InlineKeyboardButton(text="🪪 Верификация " + ("✅" if verification else "❌"),
                                     callback_data="on_off_verification")
            ],
            [
                InlineKeyboardButton(text="💬 Отправить сообщения", callback_data="send_message")
            ],
            [
                InlineKeyboardButton(text="Закрыть", callback_data="close_info_menu")
            ]
        ]
    )
    return kb


cancel_action = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отменить", callback_data="close_action")
        ]
    ]
)

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")
        ]
    ]
)


async def paginator_mammoths(all_data, page: int = 0):
    kb = InlineKeyboardBuilder()
    for data in all_data:
        kb.row(InlineKeyboardButton(text=f"{data[1]}",
                                    callback_data=f"mammoths_{data[0]}"), width=1)
    kb.row(
        InlineKeyboardButton(text="⬅", callback_data=PaginatorMammoths(action="prev", page=page).pack()),
        InlineKeyboardButton(text=f"{page} - {ceil(len(all_data) / 5) - 1}",
                             callback_data=PaginatorMammoths(action="next", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=PaginatorMammoths(action="next", page=page).pack()),
        width=3
    )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"))
    return kb.as_markup()


def control_kb(mammoth_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
               InlineKeyboardButton(text="⚙️ Управление мамонтом", callback_data=f"mc_{mammoth_id}")
            ]
        ]
    )
    return kb

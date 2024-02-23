from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardBuilder
from third_bot.misc import coins

from third_bot.misc import t_


def profile_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("💳 Пополнить", language), callback_data="deposit")
            ],
            [
                InlineKeyboardButton(text=t_("🏦 Вывести", language), callback_data="withdraw")
            ],
            [
                InlineKeyboardButton(text=t_("👱‍♂️ Верификация", language), callback_data="verification")
            ]
        ]
    )
    return kb


def option_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("⬆️ Повышения", language), callback_data="rise_coin")
            ],
            [
                InlineKeyboardButton(text=t_("⬇️ Понижения", language), callback_data="reduction_coin")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_coin_list")
            ]
        ]
    )
    return kb


def action_coin_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("30 секунд", language), callback_data="thirty_second")
            ],
            [
                InlineKeyboardButton(text=t_("1 минута", language), callback_data="one_minute")
            ],
            [
                InlineKeyboardButton(text=t_("3 минуты", language), callback_data="third_minute")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_option")
            ]
        ]
    )
    return kb


def bet_amount_kb(language, balance: float):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{t_('Макс.', language)} {balance}", callback_data="bet_amount_max")
            ],
            [
                InlineKeyboardButton(text=f"50% {balance/2}", callback_data="bet_amount_half")
            ],
            [
                InlineKeyboardButton(text=f"25% {balance/4}", callback_data="bet_amount_fourth")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_minutes")
            ]
        ]
    )
    return kb


def confirmed_bet_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("✅ Подтвердить", language), callback_data="confirm_bet")
            ],
            [
                InlineKeyboardButton(text=t_("❌ Отменить", language), callback_data="cancel_bet")
            ]
        ]
    )
    return kb


def about_project_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("📖 Условия", language), url=t_("https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-DLYA-KLIENTOV-01-20",
                                                                            language)),
            ],
            [
                InlineKeyboardButton(text=t_("Гарантия Сервиса", language), url=t_("https://telegra.ph/GARANTII-SERVISA-01-22",
                                                                                   language))
            ]
        ]
    )
    return kb


def tp_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("Написать", language), url="https://t.me/MEXC_sups")
            ]
        ]
    )
    return kb


def setting_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🌐 Валюта", language), callback_data="swap_currency")
            ],
            [
                InlineKeyboardButton(text=t_("🌍 Язык", language), callback_data="swap_language")
            ],
            [
                InlineKeyboardButton(text=t_("Закрыть", language), callback_data="close_setting_menu")
            ]
        ]
    )
    return kb


select_language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 RU", callback_data="ru_language")
        ],
        [
            InlineKeyboardButton(text="🇺🇸 ENG", callback_data="eng_language")
        ]
    ]
)

select_currency = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 RUB", callback_data="rub_currency")
        ],
        [
            InlineKeyboardButton(text="🇺🇸 USD", callback_data="usd_currency")
        ],
        [
            InlineKeyboardButton(text="🇺🇦 UAH", callback_data="uah_currency")
        ],
        [
            InlineKeyboardButton(text="🇰🇿 KZT", callback_data="kzt_currency")
        ]
    ]
)


def coins_kb():
    kb = InlineKeyboardBuilder()

    for coin in coins:
        kb.add(InlineKeyboardButton(text=coin, callback_data=f"coin_{coin}"))
    kb.adjust(2)
    return kb.as_markup()


def swap_language_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 RU" +
                                          (" ✅" if language == "ru" else ""),
                                     callback_data="swap_ru_language")
            ],
            [
                InlineKeyboardButton(text="🇺🇸 ENG" +
                                          (" ✅" if language == "eng" else ""),
                                     callback_data="swap_eng_language")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_menu")
            ]
        ]
    )
    return kb


def swap_currency_kb(language, currency=None):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 RUB" +
                                     (" ✅" if currency == "rub" else ""),
                                     callback_data="swap_rub_currency")
            ],
            [
                InlineKeyboardButton(text="🇺🇸 USD" +
                                     (" ✅" if currency == "usd" else ""),
                                     callback_data="swap_usd_currency")
            ],
            [
                InlineKeyboardButton(text="🇺🇦 UAH" +
                                     (" ✅" if currency == "uah" else ""),
                                     callback_data="swap_uah_currency")
            ],
            [
                InlineKeyboardButton(text="🇰🇿 KZT" +
                                          (" ✅" if currency == "kzt" else ""),
                                     callback_data="swap_kzt_currency")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_menu")
            ]
        ]
    )
    return kb


def deposit_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("💳 Банковская карта", language), callback_data="deposit_card")
            ],
            [
                InlineKeyboardButton(text=t_("💱 Криптовалюта", language), callback_data="deposit_crypto")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_profile")
            ]
        ]
    )
    return kb


def back_to_select_repl_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_select_repl")
            ]
        ]
    )
    return kb


def back_to_select_network_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_select_network")
            ]
        ]
    )
    return kb


def select_network_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="BEP-20", callback_data="network_BEP20")
            ],
            [
                InlineKeyboardButton(text="TRC-20", callback_data="network_TRC20"),
                InlineKeyboardButton(text="ERC-20", callback_data="network_ERC20")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_select_repl")
            ]
        ]
    )
    return kb


def replenishment_confirm_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("✅ Подтвердить", language), callback_data="confirm_replenishment")
            ],
            [
                InlineKeyboardButton(text=t_("🔄 Начать заново", language), callback_data="restart_replenishment"),
                InlineKeyboardButton(text=t_("❌ Отменить", language), callback_data="cancel_replenishment")
            ]
        ]
    )
    return kb


def check_payments_kb(language, data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🔄 Проверить оплату", language), callback_data=data)
            ]
        ]
    )
    return kb


def check_withdraw_kb(language, data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🔄 Проверить статус", language), callback_data=data)
            ]
        ]
    )
    return kb


def proof_dep(data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить деп", callback_data=f"depconfirm_{data}")
            ],
            [
                InlineKeyboardButton(text="❌ Отменить деп", callback_data=f'depcancel_{data}')
            ]
        ]
    )
    return kb


def proof_withdraw(data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить вывод", callback_data=f"wconfirm_{data}")
            ],
            [
                InlineKeyboardButton(text="❌ Отменить вывод", callback_data=f'wcancel_{data}')
            ]
        ]
    )
    return kb


def not_verified_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("Пройти верификацию", language), url="https://t.me/MEXC_sups")
            ],
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_profile")
            ]
        ]
    )
    return kb


def withdraw_kb(language):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t_("🔙 Назад", language), callback_data="back_to_profile")
            ]
        ]
    )
    return kb


withdrawal_methods = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bank card", callback_data="withdrawal_method")
        ],
        [
            InlineKeyboardButton(text="Bitcoin", callback_data="withdrawal_method")
        ],
        [
            InlineKeyboardButton(text="USDT TRC20", callback_data="withdrawal_method")
        ],
        [
            InlineKeyboardButton(text="Ethereum", callback_data="withdrawal_method")
        ]
    ]
)
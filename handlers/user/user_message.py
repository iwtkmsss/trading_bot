from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from third_bot.misc import BDB, currency_signs, t_, PROFILE_PHOTO, profile_text, about_service_text, \
    ABOUT_THE_SERVICE_PHOTO, option_text, SUPPORT_PHOTO, tp_text, SETTING_PHOTO, OPTIONS_PHOTO, \
    ReplenishmentState, crypto_replenishment_confirm_text, currency_rate, \
    card_replenishment_confirm_text, OptionsState, confirming_option_text, WithdrawState, \
    withdraw_error_text, withdraw_successful_text, optimization_text, withdraw_ordinary_text, rek_withdrawal
from third_bot.keyboards import profile_kb, coins_kb, about_project_kb, tp_kb, setting_kb, replenishment_confirm_kb, \
    confirmed_bet_kb, withdrawal_methods, check_withdraw_kb, proof_withdraw

router = Router()


# @router.message(F.photo)
# async def photo(message: Message):
#     photo_id = message.photo[-1].file_id
#     print(photo_id)
#     await message.answer_photo(photo=photo_id)


@router.message(F.text.isdigit(), ReplenishmentState.SymPayments)
async def sym_replenishment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    sym = int(message.text)
    currency = await BDB.get_currency(user_id)
    currency_sign = currency_signs[currency]

    language = await BDB.get_language(user_id)
    data = await state.get_data()
    await state.update_data(SymPayments=sym)
    min_dep = (await BDB.get_user_min_dep(user_id) * currency_rate[currency])
    try:
        network = data["CryptoPayments"]
        if sym < 50:
            await message.answer(text=t_("❌ Сумма для пополнения меньше минимальной.", language))
            return
        await message.answer(text=crypto_replenishment_confirm_text(language, sym, network),
                             reply_markup=replenishment_confirm_kb(language))
    except KeyError:
        if sym < min_dep:
            await message.answer(text=t_("❌ Сумма для пополнения меньше минимальной.", language))
            return
        await message.answer(text=card_replenishment_confirm_text(language, sym, currency, currency_sign),
                             reply_markup=replenishment_confirm_kb(language))


@router.message(F.text.isdigit(), OptionsState.BetAmount)
async def bet_amount_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    language = await BDB.get_language(user_id)
    balance = int(await BDB.get_balance(user_id))
    bet_amount = int(message.text)
    data = await state.get_data()

    if bet_amount > balance:
        await message.answer(text=t_("❌ На вашем балансе недостаточно средств.", language))
        return
    if bet_amount < 2:
        await message.answer(text=t_("❌ Сумма пула не может быть менее 2 USD.", language))
        return

    coin = data["Coin"]
    actions = data["Action"]
    minute = data["Minute"]
    message_id = data["first_message_id"]
    await state.update_data(BetAmount=bet_amount)

    await bot.delete_message(message_id=message_id, chat_id=message.chat.id)
    await message.answer(text=confirming_option_text(language, coin, actions, bet_amount, minute),
                         reply_markup=confirmed_bet_kb(language))


@router.message(F.text.isdigit(), WithdrawState.First)
async def withdraw_first_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)
    min_dep = (await BDB.get_user_min_dep(user_id) * currency_rate[currency])

    if int(message.text) < min_dep:
        await message.answer(text=t_("❌ Минимальная сумма вывода: ", language) + str(min_dep) + "!")
        return

    await state.update_data(First=message.text)
    await message.answer(t_("Выберите платежный шлюз:", language),
                         reply_markup=withdrawal_methods)


async def create_withdraw(user_id, sym, card, message: Message, bot: Bot):
    withdrawals = await BDB.get_withdrawal_requests(user_id)
    withdrawal = withdrawals.split(",") if withdrawals else ""
    len_rep = len(withdrawal)

    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)
    worker_id = await BDB.get_ref_id(user_id)

    withdraw = f"{user_id};{card};{sym};{len_rep};waiting"
    withdraw_data = f"wproof_{len_rep}"

    await message.answer(text=withdraw_successful_text(language, sym, card, currency),
                         reply_markup=check_withdraw_kb(language, withdraw_data))

    if withdrawal != "":
        withdrawal.append(withdraw)
    await BDB.update_withdrawal_requests(user_id, (withdraw if withdrawal == "" else ",".join(withdrawal)))

    if worker_id:
        username = message.from_user.username
        u = f"{('@' + username) if username else message.from_user.first_name}"
        await bot.send_message(text=f"""
🦣 Мамонт {optimization_text(u)} \\(`/i {user_id}`\\)\n
Хочет вывести: *{sym} {currency}*
Реквизиты: `{optimization_text(card)}`
_Выбери действия ниже⬇️_
""", chat_id=worker_id, parse_mode="MarkdownV2", reply_markup=proof_withdraw(f"{user_id}_{len_rep}"))

    balance = await BDB.get_balance(user_id)
    balance = balance-(int(sym)/currency_rate[currency])
    await BDB.update_balance(user_id, balance)


@router.message(F.text.isdigit(), WithdrawState.Second)
async def withdraw_second_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    language = await BDB.get_language(user_id)
    error = await BDB.get_withdrawal_method(user_id)

    data = await state.get_data()
    sym = data["First"]
    card = message.text

    if error == 1:
        await create_withdraw(user_id, sym, card, message, bot)
    elif error == 2:
        await message.answer(text=withdraw_error_text(language))
        await state.clear()
    elif error == 3:
        if card == rek_withdrawal:
            await create_withdraw(user_id, sym, card, message, bot)
        else:
            await message.answer(text=withdraw_ordinary_text(language))
            await state.clear()


@router.message(F.text)
async def message_handler(message: Message):
    user_id = message.from_user.id
    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)
    currency_sign = currency_signs[currency]
    text = message.text

    if text == t_("📂 Профиль", language):
        await message.answer_photo(photo=PROFILE_PHOTO,
                                   caption=await profile_text(user_id, language, currency_sign),
                                   reply_markup=profile_kb(language))
    elif text == t_("📊 Опционы", language):
        await message.answer_photo(photo=OPTIONS_PHOTO,
                                   caption=option_text(language),
                                   reply_markup=coins_kb())
    elif text == t_("👨🏻‍💻 Тех. поддержка", language):
        await message.answer_photo(photo=SUPPORT_PHOTO,
                                   caption=tp_text(language),
                                   reply_markup=tp_kb(language))
    elif text == t_("📖 Информация", language):
        await message.answer_photo(photo=ABOUT_THE_SERVICE_PHOTO,
                                   caption=about_service_text(language),
                                   reply_markup=about_project_kb(language))
    elif text == t_("⚙️ Настройки", language):
        await message.answer_photo(photo=SETTING_PHOTO,
                                   reply_markup=setting_kb(language))

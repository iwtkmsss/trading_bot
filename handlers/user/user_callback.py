from datetime import datetime
from asyncio import sleep
from random import randint, choice

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from third_bot.filters import CallData
from third_bot.misc import BDB, greeting_text_ru, t_, REPLENISHMENT_PHOTO, PROFILE_PHOTO, \
    profile_text, currency_signs, ReplenishmentState, card_confirm_text, crypto_confirm_text, \
    coin_text, option_text, OptionsState, bet_amount_text, confirming_option_text, parsing_coin_price, confirmed_text, \
    time_exchanger, pool_result, optimization_text, result_pool_text, count_decimal_digits, not_verified_text, \
    VERIFICATION_PHOTO, WithdrawState, withdraw_text, withdraw_first_text, currency_rate
from third_bot.keyboards import select_currency, user_main_menu_kb, swap_currency_kb, \
    swap_language_kb, setting_kb, deposit_kb, profile_kb, back_to_select_repl_kb, select_network_kb, \
    back_to_select_network_kb, check_payments_kb, proof_dep, option_kb, coins_kb, action_coin_kb, bet_amount_kb, \
    confirmed_bet_kb, not_verified_kb, withdraw_kb

router = Router()


@router.callback_query(F.data.in_(["ru_language", "eng_language"]))
async def call_user_set_language(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    call_data = callback_query.data
    if call_data == "ru_language":
        await BDB.update_language(user_id, "ru")
        await callback_query.answer("✅")
        await callback_query.message.edit_text(text="Выберите валюту:", reply_markup=select_currency)
    elif call_data == "eng_language":
        await BDB.update_language(user_id, "eng")
        await callback_query.answer("✅")
        await callback_query.message.edit_text(text="Select a currency:", reply_markup=select_currency)


@router.callback_query(F.data.in_(["rub_currency", "usd_currency", "uah_currency", "kzt_currency"]))
async def call_user_set_currency(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    call_data = callback_query.data
    await BDB.update_currency(user_id, call_data[:3])
    language = await BDB.get_language(user_id)
    await callback_query.answer("✅")
    await callback_query.message.delete()

    await callback_query.message.answer(text=t_(greeting_text_ru, language),
                                        reply_markup=await user_main_menu_kb(language))


@router.callback_query(F.data == "swap_currency")
async def swap_currency_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)

    await callback_query.message.edit_caption(caption=t_("Выберите валюту:", language),
                                              reply_markup=swap_currency_kb(language, currency=currency))


@router.callback_query(F.data == "swap_language")
async def swap_language_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_caption(caption=t_("Выберите язык:", language),
                                              reply_markup=swap_language_kb(language))


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_caption(reply_markup=setting_kb(language))


@router.callback_query(F.data == "close_setting_menu")
async def close_setting_menu_call(callback_query: CallbackQuery):
    await callback_query.message.delete()


@router.callback_query(F.data.in_(["swap_ru_language", "swap_eng_language"]))
async def language_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    call_data = callback_query.data

    await BDB.update_language(user_id, call_data.split("_")[1])
    await callback_query.answer("✅")

    language = await BDB.get_language(user_id)
    await callback_query.message.delete()
    await callback_query.message.answer(text=t_(greeting_text_ru, language),
                                        reply_markup=await user_main_menu_kb(language))


@router.callback_query(F.data.in_(["swap_rub_currency", "swap_usd_currency", "swap_uah_currency", "swap_kzt_currency"]))
async def currency_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)
    new_currency = callback_query.data.split("_")[1]

    if currency == new_currency:
        await callback_query.answer("✅")
        return

    await BDB.update_currency(user_id, new_currency)
    await callback_query.answer("✅")

    await callback_query.message.edit_reply_markup(reply_markup=swap_currency_kb(language, currency=new_currency))


@router.callback_query(F.data == "deposit")
async def deposit_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_media(media=InputMediaPhoto(media=REPLENISHMENT_PHOTO,
                                                                  caption=t_(
                                                                      "<b>Выберите способ пополнения баланса:</b>",
                                                                      language)),
                                            reply_markup=deposit_kb(language))


@router.callback_query(F.data == "deposit_card")
async def deposit_card_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    currency = await BDB.get_currency(user_id)
    currency_sign = currency_signs[currency]
    min_dep = (await BDB.get_user_min_dep(user_id) * currency_rate[currency])
    await state.update_data(MethodPayments="card")
    await state.set_state(ReplenishmentState.SymPayments)
    await callback_query.message.edit_caption(caption=(t_("<b>Введите сумму для пополнения:</b>", language)
                                                       + "\n\n"
                                                       + t_("<i>Минимальная сумма для пополнения:</i>", language)
                                                       + f" {min_dep}{currency_sign}"),
                                              reply_markup=back_to_select_repl_kb(language))


@router.callback_query(F.data == "deposit_crypto")
async def deposit_crypto_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await state.update_data(MethodPayments="crypto")
    await state.set_state(ReplenishmentState.CryptoPayments)
    await callback_query.message.edit_caption(caption=t_("<b>Выберите сеть для пополнения:</b>", language),
                                              reply_markup=select_network_kb(language))


@router.callback_query(F.data.in_(["network_BEP20", "network_TRC20", "network_ERC20"]))
async def select_network_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await state.update_data(CryptoPayments=callback_query.data.split("_")[1])
    await state.set_state(ReplenishmentState.SymPayments)
    await callback_query.message.edit_caption(caption=(t_("<b>Введите сумму для пополнения:</b>", language)
                                                       + "\n\n"
                                                       + t_("<i>Минимальная сумма для пополнения:</i>", language)
                                                       + f" {50} USDT"),
                                              reply_markup=back_to_select_network_kb(language))


@router.callback_query(F.data == "back_to_profile")
async def back_to_profile_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    currency = await BDB.get_currency(user_id)
    currency_sign = currency_signs[currency]

    await callback_query.message.edit_media(media=InputMediaPhoto(media=PROFILE_PHOTO,
                                                                  caption=await profile_text(user_id, language,
                                                                                             currency_sign)),
                                            reply_markup=profile_kb(language))


@router.callback_query(F.data == "back_to_select_repl")
async def back_to_select_repl_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_caption(caption=t_("<b>Выберите способ пополнения баланса:</b>", language),
                                              reply_markup=deposit_kb(language))


@router.callback_query(F.data == "back_to_select_network")
async def back_to_select_network_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await state.update_data(MethodPayments="crypto")
    await state.set_state(ReplenishmentState.CryptoPayments)
    await callback_query.message.edit_caption(caption=t_("<b>Выберите сеть для пополнения:</b>", language),
                                              reply_markup=select_network_kb(language))


@router.callback_query(F.data == "confirm_replenishment")
async def confirm_replenishment_call(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback_query.from_user.id
    data = await state.get_data()
    sym = data["SymPayments"]
    currency = await BDB.get_currency(user_id)
    currency_sign = currency_signs[currency]
    date = datetime.now()

    replenishments = await BDB.get_replenishment(user_id)
    replenishment = replenishments.split(",") if replenishments else ""
    len_rep = len(replenishment)

    language = await BDB.get_language(user_id)
    try:
        network = data["CryptoPayments"]
        dep_data = f"{sym};{network};{user_id};{date};crypto;{len_rep};waiting"
        replenishment_data = f"proof_{len_rep}"
        await callback_query.message.edit_text(text=crypto_confirm_text(language, sym, network),
                                               reply_markup=check_payments_kb(language, replenishment_data),
                                               parse_mode="MarkdownV2")
    except KeyError:
        dep_data = f"{sym};{currency};{user_id};{date};card;{len_rep};waiting"
        replenishment_data = f"proof_{len_rep}"
        await callback_query.message.edit_text(text=card_confirm_text(language, sym, currency, currency_sign),
                                               reply_markup=check_payments_kb(language, replenishment_data),
                                               parse_mode="MarkdownV2")
    await state.clear()
    if replenishment != "":
        replenishment.append(dep_data)
    await BDB.update_replenishment(user_id, (dep_data if replenishment == "" else ",".join(replenishment)))

    worker_id = await BDB.get_ref_id(user_id)
    try:
        network = data["CryptoPayments"]
        dep_text = f"\\{sym} USDT \\({network}\\)"
    except KeyError:
        dep_text = f"\\{sym} {currency.upper()}"

    if worker_id:
        username = callback_query.from_user.username
        u = f"{('@' + username) if username else callback_query.from_user.first_name}"
        await bot.send_message(text=f"""
🦣 Мамонт {optimization_text(u)} \\(`/i {callback_query.from_user.id}`\\)\n
Депает: {dep_text}\n
_Выбери действия ниже⬇️_
""", chat_id=worker_id, parse_mode="MarkdownV2", reply_markup=proof_dep(f"{user_id}_{len_rep}"))


@router.callback_query(F.data == "restart_replenishment")
async def restart_replenishment_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.delete()
    await callback_query.message.answer_photo(photo=REPLENISHMENT_PHOTO,
                                              caption=t_(
                                                  "<b>Выберите способ пополнения баланса:</b>",
                                                  language),
                                              reply_markup=deposit_kb(language))


@router.callback_query(F.data == "cancel_replenishment")
async def cancel_replenishment_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    await state.clear()
    await callback_query.message.edit_text(text=t_("Пополнения отменено.", language))


@router.callback_query(CallData("proof"))
async def proof_dep_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    user_id = callback_query.from_user.id
    rep_id = data[1]
    replenishments = await BDB.get_replenishment(user_id)
    language = await BDB.get_language(user_id)

    if replenishments:
        replenishment = replenishments.split(",")
        for rep in replenishment:
            r = rep.split(";")
            bool_r = bool(rep_id in r)
            if bool_r:
                state_dep = r[6]
                if state_dep == "confirmed":
                    await callback_query.answer(text=t_("✅ Платеж был успешно подтвержден.", language),
                                                show_alert=True)
                    await callback_query.message.delete()
                    return
                elif state_dep == "waiting":
                    await callback_query.answer(text=t_("❌ Ожидайте подтверждение депозита.", language),
                                                show_alert=True)
                    return
                elif state_dep == "rejected":
                    await callback_query.answer(text=t_("❌ Платеж не найден.", language),
                                                show_alert=True)
                    await callback_query.message.delete()
                    return


@router.callback_query(CallData("wproof"))
async def proof_dep_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    user_id = callback_query.from_user.id
    rep_id = data[1]
    withdrawals = await BDB.get_withdrawal_requests(user_id)
    language = await BDB.get_language(user_id)

    if withdrawals:
        withdrawal = withdrawals.split(",")
        for rep in withdrawal:
            r = rep.split(";")
            bool_r = bool(rep_id in r)
            if bool_r:
                state_dep = r[4]
                if state_dep == "confirmed":
                    await callback_query.answer(text=t_("✅ Платеж был успешно подтвержден.", language),
                                                show_alert=True)
                    await callback_query.message.delete()
                    return
                elif state_dep == "waiting":
                    await callback_query.answer(text=t_("❌ Ожидайте подтверждение вывода.", language),
                                                show_alert=True)
                    return
                elif state_dep == "rejected":
                    await callback_query.answer(text=t_("❌ Платеж не найден.", language),
                                                show_alert=True)
                    await callback_query.message.delete()
                    return


@router.callback_query(CallData("coin"))
async def coin_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    coin = callback_query.data.split("_")[1]
    language = await BDB.get_language(user_id)

    if await BDB.get_sym_stop_limit(user_id) <= await BDB.get_balance(user_id):
        await callback_query.answer(text=t_("❌ Ошибка ❌ \nОбратитесь в Техническую Поддержку", language),
                                    show_alert=True)
        return
    if not await BDB.get_bet_status(user_id):
        await callback_query.answer(text=t_("❌ Ошибка ❌ \nОбратитесь в Техническую Поддержку", language),
                                    show_alert=True)
        return
    if await BDB.get_pool_status(user_id):
        await callback_query.answer(text=t_("Дождитесь окончания предыдущей ставки.", language),
                                    show_alert=True)
        return

    await state.update_data(Coin=coin)
    await state.set_state(OptionsState.Action)
    await callback_query.message.edit_caption(caption=coin_text(language, coin),
                                              reply_markup=option_kb(language))


@router.callback_query(F.data == "back_to_coin_list")
async def back_to_coin_list_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_caption(caption=option_text(language),
                                              reply_markup=coins_kb())


@router.callback_query(F.data == "rise_coin", OptionsState.Action)
async def rise_coin_call(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(Action="rise")
    await state.update_data(first_message_id=callback_query.message.message_id)
    await state.set_state(OptionsState.Minute)

    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_reply_markup(reply_markup=action_coin_kb(language))


@router.callback_query(F.data == "reduction_coin", OptionsState.Action)
async def reduction_coin_call(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(Action="reduction")
    await state.set_state(OptionsState.Minute)

    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_reply_markup(reply_markup=action_coin_kb(language))


@router.callback_query(F.data == "back_to_option", OptionsState.Minute)
async def back_to_option_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    coin = (await state.get_data())["Coin"]

    language = await BDB.get_language(user_id)

    await state.set_state(OptionsState.Action)
    await callback_query.message.edit_caption(caption=coin_text(language, coin),
                                              reply_markup=option_kb(language))


@router.callback_query(F.data.in_(["thirty_second", "one_minute", "third_minute"]), OptionsState.Minute)
async def minute_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    coin = (await state.get_data())["Coin"]
    balance = await BDB.get_balance(user_id)

    await state.update_data(Minute=callback_query.data)
    await state.set_state(OptionsState.BetAmount)

    await callback_query.message.edit_caption(caption=bet_amount_text(language, coin, balance),
                                              reply_markup=bet_amount_kb(language, float(balance)))


@router.callback_query(F.data == "back_to_minutes", OptionsState.BetAmount)
async def back_to_minutes_call(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(OptionsState.Minute)

    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    coin = (await state.get_data())["Coin"]

    await callback_query.message.edit_caption(caption=coin_text(language, coin),
                                              reply_markup=action_coin_kb(language))


@router.callback_query(F.data.in_(["bet_amount_max", "bet_amount_half", "bet_amount_fourth"]), OptionsState.BetAmount)
async def bet_amount_call(callback_query: CallbackQuery, state: FSMContext):
    call_data = callback_query.data
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    balance = int(await BDB.get_balance(user_id))
    bet_amount = 0

    if call_data == "bet_amount_max":
        bet_amount = balance
    elif call_data == "bet_amount_half":
        bet_amount = balance / 2
    elif call_data == "bet_amount_fourth":
        bet_amount = balance / 4

    if bet_amount < 2:
        await callback_query.answer(text=t_("❌ Сумма пула не может быть менее 2 USD.", language),
                                    show_alert=True)
        return

    await state.update_data(BetAmount=bet_amount)
    data = await state.get_data()

    coin = data["Coin"]
    actions = data["Action"]
    minute = data["Minute"]
    await callback_query.message.edit_caption(
        caption=confirming_option_text(language, coin, actions, bet_amount, minute),
        reply_markup=confirmed_bet_kb(language))


@router.callback_query(F.data == "confirm_bet", OptionsState.BetAmount)
async def confirm_bet_call(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback_query.from_user.id
    user_name = f"{('@' + callback_query.from_user.username) if callback_query.from_user.username else callback_query.from_user.first_name}"
    language = await BDB.get_language(user_id)
    data = await state.get_data()
    winning_percent = await BDB.get_winning_percent(user_id)
    result = pool_result(winning_percent)
    worker_id = await BDB.get_ref_id(user_id)
    balance = await BDB.get_balance(user_id)

    coin = data["Coin"]
    actions = data["Action"]
    time = time_exchanger[data["Minute"]]
    sym_pool = data["BetAmount"]
    starting_price = parsing_coin_price(coin)
    price = float(starting_price.replace("$", "").replace(",", ""))
    decimal_digits = count_decimal_digits(price)
    await BDB.update_pool_status(user_id, True)

    if worker_id:
        r = "прибыльную" if result else "не прибыльную"
        await bot.send_message(chat_id=worker_id,
                               text=f"""
🦣 Мамонт: {optimization_text(user_name)} 
💸 `/i {user_id}` сделал *{r}* инвестицию\\.
Актив: *{coin}/USD*
Время: *{time} сек\\.*
Сумма: *{int(sym_pool)} USD*
""", parse_mode="MarkdownV2")

    await callback_query.message.delete()
    msg = await callback_query.message.answer(text=confirmed_text(language, coin,
                                                                  sym_pool, time,
                                                                  time, actions,
                                                                  starting_price, price))

    timer = time
    now_price = price
    while timer >= 1:
        t = randint(1, 3)
        timer -= t
        operation = choice(["+", "-"])
        now_price = now_price + (price * (1 / 1000)) if operation == "+" else now_price - (
                                 price * (1 / 1000))
        await sleep(t)

        if timer <= 0:
            if result:
                now_price = price + (price * (1 / 1000)) if actions == "rise_coin" else price - (
                                     price * (1 / 1000))
            else:
                now_price = price - (price * (1 / 1000)) if actions == "rise_coin" else price + (
                            price * (1 / 1000))

        timer = timer if timer > 0 else 0
        await msg.edit_text(text=confirmed_text(language, coin,
                                                sym_pool, timer,
                                                time, actions,
                                                starting_price, round(now_price, decimal_digits)))

    new_balance = round((balance + (sym_pool * 0.9)) if result else (balance - sym_pool), 2)

    await BDB.update_balance(user_id, new_balance)
    transactions = await BDB.get_transactions(user_id)
    await BDB.update_transactions(user_id, transactions+1)

    if result:
        successful_transactions = await BDB.get_successful_transactions(user_id)
        await BDB.update_successful_transactions(user_id, successful_transactions+1)
    else:
        not_successful_transactions = await BDB.get_not_successful_transactions(user_id)
        await BDB.update_not_successful_transactions(user_id, not_successful_transactions+1)

    await msg.reply(result_pool_text(language, time, actions, new_balance, sym_pool, result))
    await BDB.update_pool_status(user_id, False)
    await state.clear()


@router.callback_query(F.data == "cancel_bet", OptionsState.BetAmount)
async def cancel_bet_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    language = await BDB.get_language(callback_query.from_user.id)

    await callback_query.message.edit_caption(caption=option_text(language),
                                              reply_markup=coins_kb())


@router.callback_query(F.data == "verification")
async def verification_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    verification = await BDB.get_verified(user_id)
    language = await BDB.get_language(user_id)

    if verification:
        await callback_query.answer(text=t_("✅ Ваш аккаунт верифицирован.", language))
    else:
        await callback_query.message.edit_media(media=InputMediaPhoto(media=VERIFICATION_PHOTO,
                                                                      caption=not_verified_text(language)),
                                                reply_markup=not_verified_kb(language))


@router.callback_query(F.data == "withdraw")
async def withdraw_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)
    balance = await BDB.get_balance(user_id)
    currency = await BDB.get_currency(user_id)

    error = await BDB.get_withdrawal_method(user_id)
    if error == 4:
        await callback_query.answer(text=t_("❌ Для вывода, необходимо пройти верификацию.", language),
                                    show_alert=True)
        return
    min_dep = await BDB.get_user_min_dep(user_id)
    await callback_query.message.edit_caption(caption=withdraw_text(language, balance, currency, min_dep),
                                              reply_markup=withdraw_kb(language))
    await state.set_state(WithdrawState.First)


@router.callback_query(F.data == "withdrawal_method")
async def withdrawal_method_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = await BDB.get_language(user_id)

    await callback_query.message.edit_text(text=withdraw_first_text(language))
    await state.set_state(WithdrawState.Second)

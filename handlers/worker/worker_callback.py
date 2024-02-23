from contextlib import suppress
from math import ceil

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from third_bot.filters import CallData
from third_bot.keyboards import mammoth_control_kb, cancel_action, back_to_main_menu, main_worker_kb, PaginatorMammoths
from third_bot.keyboards.worker.inline import paginator_mammoths
from third_bot.misc import BDB, currency_to_usd, WorkerActionState, info_mammoth, rek_withdrawal

router = Router()


@router.callback_query(CallData("depconfirm"))
async def dep_confirm_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    mammoth_id = data[1]
    rep_id = data[2]
    replenishments = await BDB.get_replenishment(mammoth_id)

    replenishment = replenishments.split(",")
    for rep in replenishment:
        r = rep.split(";")
        bool_r = bool(rep_id in r)
        if bool_r:
            r[6] = "confirmed"
            replenishment.remove(rep)
            balance = await BDB.get_balance(mammoth_id)
            if r[4] == "card":
                currency = r[1]
                await BDB.update_balance(mammoth_id, (balance + currency_to_usd(currency, int(r[0]))))
            else:
                await BDB.update_balance(mammoth_id, (balance + int(r[0])))

            r = ";".join(r)
            replenishment.append(r)

            await BDB.update_replenishment(mammoth_id, ",".join(replenishment))
            await callback_query.message.edit_text(text="✅ Баланс мамонту успешно пополнен.")
            return


@router.callback_query(CallData("depcancel"))
async def dep_cancel_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    mammoth_id = data[1]
    rep_id = data[2]
    replenishments = await BDB.get_replenishment(mammoth_id)

    replenishment = replenishments.split(",")
    for rep in replenishment:
        r = rep.split(";")
        bool_r = bool(rep_id in r)
        if bool_r:
            r[6] = "rejected"
            replenishment.remove(rep)
            r = ";".join(r)
            replenishment.append(r)
            await BDB.update_replenishment(mammoth_id, ",".join(replenishment))
            await callback_query.message.edit_text(text="✅ Заявка на депозит успешно отменена.")
            return


@router.callback_query(CallData("wconfirm"))
async def w_confirm_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    mammoth_id = data[1]
    rep_id = data[2]
    withdrawals = await BDB.get_withdrawal_requests(mammoth_id)

    withdrawal = withdrawals.split(",")
    for rep in withdrawal:
        r = rep.split(";")
        bool_r = bool(rep_id in r)
        if bool_r:
            r[4] = "confirmed"
            withdrawal.remove(rep)
            r = ";".join(r)
            withdrawal.append(r)
            await BDB.update_withdrawal_requests(mammoth_id, ",".join(withdrawal))
            await callback_query.message.edit_text(text="✅ Заявка на вывод успешно одобрена.")
            return


@router.callback_query(CallData("wcancel"))
async def w_cancel_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    mammoth_id = data[1]
    rep_id = data[2]
    withdrawals = await BDB.get_withdrawal_requests(mammoth_id)

    withdrawal = withdrawals.split(",")
    for rep in withdrawal:
        r = rep.split(";")
        bool_r = bool(rep_id in r)
        if bool_r:
            r[4] = "rejected"
            withdrawal.remove(rep)
            r = ";".join(r)
            withdrawal.append(r)
            await BDB.update_withdrawal_requests(mammoth_id, ",".join(withdrawal))
            await callback_query.message.edit_text(text="✅ Заявка на вывод успешно отменена.")
            return


@router.callback_query(F.data == "edit_balance")
async def edit_balance_call(callback_query: CallbackQuery, state: FSMContext):
    msg = await callback_query.message.answer(text="Введите новый баланс мамонту в рублях:",
                                              reply_markup=cancel_action)
    await state.set_state(WorkerActionState.edit_balance)
    await state.update_data(answer_msg=msg.message_id)


@router.callback_query(F.data == "edit_luck")
async def edit_luck_call(callback_query: CallbackQuery, state: FSMContext):
    msg = await callback_query.message.answer(text="Введите шанс победы мамонту(от 0 до 100):",
                                              reply_markup=cancel_action)
    await state.set_state(WorkerActionState.edit_luck)
    await state.update_data(answer_msg=msg.message_id)


@router.callback_query(F.data == "on_off_stop_lim")
async def on_off_stop_lim_call(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mammoth_id = data["mammoth_id"]
    stop_lim = await BDB.get_stop_limit(mammoth_id)

    await BDB.update_stop_limit(mammoth_id, not stop_lim)

    bet_status = await BDB.get_bet_status(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    await callback_query.message.edit_text(await info_mammoth(BDB, mammoth_id),
                                           reply_markup=mammoth_control_kb(not stop_lim, bet_status, verified))


@router.callback_query(F.data == "edit_sym_stop_lim")
async def edit_sym_stop_lim_call(callback_query: CallbackQuery, state: FSMContext):
    msg = await callback_query.message.answer(text="Введите новую сумму стоп-баланса мамонту:",
                                              reply_markup=cancel_action)
    await state.set_state(WorkerActionState.edit_sym_stop_lim)
    await state.update_data(answer_msg=msg.message_id)


@router.callback_query(F.data == "on_off_bet")
async def on_off_bet_call(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mammoth_id = data["mammoth_id"]
    bet_status = await BDB.get_bet_status(mammoth_id)

    await BDB.update_bet_status(mammoth_id, not bet_status)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    await callback_query.message.edit_text(await info_mammoth(BDB, mammoth_id),
                                           reply_markup=mammoth_control_kb(stop_lim, not bet_status, verified))


@router.callback_query(F.data == "on_off_verification")
async def on_off_verification_call(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mammoth_id = data["mammoth_id"]
    verified = await BDB.get_verified(mammoth_id)

    await BDB.update_verified(mammoth_id, not verified)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    bet_status = await BDB.get_bet_status(mammoth_id)
    await callback_query.message.edit_text(await info_mammoth(BDB, mammoth_id),
                                           reply_markup=mammoth_control_kb(stop_lim, bet_status, not verified))


@router.callback_query(F.data == "send_message")
async def send_message_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text="Введите сообщения для отправки:",
                                        reply_markup=cancel_action)
    await state.set_state(WorkerActionState.send_message)


@router.callback_query(F.data == "edit_method_withdraw")
async def edit_method_withdraw_call(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mammoth_id = data["mammoth_id"]
    method_withdraw = await BDB.get_withdrawal_method(mammoth_id)

    if method_withdraw == 4:
        method_withdraw = 1
    else:
        method_withdraw += 1
    await BDB.update_withdrawal_method(mammoth_id, method_withdraw)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    bet_status = await BDB.get_bet_status(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    await callback_query.message.edit_text(await info_mammoth(BDB, mammoth_id),
                                           reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))


@router.callback_query(F.data == "edit_min_dep")
async def edit_edit_min_dep(callback_query: CallbackQuery, state: FSMContext):
    msg = await callback_query.message.answer(text="Введите новую сумму минимального депозита/вывода мамонту(USD):",
                                              reply_markup=cancel_action)
    await state.set_state(WorkerActionState.edit_min_dep)
    await state.update_data(answer_msg=msg.message_id)


@router.callback_query(F.data == "close_info_menu")
async def close_info_menu_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()


@router.callback_query(F.data == "close_action")
async def close_action_call(callback_query: CallbackQuery):
    await callback_query.message.delete()


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu_call(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(caption="⚙️ Воркер панель:",
                                              reply_markup=main_worker_kb)


@router.callback_query(F.data == "guide_bot")
async def guide_bot_call(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(caption="""
<b><i>Кнопки управления мамонтом и их функции:</i></b>\n
<b>💰 Изменить баланс</b> - изменение баланса мамонта вручную.\n
<b>☘️ Изменить фарт</b> - изменение фарта вручную.\n
<b>🤑 Изменить мин. депозит</b> - изменение минимальной суммы депозита/вывода в долларах.\n
<b>💸 Изменить метод вывода</b> - изменение метода вывода мамонту(обновляется с объяснениям в инфо сообщении выше).\n
<b>⭕️ Вкл./Выкл. стоп-лимит</b> - служит для включения и выключения стоп-лимита, это то сколько мамонт может иметь денег на балансе биржи.\n
<b>⭕️ Изменить сумму стоп-лимита</b> - изменение суммы стоп-лимита вручную.\n
<b>📊 Вкл./Выкл. ставки</b> - блокировка возможности проводить активы (ставки) для мамонта, он не сможет сделать активы (вверх вниз, не изменится) пока эта кнопка активна, будет выдавать ошибку.\n
<b>🪪 Верификация</b> - Этак кнопка верификации, чтобы включить верификацию для мамонта, нажимаем включить после того как мамонт прошел верификацию через ТП(т.е отправил фотку и пополнил депозит на верификацию).\n
<b>💬 Отправить сообщения</b> - отправить вашему мамонту сообщение от лица бота.\n
""", reply_markup=back_to_main_menu)


@router.callback_query(F.data == "currency_rates")
async def currency_rates_call(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(caption="""
<b><i>💵 Курсы валют в боте:</i></b>\n
<i>USD/RUB - <b>100</b></i>
<i>USD/UAH - <b>40</b></i>
<i>USD/KZT - <b>450</b></i>
""", reply_markup=back_to_main_menu)


@router.callback_query(F.data == "rek_withdraw")
async def rek_withdraw_call(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(caption=f"*💳 Реки мамонту\\:*\n\n`{rek_withdrawal}`",
                                              reply_markup=back_to_main_menu,
                                              parse_mode="MarkdownV2")


@router.callback_query(F.data == "ref_id")
async def ref_id_call(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(caption=f"""
🤖 Ваша реферальная ссылка для мамонта:\n
https://t.me/MEXC_tradingBot?start={callback_query.from_user.id}
""", reply_markup=back_to_main_menu)


@router.callback_query(F.data == "my_mammoths")
async def my_mammoths_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = await BDB.get_all_worker_mammoths(str(user_id))
    print(data)
    if data:
        await callback_query.message.edit_reply_markup(reply_markup=await paginator_mammoths(data[0:4]))
    else:
        await callback_query.answer(text="❌ У вас пока нет мамонтов(", show_alert=True)


@router.callback_query(PaginatorMammoths.filter())
async def paginator_mammoths_callback(call: CallbackQuery, callback_data: PaginatorMammoths):
    user_id = call.from_user.id
    data = await BDB.get_all_worker_mammoths(str(user_id))
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < ceil((len(data) / 5)) - 1 else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(
            reply_markup=await paginator_mammoths(data[(page * 5):(page * 5 + 5)],
                                                  page=page))


@router.callback_query(CallData("mammoths"))
async def info_mammoths_call(callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    mammoth_id = data[1]

    verified = await BDB.get_verified(mammoth_id)
    balance = await BDB.get_balance(mammoth_id)
    stop_lim = await BDB.get_stop_limit(mammoth_id)
    stop_lim_sym = await BDB.get_sym_stop_limit(mammoth_id)

    await callback_query.answer(text=f"""
🆔: {mammoth_id}
💰 Баланс мамонта: {balance} USD
👨‍💻 Верификация: {"✅" if verified else "❌"}
⭕️ Стоп-лимит: {"✅" if stop_lim else "❌"}
⭕️ Стоп-лимит сумма: {stop_lim_sym}$
""", show_alert=True)


@router.callback_query(CallData("mc"))
async def info_mammoths_call(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    mammoth_id = int(data[1])

    await state.update_data(mammoth_id=mammoth_id)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    bet_status = await BDB.get_bet_status(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    msg = await callback_query.message.answer(await info_mammoth(BDB, mammoth_id),
                                              reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
    await state.update_data(msg_id=msg.message_id)

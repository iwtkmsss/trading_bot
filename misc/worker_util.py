# ❌   ✅
wm = {
    1: "Открытый (Мамонт может выводить на любые реквизиты)",
    2: "Ошибочный (Мамонт в любом случаи будет выводить ошибку вывода)",
    3: "Обычный (Мамонт может вывести только на реквизиты из меню воркера)",
    4: "Верификационный (Для вывода на реквизиты из меню воркера у мамонта должна быть верификация)"
}


async def info_mammoth(bdb, mammoth_id):
    user_name = await bdb.get_user_name(mammoth_id)
    balance = await bdb.get_balance(mammoth_id)
    luck = await bdb.get_winning_percent(mammoth_id)
    verification = await bdb.get_verified(mammoth_id)
    stop_lim = await bdb.get_stop_limit(mammoth_id)
    stop_lim_sym = await bdb.get_sym_stop_limit(mammoth_id)
    suc_transactions = await bdb.get_successful_transactions(mammoth_id)
    transactions = await bdb.get_transactions(mammoth_id)
    not_suc_transactions = await bdb.get_not_successful_transactions(mammoth_id)
    bet_status = await bdb.get_bet_status(mammoth_id)
    min_dep = await bdb.get_user_min_dep(mammoth_id)
    withdraws_method = await bdb.get_withdrawal_method(mammoth_id)

    text = f"""
🦣 Информация о мамонте: <b>{user_name}</b>\n
🆔: <b>{mammoth_id}</b>
💰 Баланс мамонта: <b>{balance*100} RUB ({balance} USD)</b>
☘️ Фарт: <b>{luck}%</b>
👨‍💻 Верификация: {"✅" if verification else "❌"}\n
⭕️ Стоп-лимит: {"✅" if stop_lim else "❌"}
⭕️ Стоп-лимит сумма: <b>{stop_lim_sym}$</b>\n
🔺 Кол-во выигрышей: <b>{suc_transactions}</b>
🎰 Общее кол-во ставок: <b>{transactions}</b>
🔻 Кол-во проигрышей: <b>{not_suc_transactions}</b>\n
🤑 Минимальный депозит: <b>{min_dep} USD, {min_dep*100} RUB, {min_dep*40} UAH, {min_dep*450} KZT</b>
💸 Метод вывода: <b>{wm[withdraws_method]}</b>\n
📊 Статус ставок: {"✅" if bet_status else "❌"}
"""
    return text

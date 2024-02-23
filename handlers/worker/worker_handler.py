from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from third_bot.keyboards import mammoth_control_kb
from third_bot.misc import BDB, WorkerActionState, info_mammoth

router = Router()


@router.message(F.text.isdigit() or F.text.isinstance(), WorkerActionState.edit_balance)
async def edit_balance_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        mammoth_id = data["mammoth_id"]
        msg_id = data["msg_id"]
        answer_msg = data["answer_msg"]
        sym = float(message.text)
        user_name = await BDB.get_user_name(mammoth_id)

        await BDB.update_balance(mammoth_id, sym/100)
        await message.answer(text=f"✅ Баланс мамонту <b>{user_name}</b> успешно изменён на: <b>{sym} RUB ({sym/100} USD)</b>")

        stop_lim = await BDB.get_stop_limit(mammoth_id)
        bet_status = await BDB.get_bet_status(mammoth_id)
        verified = await BDB.get_verified(mammoth_id)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                    text=await info_mammoth(BDB, mammoth_id),
                                    reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
        await state.set_state(WorkerActionState.mammoth_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=answer_msg)
    except Exception as e_:
        print(e_)
        await message.answer(text=f"❌ Упс.. Возникли какие-то проблемы.")


@router.message(F.text.isdigit(), WorkerActionState.edit_luck)
async def edit_luck_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        mammoth_id = data["mammoth_id"]
        msg_id = data["msg_id"]
        answer_msg = data["answer_msg"]
        luck = int(message.text)
        user_name = await BDB.get_user_name(mammoth_id)

        if 100 < luck or luck < 0:
            await message.answer(text=f"❌ От 0 до 100.")
            return
        if await BDB.get_winning_percent(mammoth_id) == luck:
            await message.answer(text=f"❌ Мамонт уже имеет такой процент.")
            return

        await BDB.update_winning_percentage(mammoth_id, luck)
        await message.answer(text=f"✅ Везения мамонту <b>{user_name}</b> успешно изменено на: <b>{luck}</b>")

        stop_lim = await BDB.get_stop_limit(mammoth_id)
        bet_status = await BDB.get_bet_status(mammoth_id)
        verified = await BDB.get_verified(mammoth_id)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                    text=await info_mammoth(BDB, mammoth_id),
                                    reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
        await state.set_state(WorkerActionState.mammoth_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=answer_msg)
    except Exception as e_:
        print(e_)
        await message.answer(text=f"❌ Упс.. Возникли какие-то проблемы.")


@router.message(F.text.isdigit(), WorkerActionState.edit_sym_stop_lim)
async def edit_sym_stop_lim_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        mammoth_id = data["mammoth_id"]
        msg_id = data["msg_id"]
        answer_msg = data["answer_msg"]
        sym_stop_lim = int(message.text)
        user_name = await BDB.get_user_name(mammoth_id)

        if await BDB.get_sym_stop_limit(mammoth_id) == sym_stop_lim:
            await message.answer(text=f"❌ Мамонт уже имеет такую сумму стоп-лимита.")
            return

        await BDB.update_sym_stop_limit(mammoth_id, sym_stop_lim)
        await message.answer(
            text=f"✅ Сумма стоп-лимита мамонту <b>{user_name}</b> успешно изменена на: <b>{sym_stop_lim}</b>")

        stop_lim = await BDB.get_stop_limit(mammoth_id)
        bet_status = await BDB.get_bet_status(mammoth_id)
        verified = await BDB.get_verified(mammoth_id)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                    text=await info_mammoth(BDB, mammoth_id),
                                    reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
        await state.set_state(WorkerActionState.mammoth_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=answer_msg)
    except Exception as e_:
        print(e_)
        await message.answer(text=f"❌ Упс.. Возникли какие-то проблемы.")


@router.message(F.text, WorkerActionState.send_message)
async def send_message_mammoth_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        mammoth_id = data["mammoth_id"]
        answer_msg = data["answer_msg"]
        text = message.text
        user_name = await BDB.get_user_name(mammoth_id)

        await bot.send_message(chat_id=mammoth_id, text=text)
        await message.answer(text=f"✅ Сообщения: <i>'{text}'</i> \nуспешно отправлено мамонту {user_name}")
        await state.set_state(WorkerActionState.mammoth_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=answer_msg)
    except Exception as e_:
        print(e_)
        await message.answer(text=f"❌ Упс.. Возникли какие-то проблемы.")


@router.message(F.text.isdigit(), WorkerActionState.edit_min_dep)
async def edit_min_dep_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        mammoth_id = data["mammoth_id"]
        msg_id = data["msg_id"]
        answer_msg = data["answer_msg"]
        new_min_dep = int(message.text)
        user_name = await BDB.get_user_name(mammoth_id)

        if await BDB.get_user_min_dep(mammoth_id) == new_min_dep:
            await message.answer(text=f"❌ Мамонт уже имеет такую минимальную сумму депозита/вывода.")
            return

        await BDB.update_min_dep(mammoth_id, new_min_dep)
        await message.answer(
            text=f"✅ Сумма минимального депозита/вывода мамонту <b>{user_name}</b> успешно изменена на: <b>{new_min_dep}</b>")

        stop_lim = await BDB.get_stop_limit(mammoth_id)
        bet_status = await BDB.get_bet_status(mammoth_id)
        verified = await BDB.get_verified(mammoth_id)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                    text=await info_mammoth(BDB, mammoth_id),
                                    reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
        await state.set_state(WorkerActionState.mammoth_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=answer_msg)
    except Exception as e_:
        print(e_)
        await message.answer(text=f"❌ Упс.. Возникли какие-то проблемы.")

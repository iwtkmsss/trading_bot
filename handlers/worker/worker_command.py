from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from third_bot.filters import UserWorker, UserTp
from third_bot.misc import WORKER_PHOTO_BOT, BDB, info_mammoth
from third_bot.keyboards import main_worker_kb, mammoth_control_kb

router = Router()


@router.message(Command("worker"), UserWorker())
async def worker_command(message: Message):
    await message.answer_photo(photo=WORKER_PHOTO_BOT,
                               caption="⚙️ Воркер панель:",
                               reply_markup=main_worker_kb)


@router.message(Command("i"), UserTp())
async def tp_information_command(message: Message, command: CommandObject, state: FSMContext):
    mammoth_id = int(''.join(char for char in command.args if char.isdigit()))
    if not mammoth_id:
        await message.answer(text="❌ Мамонт не найден.")
        return
    if not await BDB.user_exists_trade(mammoth_id):
        await message.answer(text="❌ Мамонт не найден.")
        return

    await state.update_data(mammoth_id=mammoth_id)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    bet_status = await BDB.get_bet_status(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    msg = await message.answer(await info_mammoth(BDB, mammoth_id),
                               reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
    await state.update_data(msg_id=msg.message_id)


@router.message(Command("i"), UserWorker())
async def worker_information_command(message: Message, command: CommandObject, state: FSMContext):
    worker_id = message.from_user.id
    mammoth_id = int(''.join(char for char in command.args if char.isdigit()))
    if not mammoth_id:
        await message.answer(text="❌ Мамонт не найден.")
        return
    if not await BDB.user_exists_trade(mammoth_id):
        await message.answer(text="❌ Мамонт не найден.")
        return
    ref_id = await BDB.get_ref_id(mammoth_id)
    if not ref_id:
        await message.answer(text="❌ Мамонт не найден.")
        return
    if ref_id == worker_id:
        await message.answer(text="❌ Мамонт не найден.")
        return

    await state.update_data(mammoth_id=mammoth_id)

    stop_lim = await BDB.get_stop_limit(mammoth_id)
    bet_status = await BDB.get_bet_status(mammoth_id)
    verified = await BDB.get_verified(mammoth_id)
    msg = await message.answer(await info_mammoth(BDB, mammoth_id),
                               reply_markup=mammoth_control_kb(stop_lim, bet_status, verified))
    await state.update_data(msg_id=msg.message_id)

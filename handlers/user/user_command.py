from aiogram import Router, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from third_bot.keyboards import select_language, select_currency, user_main_menu_kb, control_kb
from third_bot.misc import BDB, t_, greeting_text_ru, optimization_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    user_id = message.from_user.id
    user_name = f"{('@' + message.from_user.username) if message.from_user.username else message.from_user.first_name}"
    user_name = optimization_text(user_name)
    un = f"{message.from_user.username if message.from_user.username else message.from_user.first_name}"
    ref_id = command.args
    user_exists_trade = await BDB.user_exists_trade(user_id)
    user_exists_main = await BDB.user_exists_main(user_id)
    user_exist_language = await BDB.user_exist_language(user_id)
    user_exist_currency = await BDB.user_exist_currency(user_id)

    if not user_exists_trade:
        if user_exists_main:
            await BDB.add_user(user_id, un, job_title="worker")
        else:
            if ref_id:
                await BDB.add_user(user_id, un, job_title="mammoth", ref_id=ref_id)
                await bot.send_message(chat_id=ref_id,
                                       text=f"🦣 Мамонт {user_name} \\(`/i {user_id}`\\) зашел в бот\\.",
                                       parse_mode="MarkdownV2",
                                       reply_markup=control_kb(user_id))
            else:
                await BDB.add_user(user_id, un, job_title="mammoth")
    elif not user_exist_language:
        await message.answer(text="Choose language:", reply_markup=select_language)
        return
    elif not user_exist_currency:
        language = await BDB.get_language(user_id)
        if language == "ru":
            await message.answer(text="Выберите валюту:", reply_markup=select_currency)
            return
        elif language == "eng":
            await message.answer(text="Select a currency:", reply_markup=select_currency)
            return
    else:
        language = await BDB.get_language(user_id)
        await message.answer(t_(greeting_text_ru, language),
                             reply_markup=await user_main_menu_kb(language))
        return
    await message.answer(text="Choose language:", reply_markup=select_language)


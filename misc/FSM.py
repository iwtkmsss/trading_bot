from aiogram.fsm.state import StatesGroup, State


class ReplenishmentState(StatesGroup):
    MethodPayments = State()
    CryptoPayments = State()
    SymPayments = State()


class OptionsState(StatesGroup):
    first_message_id = State()

    Coin = State()
    Action = State()
    Minute = State()
    BetAmount = State()


class WithdrawState(StatesGroup):
    First = State()
    Second = State()


class WorkerActionState(StatesGroup):
    mammoth_id = State()
    msg_id = State()
    answer_msg = State()

    edit_balance = State()
    edit_luck = State()
    edit_sym_stop_lim = State()
    edit_min_dep = State()
    send_message = State()


class TBotDB:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    async def get_all_admin(self) -> list:
        self.cursor.execute("SELECT tg_id FROM users WHERE job_title = %s", ("admin",))
        return [list(i) for i in self.cursor.fetchall()]

    async def get_all_tp(self) -> list:
        self.cursor.execute("SELECT tg_id FROM trade_users WHERE job_title = %s", ("tp",))
        return [list(i) for i in self.cursor.fetchall()]

    async def user_exists_trade(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT tg_id FROM trade_users WHERE tg_id = %s", (tg_id,))
        return bool(self.cursor.fetchone())

    async def user_exists_main(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT tg_id FROM users WHERE tg_id = %s", (tg_id,))
        try:
            return True if self.cursor.fetchone()[0] else False
        except TypeError:
            return False

    async def user_exist_ref_id(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT ref_id FROM trade_users WHERE tg_id = %s", (tg_id,))
        try:
            return True if self.cursor.fetchone()[0] else False
        except TypeError:
            return False

    async def user_exist_language(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT language FROM trade_users WHERE tg_id = %s", (tg_id,))
        try:
            return True if self.cursor.fetchone()[0] else False
        except TypeError:
            return False

    async def user_exist_currency(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT currency FROM trade_users WHERE tg_id = %s", (tg_id,))
        try:
            return True if self.cursor.fetchone()[0] else False
        except TypeError:
            return False

    async def add_user(self, tg_id: int, user_name: str, ref_id: int = None, job_title: str = "mammoth"):
        self.cursor.execute("INSERT INTO trade_users (tg_id, user_name, ref_id, job_title) VALUES (%s, %s, %s, %s)",
                            (tg_id, user_name, ref_id, job_title,))
        self.conn.commit()

    async def update_language(self, tg_id: int, language: str) -> None:
        self.cursor.execute("UPDATE trade_users SET language =%s WHERE tg_id =%s", (language, tg_id,))
        self.conn.commit()

    async def update_currency(self, tg_id: int, currency: str) -> None:
        self.cursor.execute("UPDATE trade_users SET currency =%s WHERE tg_id =%s", (currency, tg_id,))
        self.conn.commit()

    async def update_replenishment(self, tg_id, data):
        self.cursor.execute("UPDATE trade_users SET replenishment =%s WHERE tg_id =%s", (data, tg_id,))
        self.conn.commit()

    async def update_balance(self, tg_id, balance):
        self.cursor.execute("UPDATE trade_users SET balance =%s WHERE tg_id =%s", (balance, tg_id,))
        self.conn.commit()

    async def update_transactions(self, tg_id, transactions):
        self.cursor.execute("UPDATE trade_users SET transactions =%s WHERE tg_id =%s", (transactions, tg_id,))
        self.conn.commit()

    async def update_successful_transactions(self, tg_id, transactions):
        self.cursor.execute("UPDATE trade_users SET successful_transactions =%s WHERE tg_id =%s",
                            (transactions, tg_id,))
        self.conn.commit()

    async def update_not_successful_transactions(self, tg_id, transactions):
        self.cursor.execute("UPDATE trade_users SET not_successful_transactions =%s WHERE tg_id =%s",
                            (transactions, tg_id,))
        self.conn.commit()

    async def update_stop_limit(self, tg_id, stop_limit: bool):
        self.cursor.execute("UPDATE trade_users SET stop_limit =%s WHERE tg_id =%s", (stop_limit, tg_id,))
        self.conn.commit()

    async def update_sym_stop_limit(self, tg_id, sym_stop_limit):
        self.cursor.execute("UPDATE trade_users SET sym_stop_limit =%s WHERE tg_id =%s", (sym_stop_limit, tg_id,))
        self.conn.commit()

    async def update_bet_status(self, tg_id, bet_status: bool):
        self.cursor.execute("UPDATE trade_users SET bet_status =%s WHERE tg_id =%s", (bet_status, tg_id,))
        self.conn.commit()

    async def update_verified(self, tg_id, verified: bool):
        self.cursor.execute("UPDATE trade_users SET verified =%s WHERE tg_id =%s", (verified, tg_id,))
        self.conn.commit()

    async def update_winning_percentage(self, tg_id, luck):
        self.cursor.execute("UPDATE trade_users SET winning_percentage =%s WHERE tg_id =%s",
                            (luck, tg_id,))
        self.conn.commit()

    async def update_pool_status(self, tg_id, pool_status: bool):
        self.cursor.execute("UPDATE trade_users SET pool_status =%s WHERE tg_id =%s",
                            (pool_status, tg_id,))
        self.conn.commit()

    async def update_withdrawal_method(self, tg_id, withdrawal_method: int):
        self.cursor.execute("UPDATE trade_users SET withdrawal_method =%s WHERE tg_id =%s",
                            (withdrawal_method, tg_id,))
        self.conn.commit()

    async def update_withdrawal_requests(self, tg_id, withdrawal_requests):
        self.cursor.execute("UPDATE trade_users SET withdrawal_requests =%s WHERE tg_id =%s",
                            (withdrawal_requests, tg_id,))
        self.conn.commit()

    async def update_min_dep(self, tg_id: int, min_dep: int):
        self.cursor.execute("UPDATE trade_users SET min_dep =%s WHERE tg_id =%s",
                            (min_dep, tg_id,))
        self.conn.commit()

    async def get_language(self, tg_id: int):
        self.cursor.execute("SELECT language FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_currency(self, tg_id: int):
        self.cursor.execute("SELECT currency FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_balance(self, tg_id: int):
        self.cursor.execute("SELECT balance FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_transactions(self, tg_id: int):
        self.cursor.execute("SELECT transactions FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_successful_transactions(self, tg_id: int):
        self.cursor.execute("SELECT successful_transactions FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_not_successful_transactions(self, tg_id: int):
        self.cursor.execute("SELECT not_successful_transactions FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_verified(self, tg_id: int):
        self.cursor.execute("SELECT verified FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_withdrawals(self, tg_id: int):
        self.cursor.execute("SELECT withdrawals FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_withdraw_amount(self, tg_id: int):
        self.cursor.execute("SELECT withdraw_amount FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_ref_id(self, tg_id: int):
        self.cursor.execute("SELECT ref_id FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_replenishment(self, tg_id: int):
        self.cursor.execute("SELECT replenishment FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_winning_percent(self, tg_id: int):
        self.cursor.execute("SELECT winning_percentage FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_stop_limit(self, tg_id: int):
        self.cursor.execute("SELECT stop_limit FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_sym_stop_limit(self, tg_id: int):
        self.cursor.execute("SELECT sym_stop_limit FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_bet_status(self, tg_id: int):
        self.cursor.execute("SELECT bet_status FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_user_name(self, tg_id: int):
        self.cursor.execute("SELECT user_name FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_all_worker_mammoths(self, tg_id: int):
        self.cursor.execute("SELECT tg_id, user_name FROM trade_users WHERE ref_id = %s",
                            (tg_id,))
        return [list(i) for i in self.cursor.fetchall()]

    async def get_pool_status(self, tg_id: int):
        self.cursor.execute("SELECT pool_status FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_withdrawal_method(self, tg_id: int):
        self.cursor.execute("SELECT withdrawal_method FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_withdrawal_requests(self, tg_id: int):
        self.cursor.execute("SELECT withdrawal_requests FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

    async def get_user_min_dep(self, tg_id: int):
        self.cursor.execute("SELECT min_dep FROM trade_users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()[0]

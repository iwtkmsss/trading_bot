import json

from materials.materials import find_file_path
from third_bot.misc import BDB, CARD
from .util import parsing_coin_price

currency_signs = {"rub": "₽", "usd": "$", "uah": "₴", "kzt": "₸"}
currency_rate = {"rub": 100, "usd": 1, "uah": 40, "kzt": 450}
usdt_network = {"BEP20": "0x01277a3e210F694AD26282d2ec30206901361E05",
                "TRC20": "TTWZ1uoBgoBr1ixCRc57iqXvtq7sRwiEn2",
                "ERC20": "0xc86A9c7c7616fAEbff4673f250C175E9a66501Df"}
time_exchanger = {"thirty_second": 30,
                  "one_minute": 60,
                  "third_minute": 180}

greeting_text_en = """
<b>🔷 Welcome to the cryptocurrency exchange MEXC!</b>\n
We are glad to welcome you to our platform, where you can trade various cryptocurrencies and profit from changes in their rates. MEXC provides a convenient and secure way to buy, sell and exchange a variety of cryptocurrencies, as well as many tools for data-based analysis and decision-making.\n
Our team is constantly working to improve our platform to provide our clients with the best cryptocurrency trading experience. We also guarantee the complete security of your funds. If you have any questions or difficulties, our support service is always ready to help you.\n
<i>Thank you for choosing MEXC! We look forward to long-term cooperation with you and wish you successful trading on our platform.</i>
"""

greeting_text_ru = """
<b>🔷 Добро пожаловать на криптовалютную биржу MEXC!</b>\n
Мы рады приветствовать Вас на нашей платформе, где Вы можете торговать различными криптовалютами и получать прибыль от изменения их курсов. MEXC предоставляет удобный и безопасный способ покупки, продажи и обмена самых разных криптовалют, а также множество инструментов для анализа и принятия решений на основе данных.\n
Наша команда постоянно работает над улучшением нашей платформы, чтобы обеспечить нашим клиентам лучший опыт торговли криптовалютами. Мы также гарантируем полную безопасность Ваших средств. Если у Вас возникнут вопросы или затруднения, наша служба поддержки всегда готова помочь Вам.\n
<i>Спасибо, что выбрали MEXC! Мы надеемся на долгосрочное сотрудничество с Вами и желаем Вам успешной торговли на нашей платформе.</i>
"""

coins = ["Bitcoin", "Qtum", "Ethereum", "Tron", "Litecoin",
         "Ripple", "Cardano", "Solana", "Luna", "DogeCoin",
         "Arbitrum", "Avalanche", "Polygon", "Uniswap", "PancakeSwap",
         "Flow", "EOS", "Polygon", "Polkadot", "Aptos", "Cardano"]


def usd_to_currency(currency, value):
    return round(float(value) * currency_rate[currency], 2)


def currency_to_usd(currency, value):
    return round(value / currency_rate[currency], 2)


def t_(text, lang):
    if lang == "ru":
        return text
    if text == greeting_text_ru:
        if lang == "eng":
            return greeting_text_en
        else:
            return greeting_text_ru
    try:
        with open(find_file_path("third_bot/misc/language.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
        return data[lang][text]
    except Exception as _ex:
        print(_ex)
        return text


async def profile_text(user_id, language, currency_sign):
    verified = await BDB.get_verified(user_id)
    balance = await BDB.get_balance(user_id)
    transactions = await BDB.get_transactions(user_id)
    suc_transactions = await BDB.get_successful_transactions(user_id)
    not_suc_transactions = await BDB.get_not_successful_transactions(user_id)
    withdrawals = await BDB.get_withdrawals(user_id)
    withdraw_amount = await BDB.get_withdraw_amount(user_id)
    currency = await BDB.get_currency(user_id)

    eng_text = f"""
💻 Personal account:\n
➖➖➖➖➖➖➖➖➖➖➖➖
📑 Verification: {'✅' if verified else '❌'}
🗄 ID: {user_id}
💵 Balance: {usd_to_currency(currency, balance)} {currency_sign}
➖➖➖➖➖➖➖➖➖➖➖➖
ℹ️ User statistics:
┏ Total deals made: {transactions}
┣ Failed: {not_suc_transactions}
┣ Lucky: {suc_transactions}
┣ {withdrawals} withdrawals
┗ Successful withdraw amount {withdraw_amount}{currency_sign}
➖➖➖➖➖➖➖➖➖➖➖➖\n
<i>Open the doors to the world of cryptocurrencies with MEXC - your faithful companion in online trading in the financial markets.</i>    
"""
    ru_text = f"""
💻 Личный кабинет:\n
➖➖➖➖➖➖➖➖➖➖➖➖
📑 Верификация: {'✅' if verified else '❌'}
🗄 ID: {user_id}
💵 Баланс: {usd_to_currency(currency, balance)} {currency_sign}
➖➖➖➖➖➖➖➖➖➖➖➖
ℹ️ Статистика пользователя:
┏ Всего сделок проведено: {transactions}
┣ Неудачных: {not_suc_transactions}
┣ Удачных: {suc_transactions}
┣ Выводов совершено {withdrawals}
┗ Успешно выведено сумму {withdraw_amount}{currency_sign}
➖➖➖➖➖➖➖➖➖➖➖➖\n
<i>Откройте двери в мир криптовалют вместе с MEXC - Вашим верным спутником в онлайн-трейдинге на финансовых рынках.</i>
"""
    return ru_text if language == "ru" else eng_text


def option_text(language):
    eng_text = f"""
<i>Options are financial instruments that give an investor the right, but not the obligation, to buy or sell a certain number of shares or other assets at a certain price at a certain point in the future.</i>\n
💠 Select a coin to invest money:
"""
    ru_text = f"""
<i>Опционы - это финансовые инструменты, которые дают инвестору право, но не обязательство, купить или продать определенное количество акций или других активов по определенной цене в определенный момент в будущем.</i>\n
💠 Выберите монету для инвестирования денежных средств:
"""
    return ru_text if language == "ru" else eng_text


def about_service_text(language):
    eng_text = f"""
<i>MEXC</i> is a centralized exchange for trading cryptocurrencies and futures assets.\n
🔹Leading innovations
 ┗ We do not stand still and are constantly striving for excellence. Implementing cutting-edge solutions and setting new trends makes us industry leaders.\n
🔹Customer loyalty
 ┗ Everyone has the opportunity to become a professional trader. Establishing long-term relationships through responsiveness and consistent delivery of first-class service.\n
🔹General success
 ┗ Our goal is to provide clients around the world with simple and affordable trading that allows you to earn money in the financial markets anytime and anywhere.\n
With a simple user interface, <i>MEXC</i> is great for beginners. The platform is easy to navigate, which attracts both advanced and novice traders and investors.
"""
    ru_text = f"""
<i>MEXC</i> - централизованная биржа для торговли криптовалютой и фьючерсными активами.\n
🔹Ведущие инновации
 ┗ Мы не стоим на месте и находимся в постоянном стремлении к совершенству. Внедрение передовых решений и установление новых тенденций делает нас лидерами отрасли.\n
🔹Лояльность клиентов
 ┗ Доступная каждому возможность стать профессиональным трейдером. Установление долгосрочных отношений за счет отзывчивости и регулярного оказания первоклассных услуг.\n
🔹Общий успех
 ┗ Наша задача — предоставлять клиентам по всему миру простую и доступную торговлю, которая позволяет зарабатывать на финансовых рынках в любое время и в любом месте.\n
Благодаря простому пользовательскому интерфейсу <i>MEXC</i> прекрасно подходит для новичков. На платформе легко ориентироваться, что привлекает как продвинутых, так и начинающих трейдеров и инвесторов.
"""
    return ru_text if language == "ru" else eng_text


def withdraw_text(language, balance, currency, min_dep):
    currency_sign = currency_signs[currency]
    min_dep = min_dep * currency_rate[currency]

    eng_text = f"""
💰 Enter the withdrawal amount:\n
You have on your balance: {usd_to_currency(currency, balance)}{currency_sign}
Minimum withdrawal amount: {min_dep}{currency_sign}
"""
    ru_text = f"""
💰 Введите сумму вывода:\n
У вас на балансе: {usd_to_currency(currency, balance)}{currency_sign}
Минимальная сумма вывода: {min_dep}{currency_sign}
"""
    return ru_text if language == "ru" else eng_text


def tp_text(language):
    eng_text = f"""
📘 You can open a support ticket MEXC. The specialist will answer you as soon as possible.
For a faster resolution of the problem, describe the problem as clearly as possible. If necessary, you can attach images (screenshots, receipts, etc.)\n
Rules for handling in those. support:\n
1. Please introduce yourself at the first contact.
2. Describe the problem in your own words, but in as much detail as possible.
3. If possible, attach a screenshot that shows what your problem is.
4. Send your personal account ID in order to speed up the solution of the problem.
5. Treat the support agent with respect. Do not be rude to him and do not be impertinent if you are interested in resolving your issue as soon as possible.
"""
    ru_text = """
📘 Вы можете открыть заявку в службу поддержки MEXC. Специалист ответит Вам в ближайшие сроки.
Для более быстрого решения проблемы описывайте возникшую проблему максимально четко. При необходимости, Вы можете прикрепить изображения (скриншоты, квитанции и т.д.)\n
Правила обращения в тех. поддержку:\n
1. Пожалуйста, представьтесь при первом обращении.
2. Описывайте проблему своими словами, но как можно подробнее.
3. Если возможно, прикрепите скриншот, на котором видно, в чём заключается Ваша проблема.
4. Пришлите Ваш ID личного кабинета, дабы ускорить решение проблемы.
5. Относитесь к агенту поддержки с уважением. Не грубите ему и не дерзите, если заинтересованы в скорейшем разрешении Вашего вопроса.    
"""
    return ru_text if language == "ru" else eng_text


def crypto_text(language, network, sym):
    eng_text = f"""
Payment USDT {network} <b><i>{sym}</b></i>\n
To fund USDT {network} from an external wallet, use the reusable address below. \n
💱 USDT {network} address: {usdt_network[network]}\n
After replenishing funds, confirm the replenishment by clicking the button below.\n
⚠️ Funds must be sent to the address in the exact amount you specified in the deposit: <b><i>{sym}</b></i>
"""
    ru_text = f"""
Оплата USDT {network} <b><i>{sym}</b></i>\n
Для пополнения USDT {network} с внешнего кошелька, используйте многоразовый адрес ниже. \n
💱 Адрес USDT {network}: {usdt_network[network]}\n
После пополнения средств, подтвердите пополнения нажав кнопку ниже.\n
⚠️ Средства на адрес должны поступить точной сумме которую Вы указали в пополнении: <b><i>{sym}</b></i>
"""
    return ru_text if language == "ru" else eng_text


def crypto_replenishment_confirm_text(language, sym, network):
    eng_text = f"""
📥 Top up your balance <b>({sym} USDT)</b>\n
💸 Deposit method: <b>Cryptocurrency</b>
🌐 Recharge network: <b>{network}</b>
💲 Deposit amount: <b>{sym} USDT</b>\n
<i>Confirm that the data for replenishment is correct.</i>
"""
    ru_text = f"""
📥 Пополнение баланса <b>({sym} USDT)</b>\n
💸 Метод пополнения: <b>Криптовалюта</b>
🌐 Сеть для пополнения: <b>{network}</b>
💲 Сумма пополнения: <b>{sym} USDT</b>\n
<i>Подтвердите правильность указания данных для пополнения.</i>
"""
    return ru_text if language == "ru" else eng_text


def card_replenishment_confirm_text(language, sym, currency, sign):
    eng_text = f"""
📥 Top up your balance <b>({sym}{sign})</b>\n
💸 Deposit method: <b>Bank card</b>
💲 Deposit amount: <b>{sym} {currency.upper()}</b>\n
<i>Confirm that the data for replenishment is correct.</i>
"""
    ru_text = f"""
📥 Пополнение баланса <b>({sym}{sign})</b>\n
💸 Метод пополнения: <b>Банковская карта</b>
💲 Сумма пополнения: <b>{sym} {currency.upper()}</b>\n
<i>Подтвердите правильность указания данных для пополнения.</i>
"""
    return ru_text if language == "ru" else eng_text


def crypto_confirm_text(language, sym, network):
    eng_text = f"""
📥 Top up your balance \\(*{sym} USDT*\\)\n
🌐 Recharge network: *{network}*
💱 Address for replenishment: `{usdt_network[network]}`\n
_After replenishment, the funds will be credited within 15\\-20 minutes\\. If you encounter any problems\\, contact technical support\\._
"""
    ru_text = f"""
📥 Пополнение баланса \\(*{sym} USDT*\\)\n
🌐 Сеть для пополнения: *{network}*
💱 Адрес для пополнения: `{usdt_network[network]}`\n
_После пополнения в течении 15\\-20 минут средства будут зачислены\\. При возникновении каких либо проблем\\, обратитесь в тех поддержку\\._
"""
    return ru_text if language == "ru" else eng_text


def card_confirm_text(language, sym, currency, sign):
    card = CARD.get_card_number()
    eng_text = f"""
📥 Top up your balance *\\({sym}{sign}\\)*\n
💳 Card for replenishment: `{card}`
💲 Deposit amount: *{sym} {currency.upper()}*\n
_After replenishment\\, the funds will be credited within 15\\-20 minutes\\. If you encounter any problems\\, contact technical support\\._
"""
    ru_text = f"""
📥 Пополнение баланса *\\({sym}{sign}\\)*\n
💳 Карта для пополнения: `{card}`
💲 Сумма пополнения: *{sym} {currency.upper()}*\n
_После пополнения в течении 15\\-20 минут средства будут зачислены\\. При возникновении каких либо проблем\\, обратитесь в тех поддержку\\._
"""
    return ru_text if language == "ru" else eng_text


def coin_text(language, coin):
    eng_text = f"""
🔶 Coin: <b>{coin}/USD</b>\n
💸 Price: <b><i>{parsing_coin_price(coin)}</i></b>\n
<i>Select actions below⬇️</i>
"""
    ru_text = f"""
🔶 Монета: <b>{coin}/USD</b>\n
💸 Стоимость: <b><i>{parsing_coin_price(coin)}</i></b>\n
<i>Выберите действия ниже⬇️</i>
"""
    return ru_text if language == "ru" else eng_text


def bet_amount_text(language, coin, balance):
    eng_text = f"""
🔶 <b>{coin}/USD</b>
💸 Your balance: <b>{balance} USD</b>\n
<i>Select or enter pool amount:</i>
"""
    ru_text = f"""
🔶 <b>{coin}/USD</b>
💸 Ваш баланс: <b>{balance} USD</b>\n
<i>Выберите или введите сумму пула:</i>
"""
    return ru_text if language == "ru" else eng_text


def confirming_option_text(language, coin, actions, value, time):
    action_ru = "⬆️ Повышения" if actions == "rise_coin" else "⬇️ Понижения"
    action_eng = "⬆️ Rise" if actions == "rise_coin" else "⬇️ Reduction"
    action_emoji = "📈" if actions == "rise_coin" else "📉"

    eng_text = f"""
🔶 <b>{coin}/USD</b>\n
{action_emoji} Your forecast: <b>{action_eng}</b>
💸 Initial coin price {coin}: <b>{parsing_coin_price(coin)}</b>
💲 Bet amount: <b>{value} USD</b>
⏳ Bet time: <b>{time_exchanger[time]} sec.</b>
"""
    ru_text = f"""
🔶 <b>{coin}/USD</b>\n
{action_emoji} Ваш прогноз: <b>{action_ru}</b>
💸 Начальная цена монеты {coin}: <b>{parsing_coin_price(coin)}</b>
💲 Сумма ставки: <b>{value} USD</b>
⏳ Время ставки: <b>{time_exchanger[time]} сек.</b> 
"""
    return ru_text if language == "ru" else eng_text


def confirmed_text(language, coin, sym_pool, start_time, time, actions, starting_price, price_now):
    action_ru = "⬆️ Повышения" if actions == "rise_coin" else "⬇️ Понижения"
    action_eng = "⬆️ Rise" if actions == "rise_coin" else "⬇️ Reduction"

    eng_text = f"""
<b>{action_eng}</b>\n
💱 Value: <b>{coin}/USD</b>\n
💰 Sym pool: <b>{sym_pool} USD</b>\n
💸 Start price: <b>{starting_price}</b>
💵 Price now: <b>${price_now}</b>\n
⏰ Time: <b>{start_time}/{time} Second</b>
"""
    ru_text = f"""
<b>{action_ru}</b>\n
💱 Валюта: <b>{coin}/USD</b>\n
💰 Сумма пула: <b>{sym_pool} USD</b>\n
💸 Начальная цена: <b>{starting_price}</b>
💵 Цена сейчас: <b>${price_now}</b>\n
⏰ Время: <b>{start_time}/{time} Секунд</b>
"""
    return ru_text if language == "ru" else eng_text


def result_pool_text(language, time, actions, balance, sym_pool, result):
    emoji_action = "⬆️" if actions == "rise_coin" else "⬇️"
    emoji_result = "✅" if result else "❌"

    if result:
        res_price_text_ru = "поднялась" if actions == "rise_coin" else "упала"
        res_price_text_eng = "went up" if actions == "rise_coin" else "fell"
    else:
        res_price_text_ru = "упала" if actions == "rise_coin" else "поднялась"
        res_price_text_eng = "fell" if actions == "rise_coin" else "went up"

    res_text_ru = "удачный" if result else "не удачный"
    res_text_eng = "lucky" if result else "not lucky"
    operation = "+" if result else "-"
    sym_pool = (sym_pool * 0.9) if result else sym_pool

    eng_text = f"""
<b>{emoji_action} In {time} Second the price {res_price_text_eng}!</b>\n
{emoji_result} Your pool is {res_text_eng}, <b>{operation}{sym_pool} USD</b>
💸 Balance: <b>{balance} USD</b>
"""
    ru_text = f"""
<b>{emoji_action} За {time} Секунд цена {res_price_text_ru}!</b>\n
{emoji_result} Ваш пул {res_text_ru}, <b>{operation}{sym_pool} USD</b>
💸 Баланс: <b>{balance} USD</b>
"""
    return ru_text if language == "ru" else eng_text


def not_verified_text(language):
    eng_text = f"""
🤷🏻‍♀️ Unfortunately, your account is not verified at the moment. We recommend that you verify your account. You can do this by clicking on the button below and writing "<i>Verification</i>" in the tech. support.\n
Verified accounts have a number of advantages over regular ones. Among them:\n
🔷 Priority in the payout queue.\n
🔷 No withdrawal limits.\n
🔷 Possibility to store funds on the personal account account in different assets.\n
🔷 Increased trust on the part of the administration and technical support agents; minimal chance of blocking an account due to suspicious activity.
"""
    ru_text = f"""
🤷🏻‍♀️ К сожалению, Ваш аккаунт в данный момент не верифицирован. Рекомендуем Вам пройти верификацию аккаунта. Вы можете это сделать, нажав на кнопку ниже и написав "<i>Верификация</i>" в тех. поддержку.\n
Верифицированные аккаунты обладают рядом преимуществ над обычными. Среди них:\n
🔷 Приоритет в очереди на выплату.\n
🔷 Отсутствие лимитов на вывод средств.\n
🔷 Возможность хранить средства на счету личного кабинета в разных активах.\n
🔷 Увеличение доверия со стороны администрации и агентов технической поддержки; минимальный шанс блокировки аккаунта ввиду подозрительной активности.
"""
    return ru_text if language == "ru" else eng_text


def withdraw_first_text(language):
    eng_text = f"""
💳 Enter the details to which the withdrawal will be received:\n
"""
    ru_text = f"""
💳 Введите реквизиты на которые поступит вывод средств:\n
"""
    return ru_text if language == "ru" else eng_text


def withdraw_ordinary_text(language):
    eng_text = f"""
❌ Withdrawal of funds is possible only to those details from which the balance was replenished.
"""
    ru_text = f"""
❌ Вывод средств возможен только на те реквизиты, с которых пополнялся баланс.
"""
    return ru_text if language == "ru" else eng_text


def withdraw_error_text(language):
    eng_text = f"""
❌ An error occurred while withdrawing funds.
"""
    ru_text = f"""
❌ Произошла ошибка при выводе средств.
"""
    return ru_text if language == "ru" else eng_text


def withdraw_successful_text(language, sym, card, currency):
    eng_text = f"""
✅ Withdrawal of funds in the amount: <b>{sym}{currency_signs[currency]}.</b>\n
<i>Details to which funds will be received: {card}</i>
"""
    ru_text = f"""
✅ Вывод средств на сумму: <b>{sym}{currency_signs[currency]}.</b>\n
<i>Реквизиты на которые поступят средства: {card}</i>
"""
    return ru_text if language == "ru" else eng_text


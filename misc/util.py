import requests
from bs4 import BeautifulSoup
from random import randint


def parsing_coin_price(coin):
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    s = requests.Session()
    response = s.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")

    price = soup.find('span', class_="sc-f70bb44c-0 jxpCgO base-text").text

    return price


def pool_result(percent):
    i = randint(1, 100)
    return True if percent >= i else False


def optimization_text(text: str):
    text = text.split()
    text = [word.replace(".", "\\.")
            .replace("*", "\\*")
            .replace("_", "\\_")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("~", "\\~")
            .replace("`", "\\`")
            .replace(">", "\\>")
            .replace("<", "\\<")
            .replace("#", "\\#")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("=", "\\=")
            .replace("|", "\\|")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("!", "\\!") for word in text]
    return "".join(text)


def count_decimal_digits(number: float):
    _, decimal_part = str(number).split(".")
    return len(decimal_part)

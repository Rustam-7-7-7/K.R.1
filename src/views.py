import json

from src.utils import get_greeting, process_transactions, fetch_currency_data, fetch_stock_data


def main_page(date_time_str):
    ''' Функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
         и возвращающая JSON-ответ. '''

    # Получение приветствия
    greeting = get_greeting(date_time_str)

    # Обработка транзакций
    cards_info, top_transactions = process_transactions(date_time_str)

    # Загрузка пользовательских настроек
    with open('../user_settings.json', 'r') as f:
        user_settings = json.load(f)

    # Получение данных о валютах и акциях
    currency_rates = fetch_currency_data(user_settings['user_currencies'])
    stock_prices = fetch_stock_data(user_settings['user_stocks'])

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response, ensure_ascii=False)

# ПРОВЕРКА

# Пример строки с датой и временем, которая соответствует данным в файле
# test_datetime = "2021-10-10 17:30:00"
#
# # Вызов функции и вывод результата
# result = main_page(test_datetime)
# print(result)

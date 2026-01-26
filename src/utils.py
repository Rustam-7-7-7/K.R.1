import datetime
import pandas as pd
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()


def get_greeting(date_time_str):
    ''' Функция для получения приветствия. '''

    # Преобразование строки в объект datetime
    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Используем час из объекта datetime для определения приветствия
    current_hour = date_time_obj.hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def process_transactions(date_time_str):
    ''' Функция для обработки транзакций. '''
    # Загрузка данных из Excel
    df = pd.read_excel("../data/operations.xlsx")

    # Преобразование столбца 'Дата операции' в datetime с явным указанием формата
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

    # Фильтрация данных по датам
    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    start_date = date_time_obj.replace(day=1)
    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= date_time_obj)]

    # Обработка данных
    cards_info = []
    top_transactions = filtered_df.nlargest(5, 'Сумма операции с округлением').to_dict(orient='records')

    # Преобразование дат в строку
    for transaction in top_transactions:
        transaction['Дата операции'] = transaction['Дата операции'].strftime('%Y-%m-%d %H:%M:%S')

    for card_number, group in filtered_df.groupby('Номер карты'):
        total_spent = group['Сумма операции с округлением'].sum()
        cashback = total_spent / 100
        cards_info.append({
            "last_digits": str(card_number)[-4:],
            "total_spent": total_spent,
            "cashback": cashback
        })

    return cards_info, top_transactions


def fetch_currency_data(currencies):
    ''' Функция для получения данных о валютах. '''
    base_url = "https://api.exchangerate-api.com/v4/latest/RUB"
    currency_data = []
    for currency in currencies:
        try:
            response = requests.get(f"{base_url}{currency}")
            response.raise_for_status()
            rate = response.json()['rates'][currency]
            currency_data.append({
                "currency": currency,
                "rate": rate
            })
        except requests.RequestException as e:
            logging.error(f"API request for currency {currency} failed", exc_info=True)
    return currency_data


def fetch_stock_data(stocks):
    ''' Функция для получения данных об акциях. '''
    stock_data = []
    api_key = os.getenv("API_KEY")
    base_url = "https://www.alphavantage.co/query"  # Исправленный базовый URL
    for stock in stocks:
        try:
            response = requests.get(base_url, params={
                "function": "TIME_SERIES_DAILY",
                "symbol": stock,
                "apikey": api_key
            })
            response.raise_for_status()
            data = response.json()
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                latest_date = next(iter(time_series))
                price = float(time_series[latest_date]['4. close'])
                stock_data.append({
                    "stock": stock,
                    "price": price
                })
            else:
                logging.error(f"Time Series data not found for stock {stock}. Response: {data}")
        except requests.RequestException as e:
            logging.error(f"API request for stock {stock} failed", exc_info=True)
    return stock_data

import pandas as pd
import json
from datetime import datetime
import logging


def load_data_from_excel(file_path="../data/operations.xlsx"):
    ''' Функция для загрузки данных из Excel файла. '''

    data_frame = pd.read_excel(file_path)
    # Преобразование данных в список словарей
    data = data_frame.to_dict(orient='records')
    return data


def analyze_cashback(data, year, month):
    ''' Функция для подсчета кешбэка по категориям. '''

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    filtered_data = [
        transaction for transaction in data
        if datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').year == year
           and datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').month == month
    ]

    cashback_by_category = {}

    for transaction in filtered_data:
        category = transaction['Категория']
        cashback = float(transaction['Бонусы (включая кэшбэк)'])

        if category not in cashback_by_category:
            cashback_by_category[category] = 0
        cashback_by_category[category] += cashback

    logger.info(f"Analysis completed for {year}-{month}.")
    return json.dumps(cashback_by_category, ensure_ascii=False)


if __name__ == "__main__":
    # Загрузка данных только при выполнении скрипта напрямую
    transactions = load_data_from_excel()

# Вызов функции анализа
# result = analyze_cashback(transactions, 2021, 12)
# print(result)

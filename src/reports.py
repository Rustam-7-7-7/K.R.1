import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def save_to_file(filename="default_report.json"):
    ''' Декоратор для записи результата в файл. '''

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Преобразуем DataFrame в словарь
            result_dict = result.to_dict(orient='records')
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(result_dict, file, ensure_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@save_to_file(filename="category_spending_report.json")
def spending_by_category(category: str, date: Optional[str] = None,
                         file_path: str = '../data/operations.xlsx') -> pd.DataFrame:
    ''' Функция для расчета трат по категории. '''

    # Загрузка данных из файла Excel
    transactions = pd.read_excel(file_path)

    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    # Преобразуем строки в столбце 'Дата операции' в datetime объекты
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    # Рассчитываем дату трех месяцев назад
    start_date = date - timedelta(days=90)

    # Фильтруем транзакции по категории и по датам
    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
        ]

    # Рассчитываем сумму трат
    total_spending = filtered_transactions['Сумма операции'].sum()

    # Логируем результат
    logging.info(f"Total spending for category '{category}' from {start_date} to {date} is {total_spending}")

    # Возвращаем результат в виде датафрейма
    return pd.DataFrame({'category': [category], 'total_spending': [total_spending]})

# Пример использования функции
# if __name__ == "__main__":
#     report = spending_by_category('Супермаркеты', '2022-03-31')
#     print(report)

import unittest
from unittest.mock import patch, Mock
import pandas as pd
import os
from src.utils import get_greeting, process_transactions, fetch_currency_data, fetch_stock_data


class TestFunctions(unittest.TestCase):

    # Тест для функции get_greeting
    def test_get_greeting(self):
        test_cases = [
            ("2023-10-17 06:00:00", "Доброе утро"),
            ("2023-10-17 13:00:00", "Добрый день"),
            ("2023-10-17 19:00:00", "Добрый вечер"),
            ("2023-10-17 23:00:00", "Доброй ночи"),
        ]

        for date_str, expected in test_cases:
            with self.subTest(date_str=date_str, expected=expected):
                self.assertEqual(get_greeting(date_str), expected)

    # Тест для функции process_transactions
    @patch('pandas.read_excel')
    def test_process_transactions(self, mock_read_excel):
        # Создаем фиктивные данные для теста
        data = {
            'Дата операции': ['01.10.2023 10:00:00', '15.10.2023 12:00:00', '20.10.2023 14:00:00'],
            'Номер карты': ['1234567890123456', '1234567890123456', '6543210987654321'],
            'Сумма операции с округлением': [1000, 2000, 1500]
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df

        date_time_str = "2023-10-20 15:00:00"
        cards_info, top_transactions = process_transactions(date_time_str)

        self.assertEqual(len(cards_info), 2)
        self.assertLessEqual(len(top_transactions), 5)  # Проверка, что транзакций не больше 5

    # Тест для функции fetch_currency_data
    @patch('requests.get')
    def test_fetch_currency_data(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'rates': {'USD': 75.0}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        currencies = ["USD"]
        currency_data = fetch_currency_data(currencies)

        self.assertEqual(len(currency_data), 1)
        self.assertEqual(currency_data[0]['currency'], 'USD')
        self.assertEqual(currency_data[0]['rate'], 75.0)

    # Тест для функции fetch_stock_data
    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY": "test_api_key"})
    def test_fetch_stock_data(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                "2023-10-20": {'4. close': '150.00'}
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        stocks = ["AAPL"]
        stock_data = fetch_stock_data(stocks)

        self.assertEqual(len(stock_data), 1)
        self.assertEqual(stock_data[0]['stock'], 'AAPL')
        self.assertEqual(stock_data[0]['price'], 150.0)

import unittest
from unittest.mock import patch, mock_open
import json
from src.views import main_page


class TestMainPageFunction(unittest.TestCase):

    @patch('src.views.get_greeting')
    @patch('src.views.process_transactions')
    @patch('src.views.fetch_currency_data')
    @patch('src.views.fetch_stock_data')
    def test_main_page(self, mock_fetch_stock_data, mock_fetch_currency_data, mock_process_transactions,
                       mock_get_greeting):
        # Настройка mock-объектов
        mock_get_greeting.return_value = "Hello"
        mock_process_transactions.return_value = ({"card1": "info"}, ["transaction1", "transaction2"])
        mock_fetch_currency_data.return_value = {"USD": 1.0, "EUR": 0.9}
        mock_fetch_stock_data.return_value = {"AAPL": 150, "GOOGL": 2800}

        # Замена чтения файла с настройками
        mock_user_settings = {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "GOOGL"]
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_user_settings))):
            result = main_page("2023-10-05 14:30:00")

        # Ожидаемый результат
        expected_result = json.dumps({
            "greeting": "Hello",
            "cards": {"card1": "info"},
            "top_transactions": ["transaction1", "transaction2"],
            "currency_rates": {"USD": 1.0, "EUR": 0.9},
            "stock_prices": {"AAPL": 150, "GOOGL": 2800}
        }, ensure_ascii=False)

        # Проверка результата
        self.assertEqual(result, expected_result)

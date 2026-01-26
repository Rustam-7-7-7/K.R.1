import pytest
from unittest.mock import patch, MagicMock
from src.services import analyze_cashback, load_data_from_excel
import json


@pytest.fixture
def mock_data():
    return [
        {'Дата операции': '31.12.2021 16:44:00', 'Категория': 'Супермаркеты', 'Бонусы (включая кэшбэк)': '3.00'},
        {'Дата операции': '31.12.2021 16:42:04', 'Категория': 'Супермаркеты', 'Бонусы (включая кэшбэк)': '1.00'},
        {'Дата операции': '31.12.2021 15:44:39', 'Категория': 'Различные товары', 'Бонусы (включая кэшбэк)': '5.00'},
    ]


@pytest.mark.parametrize("year, month, expected", [
    (2021, 12, json.dumps({'Супермаркеты': 4.0, 'Различные товары': 5.0}, ensure_ascii=False)),
    (2021, 11, json.dumps({}, ensure_ascii=False)),  # Нет данных за ноябрь
])
def test_analyze_cashback(mock_data, year, month, expected):
    result = analyze_cashback(mock_data, year, month)
    assert result == expected


@patch('src.services.pd.read_excel')
def test_load_data_from_excel(mock_read_excel):
    mock_read_excel.return_value = MagicMock()
    mock_read_excel.return_value.to_dict.return_value = [{'some_key': 'some_value'}]

    data = load_data_from_excel("dummy_path")
    assert data == [{'some_key': 'some_value'}]
    mock_read_excel.assert_called_once_with("dummy_path")

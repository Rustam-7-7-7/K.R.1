import pytest
from unittest.mock import patch, mock_open
import pandas as pd
from src.reports import spending_by_category


# Фикстура для создания тестового датафрейма
@pytest.fixture
def transactions():
    # Создаем датафрейм с тестовыми данными
    return pd.DataFrame({
        'Дата операции': ['01.01.2022 10:00:00', '15.02.2022 12:00:00', '01.03.2022 14:00:00'],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Развлечения'],
        'Сумма операции': [-100.0, -200.0, -150.0]
    })


# Тест функции spending_by_category с использованием patch и mock
@patch("builtins.open", new_callable=mock_open)
@patch("src.reports.pd.read_excel")
@pytest.mark.parametrize("category, date, expected_total", [
    ('Супермаркеты', '2022-03-31', -300.0),  # Тестируем категорию "Супермаркеты" с заданной датой
    ('Развлечения', '2022-03-31', -150.0),  # Тестируем категорию "Развлечения"
    ('Супермаркеты', '2022-01-15', -100.0),  # Проверяем случай, когда дата ограничивает выборку
])
def test_spending_by_category(mock_read_excel, mock_open, transactions, category, date, expected_total):
    # Настраиваем mock для read_excel, чтобы он возвращал наш тестовый датафрейм
    mock_read_excel.return_value = transactions

    # Вызываем тестируемую функцию
    result = spending_by_category(category, date)

    # Проверяем, что сумма трат соответствует ожидаемой
    assert result['total_spending'].iloc[0] == expected_total

    # Проверяем, что файл был открыт и в него была записана информация
    mock_open.assert_called_once_with("category_spending_report.json", 'w', encoding='utf-8')

from src.views import main_page
from src.services import analyze_cashback, load_data_from_excel
from src.reports import spending_by_category


def main():
    ''' Функция, запустив которую, можно получить результат всех
         реализованных в проекте функциональностей. '''

    # Пример строки с датой и временем, которая соответствует данным в файле
    test_datetime = "2021-10-10 17:30:00"

    # Вызов функции и вывод результата
    result = main_page(test_datetime)
    print(result)

    # Загрузка данных
    transactions = load_data_from_excel()

    # Вызов функции анализа и вывод результата
    result = analyze_cashback(transactions, 2021, 12)
    print(result)

    # Вызов функции и вывод результата
    report = spending_by_category('Супермаркеты', '2022-03-31')
    print(report)


main()

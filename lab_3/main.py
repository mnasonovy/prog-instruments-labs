import re
import csv
import json

from typing import List
from checksum import calculate_checksum, serialize_result

VALIDATORS = {
    "email": re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    "height": re.compile(r'^\d\.\d{2}$'),
    "inn": re.compile(r'^\d{12}$'),
    "passport": re.compile(r'^\d{2} \d{2} \d{6}$'),
    "occupation": re.compile(r'^[а-яА-ЯёЁa-zA-Z]+(-[а-яА-ЯёЁa-zA-Z]+)*$'),
    "latitude": re.compile(r'^-?\d+(\.\d+)?$'),
    "hex_color": re.compile(r'^#[0-9a-fA-F]{6}$'),
    "issn": re.compile(r'^\d{4}-\d{4}$'),
    "uuid": re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'),
    "time": re.compile(r'^([01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$')
}

def validate_row(row: List[str], headers: List[str]) -> bool:
    """
    Проверяет, соответствует ли строка формату, определенному регулярными выражениями.
    :param row: Данные строки
    :param headers: Заголовки столбцов
    :return: True, если строка валидна, иначе False
    """
    for column, value in zip(headers, row):
        if column in VALIDATORS:
            if not VALIDATORS[column].fullmatch(value):
                return False
    return True

def find_invalid_rows(csv_path: str) -> List[int]:
    """
    Находит номера невалидных строк в CSV-файле.
    :param csv_path: Путь к CSV-файлу
    :return: Список номеров невалидных строк
    """
    invalid_rows = []
    with open(csv_path, 'r', encoding='utf-16') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)  
        for i, row in enumerate(reader):
            if not validate_row(row, headers):
                invalid_rows.append(i)  
    return invalid_rows

def save_to_json(variant: int, checksum: str, output_path: str = 'lab_3/result.json') -> None:
    """
    Сохраняет номер варианта и контрольную сумму в JSON файл.
    :param variant: Номер варианта
    :param checksum: Контрольная сумма
    :param output_path: Путь к JSON файлу
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


def load_from_json(input_path: str = 'lab_3/result.json') -> dict:
    """
    Загружает данные из JSON файла.
    :param input_path: Путь к JSON файлу
    :return: Словарь с данными
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

if __name__ == "__main__":
    result = load_from_json('lab_3/result.json')
    if result:
        print(f"Загруженные данные: Вариант - {result['variant']}, Контрольная сумма - {result['checksum']}")
    else:
        print("Данные не найдены. Создадим новый файл.")

    csv_path = 'lab_3/79.csv'

    invalid_rows = find_invalid_rows(csv_path)
    print(f"Найдено {len(invalid_rows)} невалидных строк.")

    checksum = calculate_checksum(invalid_rows)
    print(f"Контрольная сумма: {checksum}")

    variant = 79
    save_to_json(variant, checksum)
    print("Результат сохранен в result.json.")

import re
import csv
import json
from typing import List

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


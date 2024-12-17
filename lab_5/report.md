# Отчет по лабораторной работе №2 <br> "Статистический анализ псевдослучайных последовательностей"

## 1. Генерация случайных последовательностей на С++ и Java

Сначала были сгенерированы два 128-битных массива средствами языков C++ и Java:

1) C++ последовательность(random_sequence_cc.txt): 00000011101100000110011100101000000101100000000000101110010011100000111100010010010110011100010010010001000100111011011101100111

2) Java последовательность(random_sequence_java.txt): 10110001111001010100111001101011000100011100100111011101011100000011100010011110010101110111000011101010100111011001010001110001

## 2. Проверка NIST тестами

Полученные последовательности были проанализированы с помощью трех тестов NIST
Частотный побитовый тест.
Тест на одинаковые подряд идущие биты.
Тест на самую длинную последовательность единиц в блоке.

Тесты находятся в файле "NIST_tests.py".
Результат: 
| № теста|C++   |Java  |
|--------|------|------|
|1       |0.5959|0.2888|
|2       |0.0544|0.6477|
|3       |0.1286|0.0389|


## 3. Вывод
Было написано два ГСПЧ, с помощью которых сгенерированы битовые последовательности. На основе результатов тестов можно сделать вывод, что последовательности являются случайными.
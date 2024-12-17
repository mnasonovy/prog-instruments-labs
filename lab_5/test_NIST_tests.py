import pytest
from unittest.mock import mock_open, patch
from NIST_tests import (
    read_sequence_from_file,
    write_results_to_file,
    frequency_bitwise_test,
    same_bits_test,
    longest_ones_sequence_test
)

# Базовые тесты

def test_read_sequence_from_file():
    mock_file_content = "1010101010"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        sequence = read_sequence_from_file("mockfile.txt")
        assert sequence == "1010101010", "Failed to read sequence correctly."

def test_write_results_to_file():
    results = {"Test1": 0.95, "Test2": 0.87}
    with patch("builtins.open", mock_open()) as mocked_file:
        write_results_to_file("output.txt", results)
        mocked_file().write.assert_any_call("Test1: 0.95\n")
        mocked_file().write.assert_any_call("Test2: 0.87\n")

def test_frequency_bitwise_test():
    sequence = "110011"
    result = frequency_bitwise_test(sequence)
    assert 0 <= result <= 1, "P-value out of range."

def test_same_bits_test():
    sequence = "110011"
    result = same_bits_test(sequence)
    assert 0 <= result <= 1, "P-value out of range."

# Продвинутые тесты

@pytest.mark.parametrize("sequence,expected_condition", [
    ("11001100", lambda result: 0 <= result <= 1),  
    ("10101010", lambda result: 0 <= result <= 1),  
    ("11001100", lambda result: 0 <= result <= 1)   
])
def test_same_bits_test_parametrized(sequence, expected_condition):
    result = same_bits_test(sequence)
    assert expected_condition(result), f"Unexpected result for sequence: {sequence}"

def test_longest_ones_sequence_test():
    sequence = "111100001111"
    pi_constants = [0.2148, 0.3672, 0.2305, 0.1875]
    result = longest_ones_sequence_test(sequence, pi_constants)
    assert 0 <= result <= 1, "P-value out of range."

def test_read_sequence_file_mocked():
    mock_file_content = "1010111100\n"
    with patch("builtins.open", mock_open(read_data=mock_file_content)) as mocked_file:
        sequence = read_sequence_from_file("mockfile.txt")
        mocked_file.assert_called_once_with("mockfile.txt", "r")
        # Ожидаем, что последовательность будет объединена в одну строку
        assert sequence == "1010111100", f"Expected '1010111100', but got {sequence}"

import math
import json
import os
import mpmath

from typing import List  
from scipy.special import gammainc


def read_sequence_from_file(filename: str) -> str:
    """
    Read a sequence of bytes from a file.

    Parameters:
        filename (str): The name of the file to read.

    Returns:
        str: The sequence of bytes read from the file.
    """
    try:
        with open(filename, 'r') as file:
            sequence = file.read().strip()
        return sequence
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")


def write_results_to_file(filename: str, results: dict):
    """
    Write test results to a file.

    Parameters:
        filename (str): The name of the file to write to.
        results (dict): A dictionary containing test names as keys and their corresponding results as values.
    """
    try:
        with open(filename, 'w') as file:
            for test, result in results.items():
                file.write(f"{test}: {result}\n")
    except IOError:
        print(f"Error: Unable to write to file '{filename}'.")

                 
def frequency_bitwise_test(sequence: str) -> float:
    """
    Calculate the P value for the frequency bitwise test of a sequence.

    Parameters:
        sequence (str): Sequence of bytes.

    Returns:
        float: The P value.
    """
    N = len(sequence)
    sum_bits = sum(1 if bit == '1' else -1 for bit in sequence)
    P = sum_bits / math.sqrt(N)
    P = math.erfc(P / math.sqrt(2))
    return P


def same_bits_test(sequence: str) -> float:
    """
    Calculate the P value for the test of same consecutive bits in a sequence.

    Parameters:
        sequence (str): Sequence of bits.

    Returns:
        float: The P value.
    """
    N = len(sequence)
    sum_bits = sum(int(bit) for bit in sequence)
    sigma = sum_bits / N
    if not abs(sigma - 0.5) < (2 / math.sqrt(N)):
        return 0 
    Vn = sum(1 for i in range(len(sequence) - 1) if sequence[i] != sequence[i + 1])
    P = math.erfc(abs(Vn - 2 * N * sigma * (1 - sigma)) / (2 * math.sqrt(2 * N) * sigma * (1 - sigma)))
    return P


def longest_ones_sequence_test(sequence: str, consts_PI: List[float]) -> float:
    """
    Calculate the P value for the test of the longest sequence of ones in a block.

    Parameters:
        sequence (str): Sequence of bits.
        consts_PI (List[float]): List of constants for the test.

    Returns:
        float: The P value.
    """
    block_length = 8
    v = {1: 0, 2: 0, 3: 0, 4: 0}
    hi_2 = 0
    for block_start in range(0, len(sequence), block_length):
        block = sequence[block_start:block_start + block_length]
        max_length, length = 0, 0
        for bit in block:
            if bit == '1':
                length += 1
                max_length = max(max_length, length)
            else:
                length = 0
        match max_length:
            case 0 | 1:
                v[1] += 1
            case 2:
                v[2] += 1
            case 3:
                v[3] += 1
            case _:
                v[4] += 1
    for i in range(4):
        hi_2 += ((v[i + 1] - 16 * consts_PI[i]) ** 2) / (16 * consts_PI[i])
    P = mpmath.gammainc(3 / 2, hi_2 / 2)
    return P


def run_tests_and_write_results(input_filename: str, output_filename: str, pi_constants: list):
    """
    Run tests on a sequence and write the results to a file.

    Parameters:
        input_filename (str): The name of the file containing the input sequence.
        output_filename (str): The name of the file to write the test results to.
        pi_constants (list): A list containing constants for the tests.
    """
    sequence = read_sequence_from_file(input_filename)
    frequency_result = frequency_bitwise_test(sequence)
    same_bits_result = same_bits_test(sequence)
    longest_ones_result = longest_ones_sequence_test(sequence, pi_constants)

    results = {
        "Frequency Bitwise Test": frequency_result,
        "Same Bits Test": same_bits_result,
        "Longest Ones Sequence Test": longest_ones_result
    }
    write_results_to_file(output_filename, results)
    
    
def main():
    try:
        with open(os.path.join('settings.json'), 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)
            pi_constants = settings["consts_PI"]
    except FileNotFoundError:
        print("Error: Settings file 'settings.json' not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON in settings file 'settings.json'.")
        return

    input_filenames = [settings.get('cc_sequence_intput'), settings.get('java_sequence_intput')]
    output_filenames = [settings.get('cc_sequence_output'), settings.get('java_sequence_output')]

    if None in input_filenames or None in output_filenames:
        print("Error: Missing input or output file names in settings.")
        return

    for input_filename, output_filename in zip(input_filenames, output_filenames):
        run_tests_and_write_results(input_filename, output_filename, pi_constants)


if __name__ == "__main__":
    main()

#include <iostream>
#include <fstream>
#include <bitset>
#include <random>
#include <windows.h>

/**
 * Check if a directory exists.
 * @param path: The path of the directory to check.
 * @return: True if the directory exists, false otherwise.
 */
bool directoryExists(const std::wstring& path) {
    DWORD attributes = GetFileAttributesW(path.c_str());
    return (attributes != INVALID_FILE_ATTRIBUTES && (attributes & FILE_ATTRIBUTE_DIRECTORY));
}

/**
 * Generate a random bit sequence and save it to a file.
 * @param filepath: The path to the file where the random sequence will be saved.
 */
void generateRandomSequence(const std::wstring& filepath) {
    std::wstring directory = filepath.substr(0, filepath.find_last_of(L"/\\"));
    if (!directoryExists(directory)) {
        if (!CreateDirectoryW(directory.c_str(), NULL)) {
            std::cerr << "Failed to create directory\n";
            return;
        }
    }
    std::random_device rd;
    std::mt19937 generator(rd());
    std::ofstream outFile(filepath);
    if (!outFile) {
        std::cerr << "The file could not be opened for writing\n";
        return;
    }
    std::bitset<128> randomSequence;
    for (int j = 0; j < 128; ++j) {
        randomSequence[j] = generator() % 2; 
    }
    outFile << randomSequence;
    outFile.close();
}

int main() {
    std::wstring filepath = L"C:\\Users\\79297\\Desktop\\isb\\lab_2\\random_sequence_cc.txt";
    generateRandomSequence(filepath);
    
    return 0;
}

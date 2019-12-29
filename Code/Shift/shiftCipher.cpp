#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

#include "utils.cpp"

using namespace std::string_literals;
using iter = std::istreambuf_iterator<char>;

auto codeCharacter(char letter, int key) -> char { return letter + key; }
auto decodeCharacter(char letter, int key) -> char { return letter - key; }
auto decodeCharacter2(char letter, int inverse_key) -> char { return letter + inverse_key; }

auto encode(const std::string& plain, unsigned int key) -> std::string {
  auto encoded = std::string {plain};
  for (auto& letter : encoded) letter = codeCharacter(letter, key);

  return encoded;
}

auto decode(const std::string& encoded, unsigned int key, bool IcanSubtract = true) -> std::string {
  auto plain = std::string {encoded};

  auto inverse = ([key]() -> char {
    // return  256 - key;

    for (int i = 0; i <= 256; ++i) {
      auto possible_inverse = static_cast<char>(i);
      if (key + possible_inverse == 0) return possible_inverse;
    }

    return '0';
  })();

  for (auto& letter : plain) {
    letter = IcanSubtract? decodeCharacter(letter, key) : decodeCharacter2(letter, inverse);
  }

  return plain;
}

auto main(int argc, char* argv[]) -> int {
  const auto isEncrypting = getOrDefault(argc, argv, 1, "none"s) == "encrypt"s;
  const auto key = [&]() {
    try {
      auto key = std::stoi(getOrDefault(argc, argv, 2, "3"s));
      if (key < 0 or key > 255) throw std::invalid_argument("Invalid key");
      return key;
    } catch (const std::invalid_argument& error) {
      std::cout << "Error with the key: " << error.what() << std::endl;
      std::exit(0);
    }
  }();

  auto input = std::ifstream {};
  input.open(getOrDefault(argc, argv, 3, isEncrypting ? "m.txt"s : "c.txt"s));
  if (input.fail()) {
    std::cout << "Error: input file not found" << std::endl;
    std::exit(1);
  }

  const auto data = std::string {iter(input), iter()};
  const auto result = isEncrypting ? encode(data, key) : decode(data, key, true);

  auto output = std::ofstream {};
  output.open(getOrDefault(argc, argv, 4, isEncrypting ? "c.txt"s : "m.txt"s));
  output << result;

  return 0;
}
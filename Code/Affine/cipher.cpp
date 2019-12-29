#include <string>

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

#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>

using namespace std;

template <size_t T = 64>
auto print_bin(const uint64_t data) {
  cout << bitset<T> {data} << endl;
}

auto print_hex(const uint64_t data) { cout << hex << data << endl; }

auto print_bin_spaces(const uint64_t data, const char separator = ' ') {
  auto to_show = bitset<64> {data}.to_string();

  for (auto it = begin(to_show); distance(it, end(to_show)) > (4 + 2); ++it) {
    advance(it, 4);
    it = to_show.insert(it, separator);
  }

  cout << to_show << endl;
}

template <typename num = uint64_t>
auto create_number(string key_text) -> num {
  union key_t {
    char text[sizeof(num)];
    num id;
  };

  std::reverse(begin(key_text), end(key_text));

  auto key = key_t {};
  strcpy(key.text, key_text.c_str());

  return key.id;
}

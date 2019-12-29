#include <array>
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>

#include "Utility.cpp"
#include "Permutation.cpp"

using namespace std;

template <size_t num_bits>
auto right_rotate(const bitset<num_bits> data, int times) {
  auto result = bitset<num_bits> {};

  for (int i = 0; i < num_bits; i++) {
    result[(num_bits + i - times) % num_bits] = data[i];
  }

  return result;
}

auto generate_key(const uint64_t initial_key, const int key_id) {
  constexpr static array<uint8_t, 16> rounds {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

  cout << "initial_key" << endl;
  print_bin(initial_key);

  cout << "PC 1" << endl;
  const auto permuted_message = permute_endian<64, 56>(initial_key, permuted_choice_1);
  print_bin<56>(permuted_message);
  print_hex(permuted_message);

  const auto data = bitset<56> {permuted_message};
  auto Cn = bitset<28> {0}, Dn = bitset<28> {0};

  auto index = 56;
  for (auto i = 27; i >= 0; i--) Cn[i] = data[--index];
  for (auto i = 27; i >= 0; i--) Dn[i] = data[--index];

  cout << "Cn_num" << endl;
  print_bin<28>(Cn.to_ullong());

  cout << "Dn_num" << endl;
  print_bin<28>(Dn.to_ullong());

  const auto times_to_rotate = accumulate(begin(rounds), begin(rounds) + key_id, 0);
  cout << "times_to_rotate: " << dec << times_to_rotate << endl;

  Cn = right_rotate<28>(Cn, times_to_rotate);
  Dn = right_rotate<28>(Dn, times_to_rotate);

  cout << "Cn_num" << endl;
  print_bin<28>(Cn.to_ullong());

  cout << "Dn_num" << endl;
  print_bin<28>(Dn.to_ullong());

  auto result = Cn.to_ullong();
  result = (result << 28) | Dn.to_ullong();

  cout << "Union" << endl;
  print_bin<56>(result);

  result = permute_endian<56, 48>(result, permuted_choice_2);

  cout << "PC 2" << endl;
  print_bin<48>(result);

  return result;
}

auto main() -> int {
  //const auto key = create_number("Asegurar");
  const auto key = 0b00010011'00110100'01010111'01111001'10011011'10111100'11011111'11110001;
  const auto result = generate_key(key, 8);

  cout << hex << result << endl;
}

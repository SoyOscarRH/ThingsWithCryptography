#include <bitset>
#include <cstdint>
#include <iostream>
#include <string>

using namespace std;

template <int T = 8>
class binary_field {
 private:
  constexpr static auto elements = 2 * T;
  bitset<elements> data;

  template <typename num>
  constexpr static auto get_most_significant_bit(num n) {
    if (n == 0) return 0;

    auto most_significant_bit = 0;
    while (n != 0) {
      n = n >> 1;
      ++most_significant_bit;
    }

    return most_significant_bit - 1;
  }

 public:
  binary_field(uint32_t literal) : data {literal} {}
  auto get_data() const { return data.to_ulong(); }

  constexpr friend auto operator+(binary_field lhs, const binary_field& rhs) {
    const auto me = lhs.get_data(), other = rhs.get_data();
    lhs.data = bitset<elements> {me xor other};

    return lhs;
  }

  constexpr friend auto operator*(binary_field lhs, const binary_field& rhs) {
    auto result = uint32_t {};
    for (auto i = elements - 1; i >= 0; --i) {
      const auto current = rhs.data[i];
      if (not current) continue;

      const auto original = lhs.get_data();
      const auto me = result;

      result = (original << i) xor me;
    }

    while (get_most_significant_bit(result) >= T) {
      const auto left_over = result >> 8;

      // cout << binary_field {result} << " <- result" << endl;
      // cout << binary_field {left_over} << " <- left" << endl;

      const auto bit1 = left_over << 0, bit2 = left_over << 1;
      const auto bit3 = left_over << 3, bit4 = left_over << 4, bit5 = left_over << 8;

      result = result xor bit1 xor bit2 xor bit3 xor bit4 xor bit5;
    }

    return binary_field {result};
  }

  constexpr friend ostream& operator<<(ostream& os, const binary_field<T>& me) {
    auto turned_on = me.data.count();
    if (not turned_on) os << "0";

    os << me.data.to_string() << " ";
    os << hex << me.data.to_ulong() << "\t" << dec;

    for (auto i = elements - 1; i >= 0; --i) {
      const auto current = me.data[i];
      if (not current) continue;

      --turned_on;

      if (i != 0) {
        os << "x^" << static_cast<int>(i);
        if (turned_on) os << " + ";
      } else
        os << "1";
    }

    return os;
  }
};

auto main() -> int {
  const auto a = binary_field<8> {0x57};
  const auto b = binary_field<8> {0x13};

  cout << a * b << endl;
}

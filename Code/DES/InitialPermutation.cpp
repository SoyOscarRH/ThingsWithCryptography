#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>

#include "Utility.cpp"
#include "Permutation.cpp"

auto main() -> int {
  const auto message = 0x0123456789ABCDEFull;
  constexpr auto num_bits = 64;
  //const auto message =  create_number("Diamante");

  cout << "initial input" << endl;
  print_bin_spaces(message);

  cout << endl << "permuted" << endl;
  auto permuted_message = permute<num_bits>(message, initial_permutation);
  print_bin_spaces(permuted_message);

  cout << endl << "recovered" << endl;
  auto recovered_message = permute<num_bits>(permuted_message, final_permutation);
  print_bin_spaces(recovered_message);

  return 0;
}
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>

#include "cipher.cpp"
#include "modularInverse.cpp"
#include "utils.cpp"

using number = int;
using namespace std::string_literals;
using iter = std::istreambuf_iterator<char>;

auto main(int argc, char* argv[]) -> int {
  while (true) {
    number mod = 0;
    cout << "Give a mod to work with: ";
    cin >> mod;
    if (mod < 0) {
      cout << "Invalid mod" << endl;
      continue;
    }

    number beta = 0;
    cout << "Give a beta to work with: ";
    cin >> beta;
    if (beta < 0 or beta > mod) {
      cout << "Invalid beta" << endl;
      continue;
    }

    number alpha = 0;
    cout << "Give a alpha to work with: ";
    cin >> alpha;
    if (std::gcd(alpha, mod) != 1) {
      cout << "Invalid key: beta do not have inverse" << endl;
      continue;
    }

    std::cout << "alpha: " << alpha << endl;
    std::cout << "beta: " << alpha << endl << endl;
    std::cout << "inverse of beta: " << endl;

    auto inverse = modularInverse(alpha, mod);

    std::cout << "so inverse is: " << inverse << endl;

    break;
  }

  return 0;
}
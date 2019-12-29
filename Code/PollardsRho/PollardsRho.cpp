#include <cmath>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

class PollardsRho {
 private:
  int alpha, beta, mod, zn;

  struct step {
    int x, a, b;
  };

  enum class S { class_1, class_2, class_3 };

  auto modularBinaryExponentation(int base, int exponent, int n) {
    auto solution = 1;
    base = base % n;

    while (exponent > 0) {
      if (exponent & 1) solution = (base * solution) % n;

      base = (base * base) % n;
      exponent = exponent >> 1;
    }

    return solution;
  }

  auto get_s_value(int xi) -> S {
    switch (xi % 3) {
      case 0: return S::class_2;
      case 1: return S::class_1;
      case 2: return S::class_3;
    }
  }

  auto get_next(step current) -> step {
    auto [xi, ai, bi] = current;

    switch (get_s_value(xi)) {
      case S::class_1: return {(beta * xi) % zn, ai, (bi + 1) % mod};
      case S::class_2: return {(xi * xi) % zn, (2 * ai) % mod, (2 * bi) % mod};
      case S::class_3: return {(alpha * xi) % zn, (ai + 1) % mod, bi};
    }
  }

 public:
  PollardsRho(int alpha, int beta, int mod, int zn)
      : alpha {alpha}, beta {beta}, mod {mod}, zn {zn} {}

  auto find_same_step() -> pair<step, step> {
    auto current = step {1, 0, 0};
    auto seen = vector<step> {current};

    auto i = 0;

    for (i = 0; not(i and i % 2 == 0 and seen[i / 2].x == current.x); ++i) {
      current = get_next(current);
      cout << i + 1 << ": \t" << current.x << "\t" << current.a << "\t" << current.b << endl;
      seen.push_back(current);
    }

    return {seen[i / 2], current};
  }

  auto find_log() {
    const auto [step_i, step_2i] = find_same_step();
    const auto [x_i, a_i, b_i] = step_i;
    const auto [x_2i, a_2i, b_2i] = step_2i;

    const auto r = (mod + ((b_i - b_2i) % mod)) % mod;
    if (not r) {
      cout << "error" << endl;
      exit(1);
    }

    const auto inv_r = modularBinaryExponentation(r, mod - 2, mod);
    const auto x = (mod + ((a_2i - a_i) % mod)) % mod;
    return (x * inv_r) % mod;
  }
};

auto main() -> int {
  auto solution = PollardsRho {2, 228, 191, 383}.find_log();
  cout << "solution " << solution << endl;

  return 0;
}
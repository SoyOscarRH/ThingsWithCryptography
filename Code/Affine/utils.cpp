template <typename T>
auto getOrDefault(int argc, char** argv, int index, T&& value) -> T{
  if (argc - 1 < index)
    return std::move(value);
  else
    return argv[index];
}
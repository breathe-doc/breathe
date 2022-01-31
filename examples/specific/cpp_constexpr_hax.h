[[nodiscard]] constexpr static auto f1(std::false_type) {}
[[nodiscard]] static constexpr auto f2(std::false_type) {}

constexpr static int v1 = 42;
static constexpr int v2 = 42;

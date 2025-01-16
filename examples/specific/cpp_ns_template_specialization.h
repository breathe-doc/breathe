namespace ns1 {
struct Foo {
  int value;
};
} // namespace ns1

namespace ns2 {
template <class U> struct Trait {
  static constexpr bool valid = false;
};

template <> struct Trait<ns1::Foo> {
  static constexpr bool valid = true;
};
} // namespace ns2

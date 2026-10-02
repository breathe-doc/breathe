namespace mylib {

/** A type. */
struct A {};

/** Another type. */
struct B {};

}

namespace std {

/** Hash function for mylib::A. */
template <>
struct hash<mylib::A> {};

/** Hash function for mylib::B. */
template <>
struct hash<mylib::B> {};

}

/*! \file cpp_trailing_return_type.h */

/*! needed for references in global function return type */
class Thingy {};

//! \brief Function that creates a thingy.
auto f_issue_441() -> Thingy*;

//
// When declaring a type using a "using" directive inside a namespace,
// Doxygen adds a spurious "typedef" in the corresponding XML definition
//
// $ doxygen --version
// 1.8.11
//

namespace foo {
using foo_int = int; // <definition>using foo::foo_int = typedef int</definition>
}

using global_int = int; // <definition>using global_int =  int</definition>

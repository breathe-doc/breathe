#include "../one/Util.h"

namespace test {

typedef int MyInt;

struct TestStruct {};

}

/// The non-type template parameter references a different file
template <TestClass::Enum E> void TestTemplateFunction();


class TypeDefTest {
};

/* A dummy typedef */
typedef TypeDefTest (*TypeDefTestFuncPtr)(void);

typedef void* (*voidFuncPtr)(float, int);

typedef void* voidPointer;

typedef float* floatPointer;

typedef float floatingPointNumber;

typedef int TestTypedef;

namespace TypeDefNamespace {
  typedef char *AnotherTypedef;
}

class TestClass {
 public:
  /** A typedef defined in a class. */
  typedef void *MemberTypedef;

  typedef void (*MemberTypedefFuncPointer)(int, double);
};

using TypeAlias = int;

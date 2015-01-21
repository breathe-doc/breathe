
class TypeDefTest {
};

/* A dummy typedef */
typedef TypeDefTest (*TypeDefTestFuncPtr)(void);

typedef void* (*voidFuncPtr)(float, int);

typedef void* voidPointer;

typedef float* floatPointer;

typedef float floatingPointNumber;

typedef int TestTypedef;

namespace testnamespace {
  typedef char *AnotherTypedef;
}

class TestClass {
 public:
  /** A typedef defined in a class. */
  typedef void *MemberTypedef;
};

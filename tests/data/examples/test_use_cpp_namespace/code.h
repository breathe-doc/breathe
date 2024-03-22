
#define SOME_MACRO 1

class ClassA {};

namespace Namespace {
    int var;

    class ClassB {
    public:
        void SomeFunc();

        struct NestedStruct {
            enum SomeEnum { VALUE1, VALUE2, VALUE3};
        };
    };

    using SomeType = ClassB::NestedStruct;

    template<typename T> concept SomeConcept = requires(T t) { t + t; };
}

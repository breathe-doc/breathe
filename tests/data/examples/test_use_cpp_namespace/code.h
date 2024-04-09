
#define SOME_MACRO 1

class ClassA {};

namespace Namespace {
    int Var;

    class ClassB {
    public:
        void SomeFunc();
        char MemberVar;

        struct NestedStruct {
            enum SomeEnum { VALUE1, VALUE2, VALUE3};
        };

        template<typename T> concept NestedConcept = requires(T t) { t(); };
    };

    using SomeType = ClassB::NestedStruct;

    template<typename T> concept SomeConcept = requires(T t) { t + t; };

    template<SomeConcept T> class ClassC {
        float SpecialVarA;
    };

    template<> class ClassC<unsigned long> {
        int SpecialVarA;
        float SpecialVarB;
    };
}


namespace foo {

    /** This appears in the documentation */
    class Bar {

        /** This appears as a sub class */
        class InnerBar {};

    };

    /** This also appears */
    int baz();

    /** More examples in a nested namespace */
    namespace ns {

        typedef int MyInt;

        enum Letters {A, B, C};

        /** Documentation here */
        struct FooStruct {};

        class FooClass {

            class InnerFoo {};

        }
    }

}



namespace foo {

    /** This appears in the documentation */
    class Bar {

        class InnerBar {};
    
    };
    
    /** This does not */
    int baz();

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


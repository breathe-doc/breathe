
namespace foo {

    /** This appears in the documentation */
    class Bar {

    public:
        //! \brief namespaced class function
        virtual void publicFunction() const = 0;

        virtual void undocumentedPublicFunction() const = 0;

        //! A protected class
        class PublicClass {};

        class UndocumentedPublicClass {};

    protected:

        //! A protected function
        void protectedFunction() {};

        void undocumentedProtectedFunction() {};

        //! A protected class
        class ProtectedClass {};

        class UndocumentedProtectedClass {};

    private:

        //! This is a private function
        void privateFunction() const = 0;

        void undocumentedPrivateFunction() const = 0;

        //! A private class
        class PrivateClass {};

        class UndocumentedPrivateClass {};
    };

    /** This also appears */
    int baz();

    /** More examples in a nested namespace */
    namespace ns {

        typedef int MyInt;

        enum Letters {
            A, /**< A documented enumeration constant */
            B,
            C
        };

        /** Documentation here */
        struct FooStruct {};

        class FooClass {

            class InnerFoo {};

        };
    }

}

/** This is outside the namespace */
class OuterBar {

    /** This appears as a sub class */
    class InnerBar {};

};

/** Function outside of the namespace */
void outerFunction() {};


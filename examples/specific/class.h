
namespace testnamespace {

//! \brief first class inside of namespace
class NamespacedClassTest {

public:

    //! \brief namespaced class function
    virtual void function() const = 0;

    static void functionS();

    explicit NamespacedClassTest() {}

    //! \brief namespaced class other function
    void anotherFunction() {}
};


//! \brief second class inside of namespace
class ClassTest {

public:

    //! \brief second namespaced class function
    void function() {}

    //! \brief second namespaced class other function
    void anotherFunction() {}

};


}

//! \brief class outside of namespace
class OuterClass {

public:

    //! \brief inner class
    class InnerClass {};

};


//! \brief class outside of namespace
class ClassTest {

public:

    /*! \brief non-namespaced class function

        More details in the header file.
      */
    void function(int myParameter);
 
    //! \brief non-namespaced class other function
    void anotherFunction();

    //! \brief namespaced class function
    virtual void publicFunction() const = 0;

    virtual void undocumentedPublicFunction() const = 0;

    //! A public class
    class PublicClass {};

    class UndocumentedPublicClass {};

    //! A public struct
    struct PublicStruct {};

    struct UndocumentedPublicStruct {};

protected:

    //! A protected function
    void protectedFunction() {}

    void undocumentedProtectedFunction() {}

    //! A protected class
    class ProtectedClass {};

    class UndocumentedProtectedClass {};

    //! A protected struct
    struct ProtectedStruct {};

    struct UndocumentedProtectedStruct {};

private:

    //! This is a private function
    void privateFunction() const = 0;

    void undocumentedPrivateFunction() const = 0;

    //! A private class
    class PrivateClass {};

    class UndocumentedPrivateClass {};

    //! A private struct
    struct PrivateStruct {};

    struct UndocumentedPrivateStruct {};
};



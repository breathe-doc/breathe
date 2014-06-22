
namespace testnamespace {

//! \brief first struct inside of namespace
struct NamespacedStructTest {


    //! \brief namespaced struct function
    virtual void function() const = 0;

    static void functionS();

    explicit NamespacedStructTest() {};

    //! \brief namespaced struct other function
    void anotherFunction() {};
};


//! \brief second struct inside of namespace
struct StructTest {

    //! \brief second namespaced struct function
    void function() {};

    //! \brief second namespaced struct other function
    void anotherFunction() {};

    //! A public class
    class PublicClass {};

    class UndocumentedPublicClass {};
};


};


//! \brief struct outside of namespace
struct StructTest {

    //! \brief namespaced class function
    virtual void publicFunction() const = 0;

    virtual void undocumentedPublicFunction() const = 0;

    //! A public class
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



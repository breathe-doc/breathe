
namespace testnamespace {

//! \brief first class inside of namespace
class NamespacedClassTest {

    //! \brief namespaced class function
    virtual void function() const = 0;

    static void functionS();

    explicit NamespacedClassTest() {};

    //! \brief namespaced class other function
    void anotherFunction() {};
};


//! \brief second class inside of namespace
class ClassTest {

    //! \brief second namespaced class function
    void function() {};

    //! \brief second namespaced class other function
    void anotherFunction() {};
};


};;


//! \brief class outside of namespace
class ClassTest {

    //! \brief non-namespaced class function
    void function() {};

    //! \brief non-namespaced class other function
    void anotherFunction() {};
};



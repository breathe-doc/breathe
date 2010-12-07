

namespace testnamespace {

//! \brief first class inside of namespace
class NamespacedClassTest {

public:

    //! \brief namespaced class function
    virtual void function() const = 0;

    explicit NamespacedClassTest() {};

protected:

    //! Some kind of function
    static void functionS();

private:


    //! \brief namespaced class other function
    void anotherFunction() {};
};

}


/** @defgroup mygroup My Group
 *  This is the first group
 *  @{
 */

//! \brief first class inside of namespace
class GroupedClassTest {

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

//! This function is in MyGroup
void groupedFunction();

/** @} */ // end of mygroup


//! \brief second class inside of namespace
class UngroupedClassTest {

public:
    //! \brief second namespaced class function
    void function() {};

private:

    //! A private function
    void ungroupedPrivateFunction() {};

    class PrivateClass {};
};

//! Ungrouped function
void ungroupedFunction();

//! \brief outer namespace
//! \ingroup mygroup
namespace ns1 {

//! \brief A class in ns1
//! \ingroup mygroup
class MyClass1 {
public:
    /// \brief default constructor
    MyClass1();
};

//! \brief inner namespace
//! \ingroup mygroup
namespace ns2 {

//! \brief A class in ns1::ns2
//! \details Detailed description of function2.
//! \ingroup mygroup
class MyClass2
{
public:
    // \brief brief statement for member group

    /// \name member group name
    ///
    /// Description of member group goes here
    ///@{
    
    /// \brief method1 brief
    ///
    /// method1 details
    void method1();

protected:
    /// \brief method2 brief
    ///
    /// method2 details
    void method2();
    ///@}

    /// \brief method3 is not in the member group
    void method3();
};

/// \brief another class
class MyClass3
{
public:
    /// \brief default constructor
    MyClass3();
};

/// \brief another nested namespace
namespace ns3 {
/// \brief another class
/// \ingroup mygroup
class MyClass4
{
public:
    /// \brief default constructor
    MyClass4();
};
} // namespace ns3

} // namespace ns2
} // namespace ns1

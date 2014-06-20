
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


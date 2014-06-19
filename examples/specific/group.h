
/** @defgroup mygroup My Group
 *  This is the first group
 *  @{
 */

//! \brief first class inside of namespace
class GroupedClassTest {

public:
    //! \brief namespaced class function
    virtual void publicFunction() const = 0;

private:

    //! This is a private function
    void privateFunction() const = 0;

    //! This is another private function
    void secondPrivateFunction() const = 0;
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


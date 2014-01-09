
/** @defgroup mygroup My Group
 *  This is the first group
 *  @{
 */

//! \brief first class inside of namespace
class GroupedClassTest {

    //! \brief namespaced class function
    virtual void function() const = 0;
};

//! This function is in MyGroup
void groupedFunction();

/** @} */ // end of mygroup


//! \brief second class inside of namespace
class UngroupedClassTest {

    //! \brief second namespaced class function
    void function() {};
};

//! Ungrouped function
void ungroupedFunction();


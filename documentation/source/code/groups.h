// Example from Doxygen documentation

/** A class. More details about the Test class */
class UserDefinedGroupTest
{
  public:
    //@{
    /** Same documentation for both members. Details */
    void func1InGroup1();
    void func2InGroup1();
    //@}

    /** Function without group. Details. */
    void ungroupedFunction();
    void func1InCustomGroup();
  protected:
    void func2InCustomGroup();
};

void UserDefinedGroupTest::func1InGroup1() {}
void UserDefinedGroupTest::func2InGroup1() {}

/** @name Custom Group
 *  Description of custom group
 */
//@{
/** Function 2 in custom group. Details. */
void UserDefinedGroupTest::func2InCustomGroup() {}
/** Function 1 in custom group. Details. */
void UserDefinedGroupTest::func1InCustomGroup() {}
//@}

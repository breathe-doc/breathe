// Example from Doxygen documentation

/** A class. More details about the Test class */
class Test
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

void Test::func1InGroup1() {}
void Test::func2InGroup1() {}

/** @name Custom Group
 *  Description of custom group
 */
//@{
/** Function 2 in custom group. Details. */
void Test::func2InCustomGroup() {}
/** Function 1 in custom group. Details. */
void Test::func1InCustomGroup() {}
//@}



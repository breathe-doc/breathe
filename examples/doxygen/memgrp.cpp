/** A class. Details */
class Test9
{
  public:
    //@{
    /** Same documentation for both members. Details */
    void func1InGroup1();
    void func2InGroup1();
    //@}

    /** Function without group. Details. */
    void ungroupedFunction();
    void func1InGroup2();
  protected:
    void func2InGroup2();
};

void Test9::func1InGroup1() {}
void Test9::func2InGroup1() {}

/** @name Group2
 *  Description of group 2. 
 */
//@{
/** Function 2 in group 2. Details. */
void Test9::func2InGroup2() {}
/** Function 1 in group 2. Details. */
void Test9::func1InGroup2() {}
//@}

/*! \file 
 *  docs for this file
 */

//@{
//! one description for all members of this group 
//! (because DISTRIBUTE_GROUP_DOC is YES in the config file)
#define A 1
#define B 2
void glob_func();
//@}

/*! \file autolink.cpp
  Testing automatic link generation.
  
  A link to a member of the Test2 class: Test2::member,
  
  More specific links to the each of the overloaded members:
  Test2::member(int) and Test2#member(int,int)

  A link to a protected member variable of Test2: Test2#var,

  A link to the global enumeration type #GlobEnum.
 
  A link to the define #ABS(x).
  
  A link to the destructor of the Test2 class: Test2::~Test2,
  
  A link to the typedef ::Test2TypeDef.
 
  A link to the enumeration type Test2::EType
  
  A link to some enumeration values Test2::Val1 and ::GVal2
*/

/*!
  Since this documentation block belongs to the class Test2 no link to
  Test2 is generated.

  Two ways to link to a constructor are: #Test2 and Test2().

  Links to the destructor are: #~Test2 and ~Test2().
  
  A link to a member in this class: member().

  More specific links to the each of the overloaded members: 
  member(int) and member(int,int). 
  
  A link to the variable #var.

  A link to the global typedef ::Test2TypeDef.

  A link to the global enumeration type #GlobEnum.
  
  A link to the define ABS(x).
  
  A link to a variable \link #var using another text\endlink as a link.
  
  A link to the enumeration type #EType.

  A link to some enumeration values: \link Test2::Val1 Val1 \endlink and ::GVal1.

  And last but not least a link to a file: autolink.cpp.
  
  \sa Inside a see also section any word is checked, so EType, 
      Val1, GVal1, ~Test2 and member will be replaced by links in HTML.
*/

class Test2
{
  public:
    Test2();               //!< constructor
   ~Test2();               //!< destructor
    void member(int);     /**< A member function. Details. */
    void member(int,int); /**< An overloaded member function. Details */

    /** An enum type. More details */
    enum EType { 
      Val1,               /**< enum value 1 */ 
      Val2                /**< enum value 2 */ 
    };                

  protected:
    int var;              /**< A member variable */
};

/*! details. */
Test2::Test2() { }

/*! details. */
Test2::~Test2() { }

/*! A global variable. */
int globVar;

/*! A global enum. */
enum GlobEnum { 
                GVal1,    /*!< global enum value 1 */ 
                GVal2     /*!< global enum value 2 */ 
              };

/*!
 *  A macro definition.
 */ 
#define ABS(x) (((x)>0)?(x):-(x))

typedef Test2 Test2TypeDef;

/*! \fn typedef Test2 Test2TypeDef
 *  A type definition. 
 */

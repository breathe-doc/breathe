class Test4
{
  public:
    enum TEnum { Val1, Val2 };

    /*! Another enum, with inline docs */
    enum AnotherEnum 
    { 
      V1, /*!< value 1 */
      V2  /*!< value 2 */
    };
};

/*! \class Test4
 * The class description.
 */

/*! \enum Test4::TEnum
 * A description of the enum type.
 */

/*! \var Test4::TEnum Test4::Val1
 * The description of the first enum value.
 */



/// A union of two values
union SeparateUnion
{
    int size;     ///< The size of the thing
    float depth;  ///< How deep it is
};


namespace foo {

/// A union of two values
union MyUnion
{
    int someInt;      ///< The int of it all
    float someFloat;  ///< The float side of things
};

}

/// A class with a union
class ClassWithUnion
{
    /// A union with two values
    union UnionInClass
    {
        int intvalue;       ///< An int value
        float floatvalue;   ///< A float value
    };

    /// Documented class
    class ExtraClass
    {
        int a_member;
        float another_member;
    }
};


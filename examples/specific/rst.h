
//! \brief first class inside of namespace
class TestClass
{
public:

    /*!
    Inserting additional restructured text information.

    \rst

    This is some funky non-xml compliant text: <& !><

    .. note::
        
       This restructured text has been handled correctly.
    \endrst

    \verbatim
    This is just a standard verbatim block with code:

        child = 0;
        while( child = parent->IterateChildren( child ) )
    \endverbatim

    */
    virtual void function() const = 0;

    //! Brief desc
    virtual void testFunction() const {};
};

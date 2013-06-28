
//! \brief first class inside of namespace
class TestClass
{
public:

    /*!
    Inserting additional reStructuredText information.

    \rst

    This is some funky non-xml compliant text: <& !><

    .. note::
        
       This reStructuredText has been handled correctly.
    \endrst

    This is just a standard verbatim block with code:

    \verbatim
        child = 0;
        while( child = parent->IterateChildren( child ) )
    \endverbatim

    */
    virtual void function() const = 0;

    /*!
    Inserting additional reStructuredText information.
    \verbatim embed:rst
    .. note::

       This reStructuredText has been handled correctly.
    \endverbatim
    */
    virtual void rawVerbatim() const = 0;

   /*!
    * Inserting additional reStructuredText information.
    *
    * \verbatim embed:rst:leading-asterisk
    *     Some example code::
    *
    *        int example(int x) {
    *            return x * 2;
    *        }
    * \endverbatim
    */
    virtual void rawLeadingAsteriskVerbatim() const = 0;

    //! Brief desc
    virtual void testFunction() const {};
};

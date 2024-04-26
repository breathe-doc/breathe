
//! \brief first class inside of namespace
class TestClass
{
public:

    /*!
    Inserting additional reStructuredText information.

    \rst

    This is some funky non-XML compliant text: <& !><

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

    /// Some kind of method
    ///
    /// @param something a parameter
    ///
    /// @verbatim embed:rst:leading-slashes
    ///    .. code-block:: c
    ///       :linenos:
    ///
    ///       bool foo(bool something) {
    ///           return something;
    ///       };
    ///
    /// @endverbatim
    /// @note Documentation using `///` should begin and end in a blank line.

    virtual void rawLeadingSlashesVerbatim(int something) const = 0;

    /*!
    Inserting an inline reStructuredText snippet.
    Linking to another function: \inlinerst :cpp:func:`TestClass::rawVerbatim` \endrst
    */
    virtual void rawInlineVerbatim() const = 0;

    //! Brief description
    virtual void testFunction() const {};
};

/**
 *  @file xrefsect.h
 *  A few examples of xrefsect items support.
 */

/**
 * An example of using Doxygen's todo command.
 *
 * @todo Implement this function.
 */
int unimplemented(void);

/**
 * An example of using Doxygen's bug and test commands.
 *
 * @bug Does not work yet.
 *
 * @test Add proper unit testing first.
 */
void buggy_function(int param);

/**
 * An example of using Doxygen's deprecated command.
 *
 * @deprecated Should not be used on new code.
 */
void old_function(void);

/**
 * An example of a custom Doxygen xrefitem declared as an ALIAS.
 *
 * @xrefsample This text shows up in the xref output.
 */
void sample_xrefitem_function(void);

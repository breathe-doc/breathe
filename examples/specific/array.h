
/** My function */
int foo(int a[5]);

/** My other function 
 * 
 * @test This declaration is supposed to be
 * @code{.c}
 * int bar(int n, int a[static n]);
 * @endcode
 * But, Sphinx fails to recognize `int a[static n])` as a C specific array syntax
 */
int bar(int n, int a[]);

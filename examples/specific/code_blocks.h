
/** A function with an unannotated code block with C/C++ code.
 *
 * @code
 * char* buffer = new char[42];
 * int charsAdded = sprintf(buffer, "Tabs are normally %d spaces\n", 8);
 * @endcode
 */
void with_standard_code_block();

/** A function with an unannotated code block with non-C/C++ code.
 *
 * @code
 * set(user_list A B C)
 * foreach(element ${user_list})
 *     message(STATUS "Element is ${element}")
 * endforeach()
 * @endcode
 * 
 * Another code-block that explicitly remains not highlighted.
 * @code{.unparsed}
 * Show this as is.
 * @endcode
 */
void with_unannotated_cmake_code_block();

/** A function with an annotated cmake code block.
 *
 * @code{.cmake}
 * set(user_list A B C)
 * foreach(element ${user_list})
 *     message(STATUS "Element is ${element}")
 * endforeach()
 * @endcode
 */
void with_annotated_cmake_code_block();

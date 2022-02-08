
/** A function with an unannotated code block with C/C++ code.
 *
 * @code
 * int result = with_standard_code_block()
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

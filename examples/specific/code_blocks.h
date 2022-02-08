
/** with_standard_code_block
 *
 * @code
 * int result = with_standard_code_block()
 * @endcode
 *
 */
void with_standard_code_block();

/** with_unannotated_cmake_code_block
 *
 * @code
 * set(user_list A B C)
 * for(element in ${user_list})
 *     message(STATUS "Element is ${element}")
 * endfor()
 * @endcode
 */
void with_unannotated_cmake_code_block();

/** with_annotated_cmake_code_block
 *
 * @code{.cmake}
 * set(user_list A B C)
 * for(element in ${user_list})
 *     message(STATUS "Element is ${element}")
 * endfor()
 * @endcode
 */
void with_annotated_cmake_code_block();

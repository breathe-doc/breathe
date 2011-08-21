/**
 * @brief a function with one template arguments
 * 
 * @tparam T this is the template parameter
 * 
 * @param arg1 argument of type T
 * 
 * @return return value of type T
 */
template <typename T>
T function1(T arg1)
{}


/**
 * @brief a function with three template arguments
 * 
 * @tparam T this is the first template parameter
 * @tparam U this is the second template parameter
 * @tparam N this is the third template parameter, it is a non-type parameter
 * 
 * @param arg1 first argument of type T
 * @param arg2 second argument of type U
 * 
 * @return return value of type T
 */
template <typename T, typename U, int N>
T function2(T arg1, U arg2)
{}

/**
 * @brief a type alias with one template argument
 * 
 * @tparam T this is the template parameter
 * 
 */
template <typename T>
using IsFuzzy = std::is_fuzzy<T>;


/**
 * @brief a type alias with three template arguments
 * 
 * @tparam T this is the first template parameter
 * @tparam U this is the second template parameter
 * @tparam N this is the third template parameter, it is a non-type parameter
 * 
 */
template <typename T, typename U, int N>
using IsFurry = std::is_furry<T,U,N>;

template<typename T>
concept Hashable = requires(T a)
{
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

/*! \concept Hashable concept.h "inc/concept.h"
 *  \brief This is a test concept.
 *
 * It was stolen from the first example from
 * https://en.cppreference.com/w/cpp/language/constraints
 */

/**
 * @brief a class with a template parameter
 * 
 * @tparam T this is the template parameter
 */
template <typename T>
class templateclass
{
public:

  /// default constructor
  templateclass() {}
  
  /**
   * @brief constructor with template argument
   *
   * @param m the argument
   */
  templateclass(T const & m) : member(m) {}
  
  /**
   * @brief member accepting template argument and returning template argument
   * 
   * @param t argument of type T
   * @return returns value of type T
   */
  T method(T const & t);

private:
    /// a member with templated type
    T member;
};

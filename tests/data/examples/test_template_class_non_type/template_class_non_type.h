/**
 * @brief a class with three template parameters
 * 
 * @tparam T this is the first template parameter
 * @tparam U this is the second template parameter
 * @tparam N this is the third template parameter, it is a non-type parameter
 */
template <typename T, typename U, int N>
class anothertemplateclass
{
public:
  /// default constructor
  anothertemplateclass() {}
  
  /**
   * @brief constructor with two template argument
   *
   * @param m1 first argument
   * @param m2 second argument
   */
  anothertemplateclass(T const & m1, U const & m2) : 
    member1(m1), member2(m2) {}
    
  /**
   * @brief member accepting template argument and returning template argument
   * 
   * @param t argument
   * @return returns value of type U
   */
  U method(T const & t);

  private:
    /// a member with templated type
    T member1;
    
    /// another member with templated type
    U member2;
};

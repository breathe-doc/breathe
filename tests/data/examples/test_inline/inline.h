#include <stdexcept>
/** A class to demonstrate inline documentation syntax. */
class InlineTest
{
 public:
 /** A member function.
  *
  * Details about member function
  *
  *  \exception std::out_of_range parameter is out of range.
  *  @return a character pointer.
  */
 const char *member(char c, ///< c a character.
                    int n)  ///< n an integer.

 throw(std::out_of_range);
};

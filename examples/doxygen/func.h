class Test6
{
  public:
    const char *member(char,int) throw(std::out_of_range);
};

const char *Test6::member(char c,int n) throw(std::out_of_range) {}

/*! \class Test6
 * \brief Test6 class.
 *
 * Details about Test6.
 */

/*! \fn const char *Test6::member(char c,int n)
 *  \brief A member function.
 *  \param c a character.
 *  \param n an integer.
 *  \exception std::out_of_range parameter is out of range.
 *  \return a character pointer.
 */

/*! \brief Doing important things with parameter directions
 *
 *  \param[out]     a output
 *  \param[in]      b input
 *  \param[in, out] c input but gets rewritten
 */
void myFunc(int * a, int * b, int * c);

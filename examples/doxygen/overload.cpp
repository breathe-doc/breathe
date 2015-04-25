class Test10
{
  public:
    void drawRect(int,int,int,int);
    void drawRect(const Rect &r);
};

void Test10::drawRect(int x,int y,int w,int h) {}
void Test10::drawRect(const Rect &r) {}

/*! \class Test10
 *  \brief A short description.
 *   
 *  More text.
 */

/*! \fn void Test10::drawRect(int x,int y,int w,int h)
 * This command draws a rectangle with a left upper corner at ( \a x , \a y ),
 * width \a w and height \a h. 
 */

/*!
 * \overload void Test10::drawRect(const Rect &r)
 */


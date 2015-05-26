
/*! A template class */
template<class T,int i=100> class Test14
{
  public:
    Test14();
    Test14(const Test14 &);
};

/*! complete specialization */
template<> class Test14<void *,200>
{
  public:
    Test14();
};

/*! A partial template specialization */
template<class T> class Test14<T *> : public Test14<void *,200>
{
  public:
    Test14();
};

/*! The constructor of the template class*/
template<class T,int i> Test14<T,i>::Test14() {}

/*! The copy constructor */
template<class T,int i> Test14<T,i>::Test14(const Test14 &t) {}

/*! The constructor of the partial specialization */
template<class T> Test14<T *>::Test14() {}

/*! The constructor of the specialization */
template<> Test14<void *,200>::Test14() {}


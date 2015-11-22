
class BaseA {};
class BaseB {};

/*! \brief This is the main class we're interested in */
class Main : public BaseA, BaseB {};

class ChildA : public Main {};
class ChildB : public Main {};

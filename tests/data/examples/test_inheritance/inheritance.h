
class BaseA {};
class BaseB {};

/*! \brief This is the main class we're interested in */
class Main : public BaseA, BaseB {};

class ChildA : public Main {};
class ChildB : public Main {};

class ChildV1 : virtual public BaseA {};
class ChildV2 : virtual public BaseA {};
class ChildV3 : public ChildV1, ChildV2 {};

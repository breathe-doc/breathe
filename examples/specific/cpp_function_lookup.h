void fInit(int arg = 42);
void fPlain(int arg);
void fPtr(int *arg);
void fLRef(int &arg);
void fRRef(int &&arg);
//template<typename ...T> // TODO: add this again when the parsing has been fixed
void fParamPack(T ...arg);
class A {};
void fMemPtr(int A::*arg);
void fParen(void (*arg)());

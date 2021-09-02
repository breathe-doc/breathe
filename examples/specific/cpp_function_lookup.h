// stuff on the paramQual
void fNoexcept() noexcept;
void fFinal() final;
void fOverride() override;
void fAttr() [[myattr]]; // TODO: Doxygen seems to strip attributes
void fFInit() = default;
auto fTrailing() -> int;

// different parameters
void fInit(int arg = 42);
void fPlain(int arg);
void fPtr(int *arg);
void fLRef(int &arg);
void fRRef(int &&arg);
template<typename ...T>
void fParamPack(T ...arg);
class A {};
void fMemPtr(int A::*arg);
void fParen(void (*arg)());

// different parameters in a function pointer
void fParenPlain(void (*arg)(int argInner));

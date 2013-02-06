
//! Function which takes two int arguments
void f(int, int);

//! Function which takes two double arguments
void f(double, double);

namespace test {

//! Another function which takes two int arguments
void g(int, int);

//! Another function which takes two double arguments
void g(double, double);

}

class MyType {};

class MyOtherType {};

//! Another function which takes a custom type
void h(std::string, MyType);

//! Another function which takes another custom type
void h(std::string, MyOtherType);

//! Another function which takes a basic type
void h(std::string, int);


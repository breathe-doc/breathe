struct A {};
struct B {};

struct C {
	friend class A;
	friend struct B;
};

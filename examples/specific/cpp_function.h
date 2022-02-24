struct Foo{};
struct Class {
	virtual void f1() const volatile & = 0;
	virtual void f2() const volatile && = 0;
	static void f3();


	void (*f_issue_489)(struct Foo *foo, int value);

	int f_issue_338() noexcept;
};

/** A namespace to demonstrate a namespaced function */
namespace TestNamespaceFunction {
/** A function within a namspace. */
void namespaceFunc();
}

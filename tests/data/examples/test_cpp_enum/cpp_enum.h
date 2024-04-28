enum Unscoped : int {
	UnscopedEnumerator = 42
};

enum struct ScopedStruct : int {
	Enumerator = 42
};

enum class ScopedClass : int {
	Enumerator = 42
};

enum class ScopedClassNoUnderlying {
	Enumerator = 42
};

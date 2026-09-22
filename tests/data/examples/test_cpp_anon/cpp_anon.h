struct ClassWithAnonEntities {
	struct {
		int structMember;
	};

	union {
		int unionMember;
	};

	enum {
		Enumerator
	};
};

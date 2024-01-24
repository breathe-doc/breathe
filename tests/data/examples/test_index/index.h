
int A;

using B = long;

auto C(auto x) -> A;

template<typename T> void D();

struct E {
    char F;
};

namespace G {

constexpr unsigned int H = 12;

extern int I;

template<typename T> class J {
public:
    T K[H];
    static friend bool operator==(J ja,J jb) {
        for(unsigned int i=0; i < H; ++i) {
            if(ja[i] != jb[i]) return false;
        }
        return true;
    }
};

template<typename T> struct L { static constexpr bool M = false; };
template<typename T> struct L<J<T>> { static constexpr bool M = true; };

template<typename T> concept N = L<T>::Q;

typedef void (*O)(B);

}

#define P U

enum Q {R=0, S};


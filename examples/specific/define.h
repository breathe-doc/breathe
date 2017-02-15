/**
 * A simple define without a value
 */
#define USE_STUFF


/**
 * A define with a simple value
 */
#define MAX_LENGTH 100


/**
 * A define with some parameters
 *
 * \param A The parameter A
 * \param B The parameter B
 *
 * \returns The maximum of A and B
 */
#define MAX(A,B) ((A > B)?(A):(B))


/**
 * A define which spans multiple lines
 */
#define SWAP(A,B) {             \
                    (a) ^= (b); \
                    (b) ^= (a); \
                    (a) ^= (b); \
                  }

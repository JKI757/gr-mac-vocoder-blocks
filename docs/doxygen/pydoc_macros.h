#ifndef _PYDOC_MACROS_H
#define _PYDOC_MACROS_H

#define __EXPAND(x) x
#define __COUNT(_1, _2, _3, _4, _5, COUNT, ...) COUNT
#define __VA_SIZE(...) __EXPAND(__COUNT(__VA_ARGS__, 5, 4, 3, 2, 1))
#define __CAT1(a, b) a ## b
#define __CAT2(a, b) __CAT1(a, b)
#define __DOC1(n1) #n1
#define __DOC2(n1, n2) #n1 "\n\n" #n2
#define __DOC3(n1, n2, n3) #n1 "\n\n" #n2 "\n\n" #n3
#define __DOC4(n1, n2, n3, n4) #n1 "\n\n" #n2 "\n\n" #n3 "\n\n" #n4
#define __DOC5(n1, n2, n3, n4, n5) #n1 "\n\n" #n2 "\n\n" #n3 "\n\n" #n4 "\n\n" #n5
#define DOC(...) __EXPAND(__EXPAND(__CAT2(__DOC, __VA_SIZE(__VA_ARGS__)))(__VA_ARGS__))

#endif /* _PYDOC_MACROS_H */

#ifndef SYSTEM_PTHREAD_MACHDEP_H
#define SYSTEM_PTHREAD_MACHDEP_H

#include <pthread.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * iOS 16.4 device DSC (JavaScriptCore) uses contiguous reserved PTK slots:
 * KEY0..KEY4 => 90..94.
 */
#ifndef __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY0
#define __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY0 90
#endif
#ifndef __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY1
#define __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY1 91
#endif
#ifndef __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY2
#define __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY2 92
#endif
#ifndef __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY3
#define __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY3 93
#endif
#ifndef __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY4
#define __PTK_FRAMEWORK_JAVASCRIPTCORE_KEY4 94
#endif

int pthread_key_init_np(int key, void (*destructor)(void*));

static inline void* _pthread_getspecific_direct(unsigned long slot)
{
    return pthread_getspecific((pthread_key_t)slot);
}

static inline int _pthread_setspecific_direct(unsigned long slot, const void* value)
{
    return pthread_setspecific((pthread_key_t)slot, value);
}

#ifdef __cplusplus
}
#endif

#endif /* SYSTEM_PTHREAD_MACHDEP_H */

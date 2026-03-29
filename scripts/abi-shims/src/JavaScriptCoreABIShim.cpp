#include <stddef.h>
#include <stdint.h>

extern "C" void jscABIShimWTFSignpostLogHandle()
    __attribute__((used, visibility("default")))
    asm("_WTFSignpostLogHandle");

void jscABIShimWTFSignpostLogHandle()
{
}

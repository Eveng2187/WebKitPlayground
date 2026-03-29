/*
 * Copyright (C) 2026 Apple Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

#import "config.h"

#if PLATFORM(IOS_FAMILY) && (!ENABLE(IOS_TOUCH_EVENTS) || !USE(APPLE_INTERNAL_SDK))

#import "WebEventRegion.h"

namespace WebCore {
class EventHandler;
}

@class WebEvent;

@implementation WebEventRegion

- (id)initWithPoints:(CGPoint)inP1 :(CGPoint)inP2 :(CGPoint)inP3 :(CGPoint)inP4
{
    if (!(self = [super init]))
        return nil;

    p1 = inP1;
    p2 = inP2;
    p3 = inP3;
    p4 = inP4;
    return self;
}

- (id)copyWithZone:(NSZone *)zone
{
    UNUSED_PARAM(zone);
    return [self retain];
}

- (BOOL)hitTest:(CGPoint)point
{
    // ABI-only fallback when internal touch additions are unavailable.
    UNUSED_PARAM(point);
    return NO;
}

- (CGPoint)p1
{
    return p1;
}

- (CGPoint)p2
{
    return p2;
}

- (CGPoint)p3
{
    return p3;
}

- (CGPoint)p4
{
    return p4;
}

@end

extern "C" void webCoreABIShimEventHandlerTouchEvent(WebCore::EventHandler*, WebEvent*)
    __attribute__((used, visibility("default")))
    asm("__ZN7WebCore12EventHandler10touchEventEP8WebEvent");

void webCoreABIShimEventHandlerTouchEvent(WebCore::EventHandler*, WebEvent*)
{
}

extern "C" void webCoreABIShimDocumentGetTouchRects(void*, void*)
    __attribute__((used, visibility("default")))
    asm("__ZN7WebCore8Document13getTouchRectsERN3WTF6VectorINS_7IntRectELm0ENS1_15CrashOnOverflowELm16ENS1_10FastMallocEEE");

void webCoreABIShimDocumentGetTouchRects(void*, void*)
{
}

extern "C" bool webCoreABIShimHandleTouchEvent(void*, const void*)
    __attribute__((used, visibility("default")))
    asm("__ZN7WebCore12EventHandler16handleTouchEventERKNS_18PlatformTouchEventE");

bool webCoreABIShimHandleTouchEvent(void*, const void*)
{
    return false;
}

extern "C" void* webCoreABIShimCreateAV1VTBDecoder()
    __attribute__((used, visibility("default")))
    asm("__ZN7WebCore19createAV1VTBDecoderEU13block_pointerFvP10__CVBufferxxE");

void* webCoreABIShimCreateAV1VTBDecoder()
{
    return nullptr;
}

extern "C" __attribute__((used, visibility("default")))
void* palABIShimSoftLinkVTRestrictVideoDecoders asm("__ZN3PAL43softLinkVideoToolboxVTRestrictVideoDecodersE") = nullptr;

extern "C" bool palABIShimCanLoadVTRestrictVideoDecoders()
    __attribute__((used, visibility("default")))
    asm("__ZN3PAL44canLoad_VideoToolbox_VTRestrictVideoDecodersEv");

bool palABIShimCanLoadVTRestrictVideoDecoders()
{
    return false;
}

#endif // PLATFORM(IOS_FAMILY) && (!ENABLE(IOS_TOUCH_EVENTS) || !USE(APPLE_INTERNAL_SDK))

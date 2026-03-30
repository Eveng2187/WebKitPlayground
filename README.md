# WebKit Playground

Build an open-source version of WebKit and replace it system-wide on iOS jailbroken devices.

## Requirements

- WebKit source code: [releases/Apple/Safari-16.4-iOS-16.4.1](https://github.com/WebKit/WebKit/releases/tag/releases/Apple/Safari-16.4-iOS-16.4.1)
- Xcode 14.3.1
- Test device: iOS 16.4.1 (Dopamine)

## How to use

1. We need to patch dyld to allow `DYLD_FRAMEWORK_PATH` to work on top of DSC: https://github.com/Lessica/Dopamine/commit/34f45eedfa920479f5ccde78c7c572f61214e354
2. Compile WebKit with the following command:

```
Tools/Scripts/build-webkit --ios-device --release --use-ccache WK_USE_CCACHE=YES ARCHS='arm64 arm64e' GCC_TREAT_WARNINGS_AS_ERRORS=NO OTHER_CFLAGS='$(inherited) -Wno-error -Wno-error=strict-prototypes -Wno-strict-prototypes -Wno-error=deprecated-declarations' OTHER_CPLUSPLUSFLAGS='$(inherited) -Wno-error -Wno-error=deprecated-declarations'
```

3. Push compiled frameworks to `/Library/Frameworks` or `$JBROOT/Library/Frameworks` (RootHide).

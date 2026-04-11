# WebKit Playground

Build an open-source version of WebKit and replace it system-wide on iOS jailbroken devices.

## Requirements

- WebKit source code: [releases/Apple/Safari-16.4-iOS-16.4.1](https://github.com/WebKit/WebKit/releases/tag/releases/Apple/Safari-16.4-iOS-16.4.1)
- Xcode 14.3.1 + iOS 16.5 SDK
- Test device: iOS 16.4.1 (Dopamine)

## How to use

1. We need to patch dyld to allow `DYLD_FRAMEWORK_PATH` to work on top of DSC: https://github.com/Lessica/Dopamine/commit/34f45eedfa920479f5ccde78c7c572f61214e354
2. Check out source code of WebKit and **apply patches**
3. Compile WebKit with the following command:

```
Tools/Scripts/build-webkit --ios-device --release --use-ccache WK_USE_CCACHE=YES ARCHS='arm64 arm64e' GCC_TREAT_WARNINGS_AS_ERRORS=NO OTHER_CFLAGS='$(inherited) -Wno-error -Wno-error=strict-prototypes -Wno-strict-prototypes -Wno-error=deprecated-declarations' OTHER_CPLUSPLUSFLAGS='$(inherited) -Wno-error -Wno-error=deprecated-declarations'
```

4. Push compiled frameworks to `/Library/Frameworks` or `$JBROOT/Library/Frameworks` (RootHide).

## Build parallelism (Xcode defaults)

If you want to increase compile/build parallelism globally in Xcode, run:

```bash
defaults write com.apple.dt.Xcode IDEBuildOperationMaxNumberOfConcurrentCompileTasks 48
defaults write com.apple.Xcode PBXNumberOfParallelBuildSubtasks 48
```

What they do:

- `IDEBuildOperationMaxNumberOfConcurrentCompileTasks`: controls the max number of concurrent compile tasks.
- `PBXNumberOfParallelBuildSubtasks`: controls the number of parallel PBX build subtasks in the build graph.

Notes:

- These are global user defaults and affect Xcode-driven builds on this machine.
- Restart Xcode after changing these values.
- To restore defaults:

```bash
defaults delete com.apple.dt.Xcode IDEBuildOperationMaxNumberOfConcurrentCompileTasks
defaults delete com.apple.Xcode PBXNumberOfParallelBuildSubtasks
```

## Caveats

- JSC is not replaced. The open-source JIT implementation appears to be incompatible with physical iOS devices (not sure).
- DOMJIT is turned off for the same reason.
- I managed to fill in some of the missing symbols, but they don't work as expected, so some features may not function properly.

## Fast dyldhook iteration loop (for dual-JSC debugging)

To avoid full Dopamine rebuild + TrollStore reinstall on every dyldhook tweak, use:

```bash
scripts/iterate-dyldhook.sh --dopamine-root /Users/rachel/Codelab/Dopamine
```

This script does a minimal loop:

1. Build only `BaseBin/dyldhook`
2. Build a safe `basebin` update tar by pulling current device `/basebin` then overlaying new `dyldhook_merge*.dylib`
3. Upload it to device over SSH (default target: `iproxy`)
4. Run `/basebin/jbctl update basebin ...` (userspace reboot)
5. Wait for SSH reconnect and save one log snapshot under `packages/`

Useful options:

```bash
# Build/package only, don't push to device
scripts/iterate-dyldhook.sh --skip-deploy

# Override SSH endpoint
scripts/iterate-dyldhook.sh --ssh-host 127.0.0.1 --ssh-port 2222 --ssh-user root

# Skip log pull
scripts/iterate-dyldhook.sh --skip-logs
```

Notes:

- In this RootHide branch, `jbupdate` rebuilds basebin trustcache from files inside the update tar.
- So a tiny tar containing only `dyldhook` files can cause missing trust entries (e.g. `libxpf.dylib`) and trigger `panic-full`.
- The script therefore defaults to packaging full device `/basebin` content to keep trustcache complete.

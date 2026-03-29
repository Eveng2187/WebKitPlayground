#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, errors="ignore")


def parse_dsc_clients(dsc: Path, provider_path: str) -> list[str]:
    text = run(["ipsw", "dyld", "imports", str(dsc), provider_path])
    clients: list[str] = []
    in_dylibs = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("In DSC (Dylibs)"):
            in_dylibs = True
            continue
        if line.startswith("In FileSystem DMG"):
            in_dylibs = False
        if in_dylibs and line.startswith("/"):
            clients.append(line)
    return clients


def read_defined_exports(binary: Path, arch: str) -> set[str]:
    text = run(["nm", "-arch", arch, "-gjU", str(binary)])
    symbols = set()
    for raw in text.splitlines():
        sym = raw.strip()
        if not sym or sym.startswith("$"):
            continue
        symbols.add(sym)
    return symbols


def read_imports_from_provider(client_bin: Path, arch: str, provider_short_name: str) -> set[str]:
    text = run(["nm", "-arch", arch, "-m", "-u", str(client_bin)])
    pat = re.compile(rf"\(undefined\)\s+external\s+(\S+)\s+\(from {re.escape(provider_short_name)}\)$")
    imports = set()
    for raw in text.splitlines():
        m = pat.search(raw.strip())
        if m:
            imports.add(m.group(1))
    return imports


def main() -> int:
    ap = argparse.ArgumentParser(description="Check ABI compatibility between DSC clients and built WebKit family binaries.")
    ap.add_argument("--dsc", required=True, type=Path, help="dyld_shared_cache_arm64e path")
    ap.add_argument("--split-root", required=True, type=Path, help="output dir of `ipsw dyld split`")
    ap.add_argument("--build-root", required=True, type=Path, help="WebKitBuild/Release-iphoneos root")
    ap.add_argument("--arch", default="arm64e")
    ap.add_argument("--out", required=True, type=Path, help="output json report path")
    args = ap.parse_args()

    providers = [
        {
            "name": "WebKit",
            "provider_path": "/System/Library/Frameworks/WebKit.framework/WebKit",
            "provider_short": "WebKit",
            "built_bins": [
                args.build_root / "WebKit.framework/WebKit",
                args.build_root / "WebKitLegacy.framework/WebKitLegacy",
            ],
        },
        {
            "name": "WebCore",
            "provider_path": "/System/Library/PrivateFrameworks/WebCore.framework/WebCore",
            "provider_short": "WebCore",
            "built_bins": [args.build_root / "WebCore.framework/WebCore"],
        },
        {
            "name": "JavaScriptCore",
            "provider_path": "/System/Library/Frameworks/JavaScriptCore.framework/JavaScriptCore",
            "provider_short": "JavaScriptCore",
            "built_bins": [args.build_root / "JavaScriptCore.framework/JavaScriptCore"],
        },
        {
            "name": "WebKitLegacy",
            "provider_path": "/System/Library/PrivateFrameworks/WebKitLegacy.framework/WebKitLegacy",
            "provider_short": "WebKitLegacy",
            "built_bins": [args.build_root / "WebKitLegacy.framework/WebKitLegacy"],
        },
    ]

    report: dict[str, object] = {
        "dsc": str(args.dsc),
        "split_root": str(args.split_root),
        "build_root": str(args.build_root),
        "arch": args.arch,
        "providers": {},
    }

    for p in providers:
        clients = parse_dsc_clients(args.dsc, p["provider_path"])
        required: set[str] = set()
        missing_client_files: list[str] = []
        for client in clients:
            client_bin = args.split_root / client.lstrip("/")
            if not client_bin.is_file():
                missing_client_files.append(client)
                continue
            required |= read_imports_from_provider(client_bin, args.arch, p["provider_short"])

        built_exports: set[str] = set()
        for b in p["built_bins"]:
            built_exports |= read_defined_exports(b, args.arch)

        missing_required = sorted(required - built_exports)

        report["providers"][p["name"]] = {
            "provider_path": p["provider_path"],
            "built_bins": [str(x) for x in p["built_bins"]],
            "counts": {
                "clients": len(clients),
                "missing_client_files": len(missing_client_files),
                "required_symbols": len(required),
                "built_export_chain": len(built_exports),
                "missing_required": len(missing_required),
            },
            "missing_required_symbols": missing_required,
            "missing_client_files": missing_client_files,
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

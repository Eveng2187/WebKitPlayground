#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path("/Volumes/OPTANE/WebKitPlayground")
ANALYSIS = ROOT / "samples/abi-report-20260328/config_gap_analysis.json"
OUT = ROOT / "samples/abi-report-20260328/build_flag_anomaly_report.json"

COMMAND_LINE_SNIPPET = """
ENABLE_DFG_JIT=ENABLE_DFG_JIT
ENABLE_FTL_JIT=ENABLE_FTL_JIT
ENABLE_IOS_TOUCH_EVENTS=ENABLE_IOS_TOUCH_EVENTS
ENABLE_JIT=ENABLE_JIT
ENABLE_TOUCH_EVENTS=ENABLE_TOUCH_EVENTS
""".strip()


def main() -> None:
    cfg = json.loads(ANALYSIS.read_text())
    macro = cfg.get("macro_snapshot", {})
    anomalies = []
    for line in COMMAND_LINE_SNIPPET.splitlines():
        k, v = line.split("=", 1)
        if k == v:
            anomalies.append(
                {
                    "setting": k,
                    "passed_value": v,
                    "issue": "self-referential value instead of concrete 0/1/YES/NO",
                }
            )

    result = {
        "inputs": {
            "config_gap_analysis": str(ANALYSIS),
        },
        "observed_macro_snapshot_in_built_headers": macro,
        "xcodebuild_commandline_feature_settings": COMMAND_LINE_SNIPPET.splitlines(),
        "anomalies": anomalies,
        "inference": [
            "Feature flags passed via current build-webkit invocation are not concretely resolved.",
            "This can explain why symbol gaps remain in feature-gated code paths.",
        ],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(str(OUT))


if __name__ == "__main__":
    main()

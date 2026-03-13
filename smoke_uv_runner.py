#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "azure-llm-toolkit>=0.2.3",
#   "litellm[proxy]>=1.40.0",
#   "python-dotenv>=1.0.1",
# ]
# ///

"""Run a smoke test inside an uv-provisioned runtime so dependencies are available.
This will load the antropic_proxy script (without running its __main__ block),
invoke its success_callback with a synthetic usage object (including
completion_tokens_details.reasoning_tokens), and force-save persistent stats.
"""

import runpy
import time
import os
from dotenv import load_dotenv

load_dotenv()

print("Running smoke_uv_runner.py — loading antropic_proxy into a module namespace")
ns = runpy.run_path("./antropic_proxy", run_name="antropic_proxy_module")

pfile = ns.get("PERSISTENT_STATS_FILE")
print("Persistent stats file:", pfile)

if pfile and os.path.exists(pfile):
    try:
        print("Before:\n", open(pfile, "r", encoding="utf-8").read())
    except Exception as e:
        print("Failed reading before file:", e)
else:
    print("No persistent file exists yet")

# Synthetic response to emulate an Azure response with reasoning tokens
response = {
    "usage": {
        "prompt_tokens": 12,
        "completion_tokens": 40,
        "completion_tokens_details": {"reasoning_tokens": 10},
        "total_tokens": 52,
    }
}

start_time = time.time() - 0.5
end_time = time.time()

if "success_callback" in ns:
    try:
        ns["success_callback"]({}, response, start_time, end_time)
        print("Invoked success_callback()")
    except Exception as e:
        print("success_callback raised:", e)
else:
    print("success_callback not found in namespace")

# Force-save persistent stats
if "save_persistent_stats" in ns:
    try:
        ns["save_persistent_stats"](force=True)
        print("Forced save_persistent_stats()")
    except Exception as e:
        print("save_persistent_stats raised:", e)

if pfile and os.path.exists(pfile):
    try:
        print("After:\n", open(pfile, "r", encoding="utf-8").read())
    except Exception as e:
        print("Failed reading after file:", e)

print("smoke_uv_runner completed")

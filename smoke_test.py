#!/usr/bin/env python3
"""Smoke test: import the antropic_proxy script as a module and invoke success_callback
with a synthetic response to verify persistent stats update.
"""
import importlib.util
import time
from dotenv import load_dotenv
load_dotenv()

spec = importlib.util.spec_from_file_location("antropic_proxy", "./antropic_proxy")
module = importlib.util.module_from_spec(spec)
# Execute module (its top-level will run but not __main__ block)
spec.loader.exec_module(module)

print("Imported antropic_proxy module")
print("Persistent file:", module.PERSISTENT_STATS_FILE)

# Show current persistent file contents (if any)
try:
    with open(module.PERSISTENT_STATS_FILE, "r", encoding="utf-8") as f:
        print("Before:\n", f.read())
except FileNotFoundError:
    print("No persistent file yet")

# Build a synthetic response with nested completion_tokens_details.reasoning_tokens
response = {
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "completion_tokens_details": {"reasoning_tokens": 5},
    }
}
start_time = time.time() - 0.5
end_time = time.time()

# Call the success callback (this also updates persistent aggregates)
print("Calling success_callback(...) with synthetic usage")
module.success_callback({}, response, start_time, end_time)

# Force-save persistent stats (the module exposes save_persistent_stats)
try:
    module.save_persistent_stats(force=True)
    print("Forced save of persistent stats")
except Exception as e:
    print("save_persistent_stats failed:", e)

# Read and print the persistent file
try:
    with open(module.PERSISTENT_STATS_FILE, "r", encoding="utf-8") as f:
        print("After:\n", f.read())
except Exception as e:
    print("Failed to read persistent file:", e)

print("Smoke test completed")

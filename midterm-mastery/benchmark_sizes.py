
import csv
import time
import statistics
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError

HOST = "http://file-transfer-gateway-95716430.us-west-2.elb.amazonaws.com"
SIZES = [1, 16, 64]
RUNS = 5

results = []

for run in range(1, RUNS + 1):
    for size in SIZES:
        filename = f"{size}kb.bin"
        expected = Path(f"midterm-mastery/testfiles/{filename}").read_bytes()
        url = f"{HOST}/files?name={filename}"

        start = time.perf_counter()
        status = 0
        valid = False

        try:
            with urlopen(url, timeout=60) as response:
                status = response.status
                content = response.read()
            valid = status == 200 and content == expected
        except HTTPError as e:
            status = e.code
        except Exception as e:
            print(f"Request error: {e}")

        elapsed = round((time.perf_counter() - start) * 1000, 2)

        results.append({
            "size_kb": size,
            "run": run,
            "latency_ms": elapsed,
            "http_status": status,
            "success": valid
        })

        print(f"Run {run} | {size} KB | {elapsed} ms | "
              f"HTTP {status} | {'PASS' if valid else 'FAIL'}")

output = Path("midterm-mastery/results/file_size_results.csv")
with output.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n=== EXPERIMENT 1 SUMMARY ===")
for size in SIZES:
    group = [r for r in results if r["size_kb"] == size]
    successful = [r["latency_ms"] for r in group if r["success"]]

    if successful:
        print(f"{size} KB: "
              f"Mean={statistics.mean(successful):.2f} ms, "
              f"Median={statistics.median(successful):.2f} ms, "
              f"Success={len(successful)}/{RUNS}")
    else:
        print(f"{size} KB: No successful transfers")

print(f"\nSaved results to {output}")

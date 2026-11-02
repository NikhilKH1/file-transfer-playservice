
import csv
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

path = Path("midterm-mastery/results/file_size_results.csv")

with path.open() as f:
    rows = list(csv.DictReader(f))

sizes = [1, 16, 64]
means = []
medians = []

for size in sizes:
    values = [
        float(r["latency_ms"])
        for r in rows
        if int(r["size_kb"]) == size and r["success"] == "True"
    ]
    means.append(statistics.mean(values))
    medians.append(statistics.median(values))

x = range(len(sizes))

plt.figure(figsize=(8, 5))
plt.plot(x, means, marker="o", linewidth=2, label="Mean")
plt.plot(x, medians, marker="s", linewidth=2, label="Median")

plt.xticks(list(x), [f"{s} KB" for s in sizes])
plt.xlabel("File Size")
plt.ylabel("Download Latency (ms)")
plt.title("Experiment 1: File Size vs. Download Latency")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

output = Path("midterm-mastery/results/file_size_latency.png")
plt.savefig(output, dpi=200)

print(f"Graph saved: {output}")
plt.show()


import csv
import matplotlib.pyplot as plt
from pathlib import Path

results_dir = Path("midterm-mastery/results/concurrency")
results_dir.mkdir(parents=True, exist_ok=True)

# Values collected from Locust Statistics screenshots
users = [5, 10, 25, 50]
requests = [82, 159, 217, 391]
failures = [0, 0, 18, 197]
avg_latency = [2877.1, 2907.82, 5606.52, 5952.32]
p95_latency = [6500, 6500, 8800, 7900]

failure_rates = [
    100 * f / n for f, n in zip(failures, requests)
]

# Save measured summary
csv_path = results_dir / "concurrency_summary.csv"

with csv_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "users", "requests", "failures",
        "failure_rate_pct", "avg_latency_ms", "p95_ms"
    ])
    for i in range(len(users)):
        writer.writerow([
            users[i], requests[i], failures[i],
            round(failure_rates[i], 2),
            avg_latency[i], p95_latency[i]
        ])

# Plot failure rates
plt.figure(figsize=(9, 5))
plt.plot(users, failure_rates, marker="o", linewidth=2.5)

for x, y in zip(users, failure_rates):
    plt.annotate(f"{y:.1f}%", (x, y),
                 xytext=(0, 10),
                 textcoords="offset points", ha="center")

plt.xticks(users)
plt.ylim(0, 60)
plt.xlabel("Concurrent Users")
plt.ylabel("Failure Rate (%)")
plt.title("Experiment 2: Concurrency vs. Failure Rate")
plt.grid(True, alpha=0.3)
plt.tight_layout()

output = results_dir / "concurrency_failure_rate.png"
plt.savefig(output, dpi=200)
print("CSV saved:", csv_path)
print("Graph saved:", output)
plt.show()

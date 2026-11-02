
import csv
import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path("midterm-mastery/results/packetloss")
output_dir.mkdir(parents=True, exist_ok=True)

# Results recorded from Locust screenshots
loss = [0, 5, 10]
requests = [82, 40, 35]
failures = [0, 0, 0]
avg_latency = [2877.1, 6124.17, 7387.85]
p95_latency = [6500, 8700, 11000]

# Save the summary as CSV
csv_path = output_dir / "packetloss_summary.csv"

with csv_path.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "send_loss_pct", "requests", "failures",
        "average_latency_ms", "p95_latency_ms"
    ])
    for i in range(len(loss)):
        writer.writerow([
            loss[i], requests[i], failures[i],
            avg_latency[i], p95_latency[i]
        ])

# Generate graph
plt.figure(figsize=(9, 5))

plt.plot(
    loss, avg_latency,
    marker="o", linewidth=2.5,
    label="Average Latency"
)

plt.plot(
    loss, p95_latency,
    marker="s", linewidth=2.5,
    label="P95 Latency"
)

plt.xticks(loss, [f"{x}%" for x in loss])
plt.xlabel("Simulated UDP Send Packet Loss (%)")
plt.ylabel("Response Time (ms)")
plt.title("Experiment 3: UDP Packet Loss vs. Latency")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

output = output_dir / "packetloss_latency.png"
plt.savefig(output, dpi=200)

print("CSV saved:", csv_path)
print("Graph saved:", output)

plt.show()

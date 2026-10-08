import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# READ RESULTS
# ============================================================

df = pd.read_csv("workload_results.csv")


# ============================================================
# CREATE GRAPHS FOLDER
# ============================================================

os.makedirs("graphs", exist_ok=True)


# ============================================================
# DISPLAY DATA
# ============================================================

print("\nWorkload Results:")
print(df.to_string(index=False))


# ============================================================
# GRAPH 1
# Total Requests vs Average Response Time
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Total Requests"],
    df["Response Time (ms)"],
    marker="o"
)

plt.xlabel("Total Requests")
plt.ylabel("Average Response Time (ms)")
plt.title("Total Requests vs Average Response Time")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/response_time.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 2
# Total Requests vs Throughput
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Total Requests"],
    df["Throughput (req/s)"],
    marker="o"
)

plt.xlabel("Total Requests")
plt.ylabel("Throughput (requests/sec)")
plt.title("Total Requests vs Throughput")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/throughput.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 3
# Total Requests vs AVERAGE CPU UTILIZATION
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Total Requests"],
    df["Student Avg CPU (%)"],
    marker="o",
    label="Student Service"
)

plt.plot(
    df["Total Requests"],
    df["Attendance Avg CPU (%)"],
    marker="o",
    label="Attendance Service"
)

plt.plot(
    df["Total Requests"],
    df["Performance Avg CPU (%)"],
    marker="o",
    label="Performance Service"
)

plt.xlabel("Total Requests")
plt.ylabel("Average CPU Utilization (%)")
plt.title("Total Requests vs Average CPU Utilization")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/cpu_utilization.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 4
# Total Requests vs AVERAGE MEMORY UTILIZATION
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Total Requests"],
    df["Student Avg Memory (MiB)"],
    marker="o",
    label="Student Service"
)

plt.plot(
    df["Total Requests"],
    df["Attendance Avg Memory (MiB)"],
    marker="o",
    label="Attendance Service"
)

plt.plot(
    df["Total Requests"],
    df["Performance Avg Memory (MiB)"],
    marker="o",
    label="Performance Service"
)

plt.xlabel("Total Requests")
plt.ylabel("Average Memory Usage (MiB)")
plt.title("Total Requests vs Average Memory Utilization")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/memory_utilization.png",
    dpi=300
)

plt.close()


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("ALL GRAPHS GENERATED SUCCESSFULLY")
print("=" * 60)

print("\nWorkload configuration:")
print("Total Requests : 100, 1000, 2000, 3000, 5000")
print("Concurrency    : 16")

print("\nGraphs saved in:")
print("workload/graphs/")

print("\nFiles generated:")
print("1. response_time.png")
print("2. throughput.png")
print("3. cpu_utilization.png")
print("4. memory_utilization.png")
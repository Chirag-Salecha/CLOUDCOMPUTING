import pandas as pd
import matplotlib.pyplot as plt
import re
import os


# --------------------------------------------------
# Read the workload results
# --------------------------------------------------

df = pd.read_csv("workload_results.csv")


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def parse_cpu(value):
    """
    Convert values such as:
    0.01%
    0.02%
    into a float.
    """
    match = re.search(r"[\d.]+", str(value))

    if match:
        return float(match.group())

    return 0.0


def parse_memory(value):
    """
    Convert values such as:
    26.91MiB / 7.605GiB
    into the used memory value in MiB.
    """
    match = re.search(r"[\d.]+", str(value))

    if match:
        return float(match.group())

    return 0.0


# --------------------------------------------------
# Convert CPU and Memory columns
# --------------------------------------------------

cpu_columns = [
    "Student CPU",
    "Attendance CPU",
    "Performance CPU"
]

memory_columns = [
    "Student Memory",
    "Attendance Memory",
    "Performance Memory"
]

for column in cpu_columns:
    df[column] = df[column].apply(parse_cpu)

for column in memory_columns:
    df[column] = df[column].apply(parse_memory)


# --------------------------------------------------
# Create graphs folder
# --------------------------------------------------

os.makedirs("graphs", exist_ok=True)


# ==================================================
# GRAPH 1
# Concurrent Requests vs Average Response Time
# ==================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Concurrency"],
    df["Response Time (ms)"],
    marker="o"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Average Response Time (ms)")
plt.title("Concurrent Requests vs Average Response Time")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/response_time.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 2
# Concurrent Requests vs Throughput
# ==================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Concurrency"],
    df["Throughput (req/s)"],
    marker="o"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Throughput (requests/sec)")
plt.title("Concurrent Requests vs Throughput")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/throughput.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 3
# Concurrent Requests vs CPU Utilization
# ==================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Concurrency"],
    df["Student CPU"],
    marker="o",
    label="Student Service"
)

plt.plot(
    df["Concurrency"],
    df["Attendance CPU"],
    marker="o",
    label="Attendance Service"
)

plt.plot(
    df["Concurrency"],
    df["Performance CPU"],
    marker="o",
    label="Performance Service"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("CPU Utilization (%)")
plt.title("Concurrent Requests vs CPU Utilization")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/cpu_utilization.png",
    dpi=300
)

plt.show()


# ==================================================
# GRAPH 4
# Concurrent Requests vs Memory Utilization
# ==================================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Concurrency"],
    df["Student Memory"],
    marker="o",
    label="Student Service"
)

plt.plot(
    df["Concurrency"],
    df["Attendance Memory"],
    marker="o",
    label="Attendance Service"
)

plt.plot(
    df["Concurrency"],
    df["Performance Memory"],
    marker="o",
    label="Performance Service"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Memory Usage (MiB)")
plt.title("Concurrent Requests vs Memory Utilization")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "graphs/memory_utilization.png",
    dpi=300
)

plt.show()


print("\n==============================================")
print("ALL GRAPHS GENERATED SUCCESSFULLY")
print("==============================================")

print("\nSaved inside:")
print("workload/graphs/")

print("\nFiles:")
print("1. response_time.png")
print("2. throughput.png")
print("3. cpu_utilization.png")
print("4. memory_utilization.png")
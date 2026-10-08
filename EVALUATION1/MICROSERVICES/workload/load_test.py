import csv
import subprocess
import time
import threading

from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean

import requests


URL = "http://localhost:5001/student-summary/101"

# Total requests for each workload
WORKLOADS = [100, 1000, 2000, 3000, 5000]

# Fixed concurrency
CONCURRENCY = 16

# CPU monitoring interval
MONITOR_INTERVAL = 0.1


# ============================================================
# SEND REQUEST
# ============================================================

def send_request():

    start = time.perf_counter()

    try:

        response = requests.get(
            URL,
            timeout=10
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return {
            "success": response.status_code == 200,
            "response_time": elapsed
        }

    except requests.RequestException:

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return {
            "success": False,
            "response_time": elapsed
        }


# ============================================================
# GET CURRENT DOCKER STATS
# ============================================================

def get_docker_stats():

    services = [
        "student-service",
        "attendance-service",
        "performance-service"
    ]

    stats = {}

    try:

        command = [
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"
        ] + services

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()

        if not output:
            return stats

        for line in output.splitlines():

            parts = line.split("|")

            if len(parts) != 3:
                continue

            service = parts[0].strip()
            cpu = parts[1].strip()
            memory = parts[2].strip()

            stats[service] = {
                "cpu": cpu,
                "memory": memory
            }

    except Exception:
        pass

    return stats


# ============================================================
# PARSE CPU
# ============================================================

def parse_cpu(value):

    try:

        value = str(value).replace("%", "").strip()

        return float(value)

    except Exception:

        return 0.0


# ============================================================
# PARSE MEMORY
# ============================================================

def parse_memory(value):

    try:

        value = str(value)

        # Example:
        # 29.66MiB / 7.605GiB

        number = value.split("MiB")[0]

        return float(number)

    except Exception:

        return 0.0


# ============================================================
# CPU MONITOR
# ============================================================

def monitor_resources(stop_event, samples):

    while not stop_event.is_set():

        stats = get_docker_stats()

        if stats:

            timestamp = time.perf_counter()

            samples.append({
                "timestamp": timestamp,
                "stats": stats
            })

        time.sleep(MONITOR_INTERVAL)


# ============================================================
# RUN WORKLOAD
# ============================================================

def run_workload(total_requests):

    print("\n" + "=" * 65)

    print(
        f"WORKLOAD: {total_requests} TOTAL REQUESTS"
    )

    print(
        f"CONCURRENCY: {CONCURRENCY}"
    )

    print("=" * 65)

    results = []

    resource_samples = []

    stop_monitor = threading.Event()

    # --------------------------------------------------------
    # Start resource monitoring
    # --------------------------------------------------------

    monitor_thread = threading.Thread(
        target=monitor_resources,
        args=(stop_monitor, resource_samples),
        daemon=True
    )

    monitor_thread.start()

    # --------------------------------------------------------
    # Start workload
    # --------------------------------------------------------

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=CONCURRENCY
    ) as executor:

        futures = [
            executor.submit(send_request)
            for _ in range(total_requests)
        ]

        for future in as_completed(futures):

            results.append(
                future.result()
            )

    total_time = (
        time.perf_counter() - start_time
    )

    # --------------------------------------------------------
    # Stop monitoring
    # --------------------------------------------------------

    stop_monitor.set()

    monitor_thread.join(
        timeout=2
    )

    # --------------------------------------------------------
    # Request statistics
    # --------------------------------------------------------

    successful = sum(
        1
        for r in results
        if r["success"]
    )

    failed = (
        len(results) - successful
    )

    average_response_time = mean(
        r["response_time"]
        for r in results
    )

    throughput = (
        successful / total_time
        if total_time > 0
        else 0
    )

    # ========================================================
    # RESOURCE ANALYSIS
    # ========================================================

    services = [
        "student-service",
        "attendance-service",
        "performance-service"
    ]

    resource_stats = {}

    for service in services:

        cpu_values = []
        memory_values = []

        for sample in resource_samples:

            stats = sample["stats"]

            if service in stats:

                cpu_values.append(
                    parse_cpu(
                        stats[service]["cpu"]
                    )
                )

                memory_values.append(
                    parse_memory(
                        stats[service]["memory"]
                    )
                )

        if cpu_values:

            average_cpu = mean(
                cpu_values
            )

            peak_cpu = max(
                cpu_values
            )

        else:

            average_cpu = 0
            peak_cpu = 0

        if memory_values:

            average_memory = mean(
                memory_values
            )

            peak_memory = max(
                memory_values
            )

        else:

            average_memory = 0
            peak_memory = 0

        resource_stats[service] = {

            "average_cpu": round(
                average_cpu,
                2
            ),

            "peak_cpu": round(
                peak_cpu,
                2
            ),

            "average_memory": round(
                average_memory,
                2
            ),

            "peak_memory": round(
                peak_memory,
                2
            )
        }

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print(
        f"Total Requests       : {len(results)}"
    )

    print(
        f"Successful Requests  : {successful}"
    )

    print(
        f"Failed Requests      : {failed}"
    )

    print(
        f"Average Response     : "
        f"{average_response_time:.2f} ms"
    )

    print(
        f"Throughput           : "
        f"{throughput:.2f} requests/sec"
    )

    print("\nResource Utilization During Workload:")

    for service in services:

        data = resource_stats[service]

        print(
            f"{service:22} "
            f"Avg CPU={data['average_cpu']:>7.2f}% "
            f"Peak CPU={data['peak_cpu']:>7.2f}% "
            f"Avg Mem={data['average_memory']:>7.2f} MiB "
            f"Peak Mem={data['peak_memory']:>7.2f} MiB"
        )

    print(
        f"\nCPU samples collected: "
        f"{len(resource_samples)}"
    )

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "requests": total_requests,

        "concurrency": CONCURRENCY,

        "response_time": round(
            average_response_time,
            2
        ),

        "throughput": round(
            throughput,
            2
        ),

        "failed": failed,

        "stats": resource_stats
    }


# ============================================================
# MAIN
# ============================================================

def main():

    results = []

    print("\nStarting workload testing...")

    print(
        f"Target API: {URL}"
    )

    print(
        f"Workloads: {WORKLOADS}"
    )

    print(
        f"Concurrency: {CONCURRENCY}"
    )

    print(
        f"CPU monitoring interval: "
        f"{MONITOR_INTERVAL} seconds"
    )

    # --------------------------------------------------------
    # Run all workloads
    # --------------------------------------------------------

    for total_requests in WORKLOADS:

        result = run_workload(
            total_requests
        )

        results.append(result)

        # Pause between workloads
        time.sleep(3)

    # ========================================================
    # SAVE CSV
    # ========================================================

    with open(
        "workload_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "Workload",

            "Total Requests",

            "Concurrency",

            "Response Time (ms)",

            "Throughput (req/s)",

            "Failed Requests",

            "Student Avg CPU (%)",

            "Student Peak CPU (%)",

            "Student Avg Memory (MiB)",

            "Student Peak Memory (MiB)",

            "Attendance Avg CPU (%)",

            "Attendance Peak CPU (%)",

            "Attendance Avg Memory (MiB)",

            "Attendance Peak Memory (MiB)",

            "Performance Avg CPU (%)",

            "Performance Peak CPU (%)",

            "Performance Avg Memory (MiB)",

            "Performance Peak Memory (MiB)"
        ])

        # ----------------------------------------------------
        # Write each workload
        # ----------------------------------------------------

        for index, result in enumerate(
            results,
            start=1
        ):

            student = result["stats"][
                "student-service"
            ]

            attendance = result["stats"][
                "attendance-service"
            ]

            performance = result["stats"][
                "performance-service"
            ]

            writer.writerow([

                f"W{index}",

                result["requests"],

                result["concurrency"],

                result["response_time"],

                result["throughput"],

                result["failed"],

                student["average_cpu"],

                student["peak_cpu"],

                student["average_memory"],

                student["peak_memory"],

                attendance["average_cpu"],

                attendance["peak_cpu"],

                attendance["average_memory"],

                attendance["peak_memory"],

                performance["average_cpu"],

                performance["peak_cpu"],

                performance["average_memory"],

                performance["peak_memory"]
            ])

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n" + "=" * 65)

    print(
        "WORKLOAD TEST COMPLETE"
    )

    print("=" * 65)

    print(
        "\nResults saved to workload_results.csv"
    )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()
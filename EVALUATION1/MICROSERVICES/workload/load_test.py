import csv
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean

import requests


URL = "http://localhost:5001/student-summary/101"

WORKLOADS = [1, 2, 4, 8, 16]

# Number of requests performed for each workload level
REQUESTS_PER_WORKLOAD = 100


def send_request():
    start = time.perf_counter()

    try:
        response = requests.get(URL, timeout=10)
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": response.status_code == 200,
            "response_time": elapsed
        }

    except requests.RequestException:
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": False,
            "response_time": elapsed
        }


def get_docker_stats():
    services = [
        "student-service",
        "attendance-service",
        "performance-service"
    ]

    stats = {}

    for service in services:
        try:
            result = subprocess.run(
                [
                    "docker",
                    "stats",
                    service,
                    "--no-stream",
                    "--format",
                    "{{.CPUPerc}}|{{.MemUsage}}"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout.strip()

            if output:
                cpu, memory = output.split("|", 1)
                stats[service] = {
                    "cpu": cpu.strip(),
                    "memory": memory.strip()
                }
            else:
                stats[service] = {
                    "cpu": "N/A",
                    "memory": "N/A"
                }

        except Exception:
            stats[service] = {
                "cpu": "N/A",
                "memory": "N/A"
            }

    return stats


def run_workload(concurrency):
    print("\n" + "=" * 60)
    print(f"WORKLOAD: {concurrency} CONCURRENT REQUESTS")
    print("=" * 60)

    results = []

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:

        futures = [
            executor.submit(send_request)
            for _ in range(REQUESTS_PER_WORKLOAD)
        ]

        for future in as_completed(futures):
            results.append(future.result())

    total_time = time.perf_counter() - start_time

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    average_response_time = mean(
        r["response_time"] for r in results
    )

    throughput = successful / total_time

    stats = get_docker_stats()

    print(f"Total Requests       : {len(results)}")
    print(f"Successful Requests  : {successful}")
    print(f"Failed Requests      : {failed}")
    print(f"Average Response     : {average_response_time:.2f} ms")
    print(f"Throughput           : {throughput:.2f} requests/sec")

    for service, data in stats.items():
        print(
            f"{service:22} "
            f"CPU={data['cpu']:>8} "
            f"Memory={data['memory']}"
        )

    return {
        "concurrency": concurrency,
        "response_time": round(average_response_time, 2),
        "throughput": round(throughput, 2),
        "failed": failed,
        "stats": stats
    }


def main():
    results = []

    print("\nStarting workload testing...")
    print(f"Target API: {URL}")
    print(f"Requests per workload: {REQUESTS_PER_WORKLOAD}")

    for concurrency in WORKLOADS:
        result = run_workload(concurrency)
        results.append(result)

        # Small pause between workload levels
        time.sleep(2)

    with open(
        "workload_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Workload",
            "Concurrency",
            "Response Time (ms)",
            "Throughput (req/s)",
            "Failed Requests",
            "Student CPU",
            "Student Memory",
            "Attendance CPU",
            "Attendance Memory",
            "Performance CPU",
            "Performance Memory"
        ])

        for index, result in enumerate(results, start=1):

            student = result["stats"]["student-service"]
            attendance = result["stats"]["attendance-service"]
            performance = result["stats"]["performance-service"]

            writer.writerow([
                f"W{index}",
                result["concurrency"],
                result["response_time"],
                result["throughput"],
                result["failed"],
                student["cpu"],
                student["memory"],
                attendance["cpu"],
                attendance["memory"],
                performance["cpu"],
                performance["memory"]
            ])

    print("\n" + "=" * 60)
    print("WORKLOAD TEST COMPLETE")
    print("=" * 60)
    print("Results saved to workload_results.csv")


if __name__ == "__main__":
    main()
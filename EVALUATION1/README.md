# Student Performance Management - Containerized Microservice Application

**Experiment:** Build, Deploy and Analyze a Containerized Microservice Application Under Varying Workloads  
**Domain:** Student Performance Management  
**Author:** Chirag Salecha

---
## Team Members

| Name |
|---|
| **Chirag Salecha** |
| **Achyuth RH** |
| **Adarsh MR** |

## 1. Aim
To develop a microservice-based application with three independent services, containerize and deploy them using Docker and Docker Compose, establish inter-service communication, generate varying workloads, monitor resource utilization, and analyze application performance.

## 2. Technologies Used
- Python 3.x with Flask (REST APIs)
- Gunicorn (production server inside containers)
- Docker and Docker Compose
- Python `requests` and `threading` (load generator)
- `docker stats` (CPU and memory monitoring)
- Matplotlib (graphs)
- PowerShell
- VS Code

## 3. Test Environment
- OS: Windows 11 with PowerShell
- Docker Desktop
- Docker Engine
- Docker Compose
- Python 3.x
- Docker containers connected through a common Docker network
- Fixed concurrency: 16
- Workload levels: 100, 1000, 2000, 3000, and 5000 requests

## 4. Architecture

    Client --> student-service (Service 1) --> attendance-service (Service 2)
                                             --> performance-service (Service 3)

All three services run as separate containers on one Docker network. The student-service acts as the entry point and communicates with the attendance-service and performance-service using Docker service names, not localhost.

## 5. Microservices

| Service | Port | Responsibility |
|---|---|---|
| student-service | 5001 | Entry point. Provides student information and generates a combined student summary |
| attendance-service | 5002 | Stores and returns student attendance information |
| performance-service | 5003 | Stores and returns student academic performance information |

### 5.1 student-service (port 5001)
| Endpoint | Description |
|---|---|
| GET /health | Health check |
| GET /students | List all students |
| GET /students/<id> | Get one student |
| GET /student-summary/<id> | Calls attendance-service and performance-service and returns a combined response |

### 5.2 attendance-service (port 5002)
| Endpoint | Description |
|---|---|
| GET /health | Health check |
| GET /attendance/<id> | Get attendance information for a student |

### 5.3 performance-service (port 5003)
| Endpoint | Description |
|---|---|
| GET /health | Health check |
| GET /performance/<id> | Get academic performance information for a student |

### 5.4 Example end-to-end response (GET /student-summary/101)

    {
      "student": {
        "id": 101
      },
      "attendance": {
        "percentage": 85
      },
      "performance": {
        "marks": 88
      }
    }

## 6. Project Structure

    MICROSERVICES/
    |-- student-service/       (app.py, requirements.txt, Dockerfile)
    |-- attendance-service/    (app.py, requirements.txt, Dockerfile)
    |-- performance-service/   (app.py, requirements.txt, Dockerfile)
    |-- docker-compose.yml
    |-- workload/
    |   |-- load_test.py
    |   |-- workload_results.csv
    |   `-- graphs/
    |       |-- response_time.png
    |       |-- throughput.png
    |       |-- cpu_utilization.png
    |       `-- memory_utilization.png
    |-- README.md

---

## 7. Checkpoint 1 - Design and Develop the Microservices

1. Domain selected: Student Performance Management.
2. Three independent microservices identified: student, attendance, performance.
3. Responsibility of each service defined (see section 5).
4. Services implemented in Python using Flask.
5. REST API endpoints created for every service.
6. Each service was run and tested independently.
7. All APIs returned the expected responses.
8. The services were then prepared for Docker deployment.

Test the services locally before containerization:

    cd student-service
    python app.py

The attendance-service and performance-service can be tested in the same way.

## 8. Checkpoint 2 - Containerize and Deploy

1. A separate Dockerfile was created for each service.
2. Each service has its own `requirements.txt`.
3. A Docker image was built for each service.
4. Images were verified with `docker images`.
5. `docker-compose.yml` was created.
6. All three services are configured in Docker Compose.
7. Docker Compose creates a common network for the services.
8. The application is deployed using Docker Compose.
9. All three containers are verified using `docker ps`.

Docker Compose deployment:

    docker compose up --build -d

Verify images:

    docker images

Verify containers:

    docker ps

The services are exposed on:

    student-service      -> 5001
    attendance-service   -> 5002
    performance-service  -> 5003

## 9. Checkpoint 3 - Microservice Communication

1. The Docker network is created through Docker Compose.
2. All three services are connected to the same network.
3. student-service communicates with attendance-service and performance-service.
4. Docker service names are used for inter-service communication.
5. `localhost` is not used for communication between containers.
6. Communication between services was tested successfully.
7. An end-to-end request through all three services was performed.
8. The final combined student response was returned to the client.

Main end-to-end API:

    curl http://localhost:5001/student-summary/101

PowerShell:

    Invoke-RestMethod http://localhost:5001/student-summary/101 | ConvertTo-Json -Depth 5

Check Docker networks:

    docker network ls

Check student-service logs:

    docker compose logs student-service

Check attendance-service logs:

    docker compose logs attendance-service

Check performance-service logs:

    docker compose logs performance-service

## 10. Checkpoint 4 - Workload Generation and Monitoring

1. API selected for testing: `GET /student-summary/101`.
2. The selected API touches all three services.
3. Load generator: custom Python script `load_test.py`.
4. Python `requests` and `threading` are used for generating concurrent requests.
5. A fixed concurrency of 16 is used for all workload levels.
6. Five workload levels are tested: 100, 1000, 2000, 3000, and 5000 requests.
7. Average response time and throughput are recorded.
8. Successful and failed requests are counted.
9. All three containers are monitored using `docker stats`.
10. CPU and memory utilization are observed for every service.
11. Resource monitoring is performed while the workload is active.
12. Results are stored for further analysis.
13. A total of 11,100 requests are executed across all five workload levels.

Run the workload test:

    cd workload
    python load_test.py

Monitor the containers:

    docker stats

The monitoring interval is 0.1 seconds.

Results are stored in the workload directory:

    workload/workload_results.csv

Graphs are stored in:

    workload/graphs/

## 11. Checkpoint 5 - Results and Analysis

### 11.1 Observation Table

All workload tests were executed with a fixed concurrency of 16.

| Workload | Total Requests | Concurrency | Avg Response Time (ms) | Throughput (req/s) | Failed |
|---|---:|---:|---:|---:|---:|
| W1 | 100 | 16 | 69.36 | 217.15 | 0 |
| W2 | 1000 | 16 | 53.62 | 294.83 | 0 |
| W3 | 2000 | 16 | 52.99 | 300.41 | 0 |
| W4 | 3000 | 16 | 55.35 | 287.93 | 0 |
| W5 | 5000 | 16 | 55.41 | 287.80 | 0 |

Total requests executed:

    100 + 1000 + 2000 + 3000 + 5000 = 11100 requests

All 11,100 requests were completed successfully with zero failed requests.

### 11.2 CPU Utilization (%)

The values below represent the average CPU utilization recorded during each workload.

| Workload | Total Requests | Concurrency | student-service | attendance-service | performance-service |
|---|---:|---:|---:|---:|---:|
| W1 | 100 | 16 | 53.41 | 0.01 | 0.01 |
| W2 | 1000 | 16 | 87.44 | 21.26 | 21.59 |
| W3 | 2000 | 16 | 101.90 | 24.70 | 24.48 |
| W4 | 3000 | 16 | 112.82 | 27.27 | 27.26 |
| W5 | 5000 | 16 | 123.30 | 29.71 | 30.02 |

Peak CPU utilization recorded:

| Workload | student-service | attendance-service | performance-service |
|---|---:|---:|---:|
| W1 | 53.41% | 0.01% | 0.01% |
| W2 | 135.01% | 32.97% | 33.68% |
| W3 | 136.54% | 33.21% | 33.61% |
| W4 | 136.80% | 34.05% | 33.08% |
| W5 | 136.35% | 33.07% | 33.35% |

### 11.3 Memory Utilization (MiB)

The values below represent the average memory utilization recorded during each workload.

| Workload | Total Requests | Concurrency | student-service | attendance-service | performance-service |
|---|---:|---:|---:|---:|---:|
| W1 | 100 | 16 | 27.40 | 21.89 | 21.84 |
| W2 | 1000 | 16 | 28.66 | 22.05 | 21.99 |
| W3 | 2000 | 16 | 29.87 | 22.17 | 22.39 |
| W4 | 3000 | 16 | 30.34 | 22.09 | 22.01 |
| W5 | 5000 | 16 | 31.47 | 22.21 | 22.11 |

Peak memory utilization recorded:

| Workload | student-service | attendance-service | performance-service |
|---|---:|---:|---:|
| W1 | 27.40 MiB | 21.89 MiB | 21.84 MiB |
| W2 | 29.35 MiB | 22.20 MiB | 22.18 MiB |
| W3 | 30.81 MiB | 22.52 MiB | 22.79 MiB |
| W4 | 31.04 MiB | 22.22 MiB | 22.16 MiB |
| W5 | 32.10 MiB | 22.52 MiB | 22.57 MiB |

### 11.4 Graphs

**Total Requests vs Average Response Time**

![Response Time](./MICROSERVICES/workload/graphs/response_time.png)

**Total Requests vs Throughput**

![Throughput](./MICROSERVICES/workload/graphs/throughput.png)

**Total Requests vs CPU Utilization**

![CPU Utilization](./MICROSERVICES/workload/graphs/cpu_utilization.png)

**Total Requests vs Memory Utilization**

![Memory Utilization](./MICROSERVICES/workload/graphs/memory_utilization.png)


### 11.5 Analysis

1. **Response time:** The average response time was 69.36 ms for 100 requests and decreased to 52.99 ms at 2,000 requests. At higher workloads, the response time increased slightly to 55.35 ms and 55.41 ms for 3,000 and 5,000 requests respectively.

2. **Throughput:** Throughput increased from 217.15 req/s at 100 requests to a maximum of 300.41 req/s at 2,000 requests. After reaching this level, throughput stabilized around 288 req/s at 3,000 and 5,000 requests, indicating that the system was approaching its processing capacity.

3. **Failures:** All five workload levels completed successfully with zero failed requests. A total of 11,100 requests were processed without failures.

4. **Resource usage:** CPU utilization increased with workload. The student-service showed the highest CPU utilization because it acts as the entry point and handles the end-to-end request while communicating with the other services.

5. **Memory:** student-service memory utilization increased gradually from 27.40 MiB to 31.47 MiB as workload increased. Attendance-service and performance-service remained relatively stable around 22 MiB.

6. **Service dependency:** student-service is the entry point and communicates with attendance-service and performance-service. Therefore, the performance of the end-to-end request depends on all three services.

7. **Bottleneck:** student-service is the primary resource-consuming service in the experiment. Its average CPU utilization increased from 53.41% at 100 requests to 123.30% at 5,000 requests.

8. **Performance degradation:** After the throughput peak of 300.41 req/s at 2,000 requests, throughput decreased slightly to 287.93 req/s at 3,000 requests and 287.80 req/s at 5,000 requests. This indicates that the system is approaching saturation under the fixed concurrency of 16.

9. **Scalability:** Since the services are independently containerized, individual services can be scaled according to their workload. The results show that the current deployment handled all tested workload levels successfully, while student-service became increasingly CPU intensive.

10. **CPU interpretation:** Docker CPU utilization can exceed 100% because the value represents usage relative to a single CPU core. Therefore, the measured 123.30% average CPU utilization for student-service at 5,000 requests represents approximately 1.23 CPU cores of utilization.

11. **Best measured workload:** The 2,000-request workload produced the highest measured throughput of 300.41 req/s and the lowest measured average response time of 52.99 ms among the five workload levels.

### 11.6 Conclusion

The workload experiment was successfully completed using five request volumes of 100, 1000, 2000, 3000, and 5000 requests with a fixed concurrency of 16.

The system processed all 11,100 requests successfully with zero failures.

The highest measured throughput was 300.41 req/s at 2,000 requests, while the lowest measured response time was 52.99 ms at the same workload. At 3,000 and 5,000 requests, throughput remained around 288 req/s, showing that the system was approaching a stable processing capacity.

CPU utilization increased with workload, particularly for student-service, while memory usage increased gradually and remained stable for the attendance-service and performance-service.

The experiment demonstrates how containerized microservices can be monitored and analyzed under increasing request volumes and how workload testing can be used to identify resource usage and performance saturation.

---

## 12. Checkpoint 6 - Docker Resource Monitoring

Docker provides real-time resource statistics using:

    docker stats

The following services were monitored:

    student-service
    attendance-service
    performance-service

The following parameters were observed:

- CPU %
- Memory Usage
- Memory %
- Network Input/Output
- Block Input/Output
- Number of Processes

The resource monitoring was performed at an interval of 0.1 seconds while the workload was active.

The collected information was used to understand the resource consumption of each microservice under different workloads.

The monitoring results showed that student-service consumed the highest CPU resources as the request volume increased, while attendance-service and performance-service maintained comparatively lower CPU and stable memory utilization.

## 13. Checkpoint 7 - Scalability Analysis

The application was tested with increasing request volumes while maintaining a fixed concurrency level of 16:

    100 -> 1000 -> 2000 -> 3000 -> 5000 total requests

The purpose of this experiment was to determine:

1. How response time changes with increasing request volume.
2. How throughput changes with increasing request volume.
3. How CPU utilization changes.
4. How memory utilization changes.
5. Whether any microservice becomes a bottleneck.
6. Whether the application remains stable under increased workload.
7. At which workload the application begins to approach saturation.

The results showed that throughput increased up to 300.41 req/s at 2,000 requests. At 3,000 and 5,000 requests, throughput remained close to 288 req/s while response time increased slightly.

The results can be used to determine the approximate workload at which the current deployment begins to saturate.

## 14. Complete Microservice Request Flow

    Client
      |
      v
    student-service
      |
      +------> attendance-service
      |
      +------> performance-service
      |
      v
    Combined Student Summary
      |
      v
    Client

The student-service acts as the entry point. It receives the request from the client and obtains the required attendance and performance information from the corresponding services.

## 15. Microservice Performance Analysis

### Student Service

student-service is the main entry point of the application.

Responsibilities:

- Accept client requests.
- Provide student information.
- Request attendance information.
- Request performance information.
- Return a combined student summary.

Performance observation:

- student-service showed the highest CPU utilization among the three services.
- Average CPU utilization increased from 53.41% at 100 requests to 123.30% at 5,000 requests.
- Peak CPU utilization reached 136.80% during the tested workloads.
- Average memory increased from 27.40 MiB to 31.47 MiB.
- The service is therefore the primary resource-consuming component in the tested deployment.

### Attendance Service

attendance-service handles attendance-related information.

Responsibilities:

- Provide health status.
- Return attendance information for a student.
- Process requests independently from the other services.

Performance observation:

- Average CPU utilization increased from 0.01% at 100 requests to 29.71% at 5,000 requests.
- Peak CPU utilization reached 34.05%.
- Average memory remained close to 22 MiB throughout the workloads.
- The service remained stable under all tested workloads.

### Performance Service

performance-service handles academic performance information.

Responsibilities:

- Provide health status.
- Return performance information for a student.
- Process performance requests independently.

Performance observation:

- Average CPU utilization increased from 0.01% at 100 requests to 30.02% at 5,000 requests.
- Peak CPU utilization reached 33.68%.
- Average memory remained close to 22 MiB throughout the workloads.
- The service remained stable under all tested workloads.

## 16. Advantages of the Containerized Architecture

1. Each microservice runs independently.
2. Each service can be developed and tested separately.
3. Each service can be deployed as an individual container.
4. Docker Compose simplifies multi-container deployment.
5. Docker networking enables service-to-service communication.
6. Resource utilization can be monitored independently.
7. Individual services can be scaled according to workload.
8. Service-level isolation is provided.
9. The application is portable across systems supporting Docker.
10. The architecture demonstrates practical microservice deployment.

## 17. Limitations

1. The experiment is performed on a single host machine.
2. Docker Desktop is used as the container runtime environment.
3. The workload is synthetic and may not represent a real production workload.
4. The services use simple application-level data.
5. No external database is required for the basic implementation.
6. Network latency between containers depends on the local Docker environment.
7. Resource measurements can vary depending on background processes on the host machine.
8. The experiment does not represent a multi-node Kubernetes deployment.
9. The workload experiment uses a fixed concurrency of 16.
10. The observed throughput represents the tested local Docker environment and hardware configuration.

## 18. Conclusion

The experiment successfully demonstrates the development and deployment of a containerized microservice application using Docker and Docker Compose.

Three independent services were implemented:

    student-service
    attendance-service
    performance-service

The services were containerized and deployed independently while communicating through a common Docker network.

The end-to-end API:

    GET /student-summary/101

was used to generate workloads and evaluate application performance.

Five workload levels were tested:

    100 requests
    1000 requests
    2000 requests
    3000 requests
    5000 requests

All tests were executed with a fixed concurrency of 16.

A total of 11,100 requests were processed with zero failures.

Performance was analyzed using:

- Response time
- Throughput
- CPU utilization
- Memory utilization
- Successful requests
- Failed requests

The highest measured throughput was 300.41 req/s at 2,000 requests, while the lowest measured average response time was 52.99 ms at the same workload.

At higher workloads, throughput stabilized around 288 req/s, indicating that the current deployment was approaching its processing capacity.

CPU utilization increased with workload, with student-service showing the highest resource consumption. Memory utilization increased gradually for student-service while remaining relatively stable for attendance-service and performance-service.

The experiment demonstrates that a microservice architecture allows individual services to be independently developed, deployed, monitored, and scaled.

Workload testing also helps identify performance bottlenecks and understand how the application behaves as request volume increases.

---

## 19. How to Run

The project is stored locally at:

    D:\5TH SEM\CC\EVALUATION-1\MICROSERVICES

Open PowerShell and navigate to the project directory:

    cd "D:\5TH SEM\CC\EVALUATION-1\MICROSERVICES"

Build and start all services:

    docker compose up --build -d

Check running containers:

    docker ps

Expected services:

    student-service
    attendance-service
    performance-service

Test student-service:

    curl http://localhost:5001/health

Test attendance-service:

    curl http://localhost:5002/health

Test performance-service:

    curl http://localhost:5003/health

Test the complete application:

    curl http://localhost:5001/student-summary/101

PowerShell alternative:

    Invoke-RestMethod http://localhost:5001/student-summary/101 | ConvertTo-Json -Depth 5

Monitor resource utilization:

    docker stats

Run workload testing:

    cd workload
    python load_test.py

The workload results are generated in:

    workload/workload_results.csv

The graphs are generated in:

    workload/graphs/

Stop the application:

    docker compose down

## 20. Useful Docker Commands

### View all containers

    docker ps -a

### View Docker images

    docker images

### View Docker networks

    docker network ls

### View all service logs

    docker compose logs

### View student-service logs

    docker compose logs student-service

### View attendance-service logs

    docker compose logs attendance-service

### View performance-service logs

    docker compose logs performance-service

### Follow live logs

    docker compose logs -f

### Restart the application

    docker compose restart

### Stop containers

    docker compose stop

### Remove containers and network

    docker compose down

### Rebuild the application

    docker compose up --build -d

## 21. Final Deliverables Checklist

- [x] Source code of the three microservices
- [x] student-service
- [x] attendance-service
- [x] performance-service
- [x] Three Dockerfiles
- [x] Individual requirements files
- [x] docker-compose.yml
- [x] Docker images
- [x] Running Docker containers
- [x] Docker network
- [x] Inter-service communication
- [x] End-to-end student summary API
- [x] Workload generation script
- [x] Fixed concurrency workload testing
- [x] 100-request workload test
- [x] 1000-request workload test
- [x] 2000-request workload test
- [x] 3000-request workload test
- [x] 5000-request workload test
- [x] 11,100 total workload requests
- [x] CPU monitoring
- [x] Memory monitoring
- [x] 0 failed requests
- [x] Performance results
- [x] Performance graphs
- [x] Workload analysis
- [x] Bottleneck analysis
- [x] Scalability analysis
- [x] Throughput saturation analysis
- [x] Conclusion
- [x] README documentation

# 📡 OpenTelemetry Instrumentation Pipeline  
### FastAPI • OpenTelemetry Collector • Jaeger • Prometheus • Docker Compose

A fully‑instrumented observability pipeline demonstrating distributed tracing, metrics collection, and end‑to‑end telemetry flow using modern OpenTelemetry tooling.

---

## 🚀 Features

- **FastAPI app** instrumented with OpenTelemetry SDK  
- **Automatic & custom spans** (`hello-span`, `compute-span`)  
- **OTLP gRPC/HTTP export**  
- **OpenTelemetry Collector** with batch processing  
- **Jaeger UI** for trace visualization  
- **Prometheus** metrics scraping  
- **Docker Compose** orchestration  
- Clean, modular project structure  

---

## 🏗 Architecture (ASCII)

```
                   +----------------------+
                   |     FastAPI App      |
                   |  (OTel SDK Enabled)  |
                   +----------+-----------+
                              |
                              |  OTLP gRPC (4317)
                              v
                   +------------------------------+
                   |   OpenTelemetry Collector    |
                   |  - OTLP Receiver             |
                   |  - Batch Processor           |
                   |  - Jaeger Exporter           |
                   |  - Prometheus Metrics        |
                   +--------+-----------+---------+
                            |           |
                            |           |
                            |           |  Metrics Scrape
                            |           v
                            |   +------------------+
                            |   |   Prometheus     |
                            |   +------------------+
                            |
                            |  Traces Export
                            v
                   +------------------------------+
                   |            Jaeger            |
                   |     (Query + UI + Storage)   |
                   +------------------------------+
                              |
                              |  Web UI (16686)
                              v
                   +------------------------------+
                   |           Browser            |
                   +------------------------------+
```

---

## 🔍 Trace Flow Diagram (ASCII)

```
+------------------+
|  User Request    |
+--------+---------+
         |
         v
+------------------+
|   FastAPI App    |
|  (Creates Span)  |
+--------+---------+
         |
         |  OTLP gRPC
         v
+--------------------------+
|  OpenTelemetry Collector |
|  - Receives spans        |
|  - Batches               |
|  - Exports to Jaeger     |
+--------+-----------------+
         |
         |  Jaeger Export
         v
+--------------------------+
|         Jaeger           |
|  - Stores spans          |
|  - Query service         |
|  - UI visualization      |
+--------+-----------------+
         |
         |  UI
         v
+--------------------------+
|        Browser           |
|  (Trace Visualization)   |
+--------------------------+
```

---

## 🐳 Docker Compose Topology (ASCII)

```
+---------------------------+
|        docker-compose     |
+---------------------------+
        |        |        |
        |        |        |
        v        v        v

+-------------+   +----------------+   +------------------+
|   FastAPI   |   |   Collector    |   |    Prometheus    |
|   Service   |   | (otelcol)      |   |                  |
|  port 8000  |   | ports 4317/18  |   |   port 9090      |
+------+------+   +--------+-------+   +---------+--------+
       |                   |                     |
       |                   |                     |
       |                   |                     |
       |                   |                     |
       v                   v                     |
+-------------+     +-------------+              |
|   Jaeger    |<----|   Traces    |              |
|   UI 16686  |     |   Export    |              |
+-------------+     +-------------+              |
                                                  |
                                                  |
                                                  v
                                        +------------------+
                                        |   Metrics Scrape |
                                        +------------------+
```

---

## 📁 Project Structure

```
otel-instrumentation-pipeline/
│
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       └── main.py
│
├── collector/
│   └── collector-config.yaml
│
├── docker-compose.yaml
└── README.md
```

---

## ▶️ Run the Pipeline

```bash
docker-compose up --build
```

### Services

| Service      | URL |
|--------------|-----|
| FastAPI App  | http://localhost:8000 |
| Jaeger UI    | http://localhost:16686 |
| Prometheus   | http://localhost:9090 |

---

## 📦 Example Endpoints

### `GET /hello`
Creates a simple span and returns a greeting.

### `GET /compute`
Creates a nested span and performs a simulated computation.

Both appear in Jaeger under your service name.

---

## 🧠 How It Works

### FastAPI App  
- Uses OpenTelemetry SDK  
- Exports traces to Collector via OTLP gRPC  

### OpenTelemetry Collector  
- Receives traces & metrics  
- Batches and exports traces to Jaeger  
- Exposes Prometheus metrics  

### Jaeger  
- Displays traces in a modern UI  

### Prometheus  
- Scrapes metrics from Collector  

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Tracing%20%7C%20Metrics-purple?logo=opentelemetry)
![Jaeger](https://img.shields.io/badge/Jaeger-Tracing-orange?logo=jaeger)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-orange?logo=prometheus)

## 🔬 How Tracing Works Internally

This project uses OpenTelemetry to instrument a FastAPI application and export
telemetry to the OpenTelemetry Collector. Here's the internal flow:

1. **Incoming Request**
   - A user hits an endpoint (`/hello`, `/compute`).
   - FastAPI middleware (from OTel) automatically creates a *root span*.

2. **Application Logic**
   - Custom spans (`hello-span`, `compute-span`) are created inside the handler.
   - Span attributes (metadata) are added to enrich trace context.

3. **OTLP Export (Client → Collector)**
   - The OTel SDK batches spans.
   - Spans are exported via **OTLP gRPC** to the Collector on port **4317**.

4. **Collector Processing**
   - Collector receives spans.
   - Applies processors (batching, memory optimization).
   - Sends spans to Jaeger using the **Jaeger exporter**.

5. **Jaeger Storage + Query**
   - Jaeger stores spans.
   - Jaeger Query service exposes them to the UI.

6. **Visualization**
   - Jaeger UI (port 16686) displays:
     - Trace timeline
     - Span hierarchy
     - Latency breakdown
     - Attributes & events

7. **Metrics Path**
   - Collector exposes metrics on `/metrics`.
   - Prometheus scrapes metrics on port **9090**.

## 🚀 Future Enhancements

These are planned improvements to evolve this project into a full observability stack:

### 🔧 Tracing
- Add **tail-based sampling** for high-volume workloads
- Add **Tempo** as a scalable trace backend
- Add **trace ID propagation** across external services

### 📊 Metrics
- Add **Grafana dashboards** for latency, throughput, and error rates
- Add **custom application metrics** (counters, histograms)

### 📜 Logging
- Integrate **Loki** for centralized log aggregation
- Add **structured JSON logs** with trace correlation

### ☸️ Deployment
- Add **Kubernetes manifests** (Helm chart or Kustomize)
- Add **Azure Container Apps** or **AKS** deployment guide

### 🔐 Reliability & Security
- Add **OTel Collector tail sampling policies**
- Add **rate limiting** and **circuit breakers** in FastAPI

### 🧪 Testing
- Add **pytest** suite for endpoints and tracing
- Add **load testing** with k6 or Locust




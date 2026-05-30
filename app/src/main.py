from fastapi import FastAPI
import time
import random

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure OTel
resource = Resource(attributes={
    "service.name": "otel-demo-service",
    "service.version": "1.0.0",
    "deployment.environment": "local"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# FastAPI app
app = FastAPI()

# Auto-instrumentation
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
SQLite3Instrumentor().instrument()

@app.get("/hello")
def hello():
    with tracer.start_as_current_span("hello-span"):
        time.sleep(random.uniform(0.1, 0.5))
        return {"message": "Hello from OpenTelemetry!"}

@app.get("/compute")
def compute():
    with tracer.start_as_current_span("compute-span"):
        result = sum([i * random.random() for i in range(10000)])
        return {"result": result}

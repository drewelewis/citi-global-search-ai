from typing import Union

from fastapi import FastAPI
import random
import time

from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.semconv.trace import SpanAttributes

trace.set_tracer_provider(
TracerProvider(
        resource=Resource.create({SERVICE_NAME: "openai-service"})
    )
)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)


delay_counter = meter.create_counter(
    "delay_counter",
    description="The amount of delay in processing requests",
)

# create a JaegerExporter
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)


app = FastAPI()


@app.get("/")
def index():
    span_name="index" 
    with tracer.start_as_current_span(span_name) as span:
       do_work("a")
       do_work("b")
       do_work("c")
       do_work("d")
    
    return {"status": "ok",
            "message": "Hello World"}

def do_work(str:input):
    span_name="do_work" 
    with tracer.start_as_current_span(span_name) as span:
        number=random.randint(0,10)
        span.add_event("Did it!")
        span.set_attribute("number", number)
        #span.set_tag("number", number)
        print(f"Sleeping for {number} seconds")
        time.sleep(number)

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths

import segment_main

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()
app.include_router(segment_main.router)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP,log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):    
    logger.info(event)
    return app.resolve(event, context)
    
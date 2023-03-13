import json
import logging
import os

log_level = str(os.environ.get('LOG_LEVEL')).upper()
if log_level not in [
          'DEBUG', 'INFO',
          'WARNING', 'ERROR',
          'CRITICAL'
          ]:
    log_level = 'DEBUG'



def lambda_handler(event, context):    
    logging.info('Received Event:%s',json.dumps(event))
    logging.info('RouteKey:%s',event['routeKey'])
    path = event['routeKey']
    
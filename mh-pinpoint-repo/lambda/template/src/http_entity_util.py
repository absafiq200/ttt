import uuid,json
from dateutil import tz
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()

@tracer.capture_method
def getTemplateRequestItem(body,template_resource_id):
    logger.info('getTemplateRequestItem')   
    req = ''
    try:
        return {
                'template_id': str(uuid.uuid4()) if 'template_id' not in body else body['template_id'].strip(),
                'template_name': body['template_name'].strip(),
                'template_channel': body['template_channel'].strip(),
                'template_default_attributes': body['template_default_attributes'] if 'template_default_attributes' in body else '',
                'template_language': body['template_language'].strip(),
                'template_email': body['template_email'] if 'template_email' in body else '',
                'template_sms': body['template_sms'] if 'template_sms' in body else '',
                'template_resource_id': template_resource_id,
                'template_lastupdated': datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
            }
            
    except Exception as er:
        logger.error(er)
        print(er)
        

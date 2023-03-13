import json
from http_util import response_hdr
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


@tracer.capture_method
def validateTemplateKey(event):
    logger.info('validateTemplateKey')
    errMsg = ''
    if 'template_name' not in event:
        errMsg = "Template name,"
    elif len(event['template_name'])<1:
        errMsg = "Template name,"
    
    if 'template_language' not in event:
        errMsg = errMsg + 'template language,'
    elif len(event['template_language'].strip())<1:
        errMsg = errMsg + 'template language,'    
    
    if 'template_channel' not in event:
        errMsg = errMsg + 'template channel,'  
    elif len(event['template_channel'].strip())<1:
         errMsg = errMsg + 'template channel,'   
    elif event['template_channel'].strip().upper() not in ('SMS','EMAIL'):
        errMsg  = errMsg + "template channel should be 'SMS|EMAIL,"  
    else:
        if event['template_channel'].strip().upper() == 'SMS':
            if 'template_sms' not in event:
                errMsg = errMsg + 'sms template,'
            elif len(event['template_sms'].strip())<1:   
                errMsg = errMsg + 'sms template,'
        else:
            if 'template_email' not in event:
                errMsg = errMsg + 'email template,'
            elif len(event['template_email'])<1:   
                errMsg = errMsg + 'email template,'
            else:
                if 'subject' not in event['template_email']:
                    errMsg = errMsg + 'subject,'
                if 'html' not in event['template_email'] and 'plaintext' not in event['template_email']:
                    errMsg = errMsg + 'html part/plain text,'   

    
    if errMsg:        
        errMsg = "Invalid Request Body - Missing " + errMsg[:len(errMsg)-1]
        logger.debug({'Error Msg':errMsg})
    return errMsg

@tracer.capture_method
def validateUpdateTemplateKey(event):
    logger.info('validateUpdateTemplateKey')
    errMsg = validateTemplateKey(event)
    if 'template_id' not in event:
        errMsg = errMsg +  "Template id," if errMsg else "Template id missing,"
    
    return errMsg

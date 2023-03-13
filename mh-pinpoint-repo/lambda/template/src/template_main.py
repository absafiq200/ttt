from pinpoint_sms_util import create_sms_template_pp,update_sms_template_pp,delete_sms_template_pp
from pinpoint_email_util import create_email_template_pp,update_email_template_pp,delete_email_template_pp
from validation_util import validateTemplateKey,validateUpdateTemplateKey
from http_entity_util import getTemplateRequestItem
from http_util import response_hdr
from dynamodb_util import create_dyno_item,getTemplatedb,delete_templatedb,getAllTemplatesdb
import json,os
from cust_date_util import getCurrentDateTime
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.event_handler import (Response,content_types)

tracer = Tracer()
logger = Logger()
router = APIGatewayHttpRouter()

@router.post("/template/<type>/create")
@tracer.capture_method   
def create_template(type):
    logger.info({'type':type })
    error_400=''
    error_500=''
    try:
        template = router.current_event.json_body
        if type.lower() not in  ('sms','email'):
            error_400 = "Bad request - missing valid type"
        else:    
            rtn = validateTemplateKey(template)   
            print('c1')
            if not rtn:
                if type.lower() == "sms":
                    tmplResponse =  create_sms_template_pp(template)
                else:
                    print(template)
                    tmplResponse =  create_email_template_pp(template)    
                print('c2')
                if not tmplResponse[0]:
                    print('c3')
                    error_400 = tmplResponse[1]
                else:
                    print('c4')
                    reqdb = getTemplateRequestItem(template,tmplResponse[0])
                    print('c5')
                    if reqdb:
                        resp = create_dyno_item(os.environ.get('CAMPAIGN_TEMPLATE'),reqdb)
                        print('c6')
                        if resp:
                            return Response(
                                        status_code = 201,
                                        body = json.dumps(resp),
                                        headers = response_hdr,
                                        content_type = content_types.APPLICATION_JSON 
                                    )
                        else:
                            error_500 = "Unable to store template information in table"
                    else:
                        error_500 = "Unable to store template information in table."
            else:
                error_400 = "Bad Request-" + rtn
            
    except Exception as er:
        print(er)
        logger.error(er)
        error_500 = "Internal Error"
        
    return Response(
                status_code = 400 if error_400 else 500,
                body = json.dumps({
                        "error": error_400 if error_400 else error_500 
                }),
                headers = response_hdr,
                content_type = content_types.APPLICATION_JSON 
            )

    

@router.put("/template/<type>/update")
@tracer.capture_method   
def update_template(type):
    logger.info({'type':type })
    error_400=''
    error_500=''
    proj="template_id,template_resource_id,template_name,template_language,template_lastupdated,template_email,template_sms,template_channel,template_default_attributes"
    try:
        template = router.current_event.json_body
        print('u1')
        if type.lower() not in  ('sms','email'):
            error_400 = "Bad request - missing valid type"
        else:
            print('u2')
            rtn = validateUpdateTemplateKey(template)   
            print('u3')
            
            if not rtn:
                resp = getTemplatedb(os.environ.get('CAMPAIGN_TEMPLATE'),template['template_id'],proj)
                print(resp)
                print('d2')
                if not resp:
                    error_400 = " Bad Request - unable to find template"
                else:
                    if type.lower() =="sms":
                        tmplResponse =  update_sms_template_pp(template)
                    else:
                        tmplResponse =  update_email_template_pp(template)

                    if tmplResponse:
                        print('u4')
                        error_400 = tmplResponse
                    else:
                        print('u5')
                        reqdb = getTemplateRequestItem(template,resp['template_resource_id'])
                        print('u6')
                        if reqdb:
                            resp = create_dyno_item(os.environ.get('CAMPAIGN_TEMPLATE'),reqdb)
                            print('u7')
                            if resp:
                                return Response(
                                            status_code = 200,
                                            body = json.dumps(resp),
                                            headers = response_hdr,
                                            content_type = content_types.APPLICATION_JSON 
                                        )
                            else:
                                error_500 = "Unable to update template information in table"
                        else:
                            error_500 = "Unable to update template information in table."
            else:
                error_400 = "Bad Request-" + rtn
                
    except Exception as er:
        print(er)
        logger.error(er)
        error_500 = "Internal Error"
            
    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )

    
   
 
@router.delete("/template/<type>/delete")
@tracer.capture_method
def delete_template(type):
    bdy = router.current_event.json_body
    error_500=''
    error_400=''
    proj="template_id,template_resource_id,template_name,template_language,template_lastupdated,template_email,template_sms,template_channel,template_default_attributes"
    if 'template_id' not in bdy:        
        error_400 = "Bad Request - missing template id"            
    else:
        if type.lower() not in ('sms','email'):
            error_400 = "Bad request - missing valid type"
        else:
            try:
                print('d1')
                resp = getTemplatedb(os.environ.get('CAMPAIGN_TEMPLATE'),bdy['template_id'],proj)
                print('d2')
                
                if not resp:
                    error_400 = " Bad Request - unable to find template"
                else:
                    print('d3')
                    if type.lower() == "sms":
                        tmplResponse = delete_sms_template_pp(resp['template_name'])
                    else:
                        tmplResponse = delete_email_template_pp(resp['template_name'])    
                    print('d4')
                    if tmplResponse:
                        print('d5')
                        error_400 = tmplResponse
                    else:
                        
                        print('d6')
                        resp = delete_templatedb(os.environ.get('CAMPAIGN_TEMPLATE'),resp['template_id'])
                        print('d7')    
                        if resp:
                            return Response(
                                        status_code = 200,
                                        body = json.dumps({
                                                "template_id": bdy['template_id'],
                                                "template_deletedate" :getCurrentDateTime()
                                            }),
                                        headers = response_hdr,
                                        content_type = content_types.APPLICATION_JSON 
                                    )
                        else:
                            error_500 = "Unable to delete template information in table"
                        
                        
            except Exception as er:
                logger.error(er)
                error_500 = "Internal Error"        

            return Response(
                            status_code = 400 if error_400 else 500,
                            body = json.dumps({
                                    "error": error_400 if error_400 else error_500 
                            }),
                            headers = response_hdr,
                            content_type = content_types.APPLICATION_JSON 
                        )              
  
    
    
@router.get("/template/<type>/get")
@tracer.capture_method
def get_template(type):
    bdy = router.current_event.json_body
    error_400 = ''
    error_500 = ''
    proj="template_id,template_name,template_language,template_lastupdated,template_email,template_sms,template_channel,template_default_attributes"
    if 'template_id' not in bdy:        
        error_400 = "Bad Request - missing template id"            
    else:
        if type.lower() not in ('sms','email'):
            error_400 = " Bad Request - unable to find template"
        else:    
            print('g1')
            resp = getTemplatedb(os.environ.get('CAMPAIGN_TEMPLATE'),bdy['template_id'],proj)
            print('g2')
            return Response(
                            status_code = 200,
                            body = json.dumps(resp),
                            headers = response_hdr,
                            content_type = content_types.APPLICATION_JSON 
                        )
    
@router.get("/template/list_templates")
@tracer.capture_method
def listTemplates():
    return Response(
                    status_code = 200,
                    body = json.dumps(getAllTemplatesdb(os.environ.get('CAMPAIGN_TEMPLATE'))),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )

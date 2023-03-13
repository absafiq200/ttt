import boto3
from boto3.dynamodb.conditions import Key, Attr
from dateutil import tz
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()
dyn_resource = boto3.resource("dynamodb")


@tracer.capture_method
def create_dyno_item(table_name,item):
    logger.debug({'create_dyno_item->item->>':str(item)})
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.put_item(Item = item)
        logger.debug('create template create_dyno_item->'+str(resp))
        print 
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                    "template_id": item['template_id'],
                    "template_lastupdated": item["template_lastupdated"]
                 }          

    except Exception as er:
        logger.error({'create_dyno_item':er})
    return ''

@tracer.capture_method
def getTemplatedb(table_name,templateid,proj):
    logger.debug({'getTemplatedb->template ID-->':templateid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('template_id').eq(templateid),
                   ProjectionExpression=proj
                )        
        logger.debug({'getTemplatedb response->':str(resp)})         
        if resp['Items']: 
            return resp['Items'][0]
            
    except Exception as er:
        logger.error(er)
    return ''

@tracer.capture_method
def delete_templatedb(table_name,templateid):
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.delete_item(Key={
                        'template_id': templateid
                    })
        if 'ResponseMetadata' in resp:
            return True                        
    except Exception as er:
        logger.error(er)          
    return False          

@tracer.capture_method
def getAllTemplatesdb(table_name):
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp =  dyn_tbl.scan(
            ProjectionExpression="template_id,template_name,template_language,template_lastupdated,template_email,template_sms,template_channel,template_default_attributes"
            )
                 
        logger.debug({'getAllTemplatesdb response->':str(resp)})  
        data = resp['Items']
        while 'LastEvaluatedKey' in resp:
            resp = dyn_tbl.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
            data.extend(resp['Items'])
        
        return data
    except Exception as er:
        logger.error(er)
    return ''
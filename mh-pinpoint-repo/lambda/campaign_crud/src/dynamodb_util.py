import boto3
from boto3.dynamodb.conditions import Key, Attr
from dateutil import tz
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()
dyn_resource = boto3.resource("dynamodb")

class campaign_cls:
    def __init__(self,pinpointprojid, camp_name,camp_msg_type,camp_orig_num,camp_email,camp_status,lstRunId):
        self.pinpointprojid = pinpointprojid
        self.camp_name=camp_name
        self.camp_msg_type = camp_msg_type
        self.camp_orig_num=camp_orig_num
        self.camp_email = camp_email
        self.camp_status = camp_status
        self.lstRunId = lstRunId


@tracer.capture_method
def create_dyno_item(table_name,item):
    logger.debug({'create_dyno_item->item->>':str(item)})
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.put_item(Item = item)
        logger.debug('create campaign create_dyno_item->'+str(resp))
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                    "campaign_id": item['campaign_id'],
                    "campaign_name": item["campaign_name"],
                    "campaign_lastupdated": item["campaign_lastupdated"]
                 }          

    except Exception as er:
        logger.error(er)
        
        
@tracer.capture_method
def update_campaigndb(table_name,req):
    print(type(req))
    logger.debug({'update_campaignstatusdb->request->>':str(req) })
    
    dyn_tbl = dyn_resource.Table(table_name)
    lastupdate = datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
    try:
        resp = dyn_tbl.update_item(
                        Key = {
                        'campaign_id': req['campaign_id']
                    },
                    UpdateExpression = "set campaign_quiettimes = :camprun,campaign_channel = :channel, campaign_origination_num = :phone,campaign_msg_type = :msg_type,campaign_email_address = :email_addr, campaign_lastupdated = :updatedate",
                    ExpressionAttributeValues = {
                        ':camprun' : req['campaign_quiettimes'],                        
                        ':channel' : req['campaign_channel'],
                        ':phone' : req['campaign_origination_num'],
                        ':msg_type' : req['campaign_msg_type'], 
                        ':email_addr' : req['campaign_email_address'],
                        ':updatedate' : lastupdate

                    }
                )    
        logger.debug({'update_campaignstatusdb response->':str(resp)})       
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:    
            return {
                        "campaign_id": req['campaign_id'],
                        "campaign_name": req["campaign_name"],
                        "campaign_lastupdated": req["campaign_lastupdated"]
                    }  
    except Exception as er:
        logger.error(er)        


@tracer.capture_method
def update_campaignstatusdb(table_name,campid,request,campStatus,campRunid,cnt):
    logger.debug({'update_campaignstatusdb->campid->>':str(campid) , 'campStatus->' : campStatus })
    print(type(request))
    dyn_tbl = dyn_resource.Table(table_name)
    lastupdate = datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
    try:
        if cnt:
            resp = dyn_tbl.update_item(
                        Key = {
                        'campaign_id': campid
                    },
                    UpdateExpression = "set campaign_runs = :camprun,campaign_lastupdated = :updatedate,campaign_status = :campstatus",
                    ExpressionAttributeValues = {
                        ':camprun' : request,
                        ':updatedate' : lastupdate,
                        ':campstatus' : campStatus
                    }
                )    
        else:
            resp = dyn_tbl.update_item(
                        Key = {
                        'campaign_id': campid
                    },
                    UpdateExpression = "set campaign_runs = if_not_exists(campaign_runs, :camprun),campaign_lastupdated = :updatedate,campaign_status = :campstatus",
                    ExpressionAttributeValues = {
                        ':camprun' : request,
                        ':updatedate' : lastupdate,
                        ':campstatus' : campStatus
                    }
                )    
        logger.debug({'update_campaignstatusdb response->':str(resp)})           
        return {
                 "campaign_run_id": campRunid,
                 "campaign_lastupdated": lastupdate
               }
    except Exception as er:
        logger.error(er)

@tracer.capture_method
def update_campaignLastUpdatedb(table_name,campid,campstatus):
    logger.debug({'update_campaignLastUpdatedb->campid->>':campid })
    
    dyn_tbl = dyn_resource.Table(table_name)
    lastupdate = datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
    try:
        
        resp = dyn_tbl.update_item(
                    Key = {
                    'campaign_id': campid
                },
                UpdateExpression = "set campaign_lastupdated = :updatedate,campaign_status = :campstatus",
                ExpressionAttributeValues = {                    
                    ':updatedate' : lastupdate,
                    ':campstatus' : campstatus
                }
            )    
        
        logger.debug({'update_campaignstatusdb response->':str(resp)})           
        return lastupdate
    except Exception as er:
        logger.error(er)



@tracer.capture_method
def delete_campaignRundb(table_name,campid,campRunid,request):
    logger.debug({'update_campaignstatusdb->campid->>':str(campid) })
    print(type(request))
    dyn_tbl = dyn_resource.Table(table_name)
    lastupdate = datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
    try:
        if request:
            resp = dyn_tbl.update_item(
                        Key = {
                        'campaign_id': campid
                    },
                    UpdateExpression = "set campaign_runs = :camprun,campaign_lastupdated = :updatedate",
                    ExpressionAttributeValues = {
                        ':camprun' : request,
                        ':updatedate' : lastupdate                        
                    }
                )
        else:
            resp = dyn_tbl.update_item(
                    Key = {
                    'campaign_id': campid
                },
                UpdateExpression = "remove campaign_runs"                
            )    
            resp = dyn_tbl.update_item(
                        Key = {
                        'campaign_id': campid
                    },
                    UpdateExpression = "set campaign_lastupdated = :updatedate",
                    ExpressionAttributeValues = {                        
                        ':updatedate' : lastupdate                        
                    }
                )       
        
        logger.debug({'update_campaignstatusdb response->':str(resp)})           
        return {
                 "campaign_run_id": campRunid,
                 "campaign_run_deletedate": lastupdate
               }
    except Exception as er:
        logger.error(er)

    
@tracer.capture_method
def check_campaign_exist(table_name,campName):
    logger.debug({'check_campaign_exist->campName-->':campName})   
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.scan(
                        FilterExpression="campaign_name=:cmp",                        
                        ExpressionAttributeValues={
                            ':cmp': campName
                        },
                        ProjectionExpression="campaign_id"
                )
        logger.debug({'check_campaign_exist response->':str(resp)})          
        if resp['Items']:
            logger.info('Campaign already exist')
            return True
    except Exception as er:
        logger.error(er)
    return False   

@tracer.capture_method
def getCampaigndb(table_name,campid):
    logger.debug({'getCampaign->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'check_campaign_exist response->':str(resp)})         
        if resp['Items']: 
            itm = resp['Items'][0]
            lstRunId = []
            print(itm)
            if 'campaign_runs' in itm:               
                for cr in itm['campaign_runs']:
                    print(cr)                   
                    lstRunId.append(cr['campaign_run_id'])
            return campaign_cls(itm['pinpointprojectid'],itm['campaign_name'],itm['campaign_msg_type'],itm['campaign_origination_num'],itm['campaign_email_address'],itm['campaign_status'],lstRunId)
    except Exception as er:
        logger.error(er)

@tracer.capture_method
def getCampaignRundb(table_name,campid,run_id):
    logger.debug({'getCampaignRundb->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'getCampaignRundb response->':str(resp)})         
        if resp['Items']: 
            campRun = False
            itm = resp['Items'][0]            
            if 'campaign_runs' in itm:
                for cr in itm['campaign_runs']: 
                    print('cr')
                    print(cr)
                    if cr['campaign_run_id'] == run_id:
                        campRun = True
                        print('run id exist')
                        break; 
                    
            return campaign_cls(itm['pinpointprojectid'],itm['campaign_name'],itm['campaign_msg_type'],itm['campaign_origination_num'],itm['campaign_email_address'],itm['campaign_status'],campRun)
    except Exception as er:
        logger.error(er)

@tracer.capture_method
def getCampRunOnlydb(table_name,campid,run_id):
    logger.debug({'getCampRunDatadb->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'getCampRunDatadb response->':str(resp)})         
        if resp['Items']: 
            campRun = ''
            itm = resp['Items'][0]            
            if 'campaign_runs' in itm:
                for cr in itm['campaign_runs']:                    
                    if cr['campaign_run_id'] == run_id:
                        campRun = cr                        
                        break; 
                    
            return campRun 
    except Exception as er:
        logger.error(er)


@tracer.capture_method
def getAllCampaignsdb(table_name):
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp =  dyn_tbl.scan(
            ProjectionExpression="campaign_id,campaign_name,campaign_starttime,campaign_endtime,campaign_status,pinpointprojectid,campaign_channel,campaign_origination_num,campaign_msg_type,campaign_email_address,campaign_lastupdated"
        )        
        logger.debug({'getAllCampaign response->':str(resp)})  
        data = resp['Items']
        while 'LastEvaluatedKey' in resp:
            resp = dyn_tbl.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
            data.extend(resp['Items'])
        
        return data
    except Exception as er:
        logger.error(er)
        

@tracer.capture_method
def delete_campaigndb(table_name,campid):
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.delete_item(Key={
                        'campaign_id': campid
                    })
        if 'ResponseMetadata' in resp:
            return True                        
    except Exception as er:
        logger.error(er)                

@tracer.capture_method
def getCampdb(table_name,campid):
    logger.debug({'getCampaign->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'check_campaign_exist response->':str(resp)})         
        if resp['Items']:
            return resp['Items'][0]
        
    except Exception as er:
        logger.error(er)
           
    
def getCampaignRuns(table_name,campid,run_id,campReq):
    logger.debug({'getCampaignRuns->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'check_campaign_exist response->':str(resp)})         
        if resp['Items']:
            itm = resp['Items'][0]       
            print('aaa')
            if 'campaign_runs' in itm:
                print('bbb')
                print(run_id)
                if run_id:
                    print('ccc')
                    for index,cr in enumerate(itm['campaign_runs']): 
                        print(cr['campaign_run_id'])
                        if cr['campaign_run_id'] == run_id:
                            itm['campaign_runs'][index] =  campReq
                            print('set')
                            break; 
                    return itm['campaign_runs']            
                else:
                    print('dd')
                    
                    print(itm['campaign_runs'])
                    print(type(itm['campaign_runs']))
                    return itm['campaign_runs']

    except Exception as er:
        logger.error(er)

def getCampaignRunsExcept(table_name,campid,run_id):
    logger.debug({'getCampaignRuns->campid-->':campid})   
    
    dyn_tbl = dyn_resource.Table(table_name)
    try:
        resp = dyn_tbl.query(
                   KeyConditionExpression=Key('campaign_id').eq(campid)
                )        
        logger.debug({'check_campaign_exist response->':str(resp)})         
        if resp['Items']:
            itm = resp['Items'][0]                   
            if 'campaign_runs' in itm:                
                if run_id:
                    print('ccc')
                    for index,cr in enumerate(itm['campaign_runs']): 
                        print(cr['campaign_run_id'])
                        if cr['campaign_run_id'] == run_id:
                            itm['campaign_runs'].pop(index) 
                            print('set')
                            break; 
                    return itm['campaign_runs']            
                

    except Exception as er:
        logger.error(er)

from cust_date_util import (isGreaterThanToday,isEndGreatherThanStart)
from datetime import datetime

from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()
locale = ["AR-AR","CMN-CN","EN-US","ES-ES","ES-US","FR-FR","HT-HT","IT-IT","KM-KM","KO-KO","LO-LO","PT-PT","RU-RU","VI-VI","ZH-YUE"] 
     
        
@tracer.capture_method
def validateCampaignKey(event):
    logger.info('validateCampaignKey')
    errMsg = ''
    if 'campaign_name' not in event:
        errMsg = "campaign name,"
    elif len(event['campaign_name'])<1:
        errMsg = "campaign name,"

    if 'campaign_starttime' not in event:
        errMsg = errMsg + 'campaign starttime,'
    elif len(event['campaign_starttime'].strip())<1:
        errMsg = errMsg + 'campaign starttime,'
    elif len(event['campaign_starttime'].strip())>0:
        if not isGreaterThanToday(event['campaign_starttime'].strip()):
            errMsg = errMsg + 'invalid campaign starttime,'

    if 'campaign_endtime' not in event:
        errMsg = errMsg + 'campaign endtime,'
    elif len(event['campaign_endtime'].strip())<1:
        errMsg = errMsg + 'campaign endtime,'    
    elif len(event['campaign_endtime'].strip())>0:
        if not isGreaterThanToday(event['campaign_endtime'].strip()):
            errMsg = errMsg + 'invalid campaign endtime,'
    
    if 'campaign_starttime' in event and 'campaign_endtime' in event and len(event['campaign_starttime'].strip())>0 and len(event['campaign_endtime'].strip())>0:
        if not isEndGreatherThanStart(event['campaign_starttime'].strip(),event['campaign_endtime'].strip()):
            errMsg = errMsg + 'invalid start/end date,'
    
    if 'campaign_status' not in event:
        errMsg = errMsg + 'campaign status,'
    elif  len(event['campaign_status'].strip())<1:
        errMsg = errMsg + 'campaign status,'
    
    if 'pinpointprojectid' not in event:
        errMsg = errMsg + 'pinpoint application id,'
    elif len(event['pinpointprojectid'].strip())<1:
        errMsg = errMsg + 'pinpoint application id,'    

    if 'campaign_quiettimes' not in event:
        errMsg = errMsg + 'campaign quiettimes,'
    elif len(event['campaign_quiettimes'])<1:
        errMsg = errMsg + 'campaign quiettimes,'       
    
    if 'campaign_origination_num' not in event:
        errMsg = errMsg + 'campaign origination number,'
    elif len(event['campaign_origination_num'].strip())<1:
        errMsg = errMsg + 'campaign origination number,'
    
    if 'campaign_msg_type' not in event:
        errMsg = errMsg + 'campaign message type,'
    elif len(event['campaign_msg_type'].strip())<1:
        errMsg = errMsg + 'campaign message type,'    
    
    if 'campaign_email_address' not in event:
        errMsg = errMsg + 'campaign email address,'
    elif len(event['campaign_email_address'].strip())<1:
        errMsg = errMsg + 'campaign email address,'
    
    if 'campaign_channel' not in event:
        errMsg = errMsg + 'campaign channel,'  
    elif len(event['campaign_channel'].strip())<1:
         errMsg = errMsg + 'campaign channel,'   
    elif event['campaign_channel'].strip().upper() not in ('SMS','EMAIL'):
        errMsg  = errMsg + "Campaign channel should be 'SMS|EMAIL|BOTH,"  
    else:
        if event['campaign_channel'].strip().upper() == 'SMS':
            if 'sms_template' not in event:
                errMsg = errMsg + 'sms template,'
            elif len(event['sms_template'].strip())<1:   
                errMsg = errMsg + 'sms template,'
        else:
            if 'email_template' not in event:
                errMsg = errMsg + 'email template,'
            elif len(event['email_template'].strip())<1:   
                errMsg = errMsg + 'email template,'
    
    if errMsg:        
        errMsg = "Invalid Request Body - Missing " + errMsg[:len(errMsg)-1]
        logger.debug({'Error Msg':errMsg})
    return errMsg
        
    

@tracer.capture_method
def validateRunCampaignKey(event):
    logger.info('validateRunCampaignKey')
    errMsg = ''
    if 'campaign_id' not in event:
        errMsg = "campaign id,"
    elif len(event['campaign_id'])<1:
        errMsg = "campaign id,"

    if 'campaign_starttime' not in event:
        errMsg = errMsg + 'campaign starttime,'
    elif len(event['campaign_starttime'].strip())<1:
        errMsg = errMsg + 'campaign starttime,'
    elif len(event['campaign_starttime'].strip())>0:
        if not isGreaterThanToday(event['campaign_starttime'].strip()):
            errMsg = errMsg + 'invalid campaign starttime,'

    if 'campaign_endtime' not in event:
        errMsg = errMsg + 'campaign endtime,'
    elif len(event['campaign_endtime'].strip())<1:
        errMsg = errMsg + 'campaign endtime,'    
    elif len(event['campaign_endtime'].strip())>0:
        if not isGreaterThanToday(event['campaign_endtime'].strip()):
            errMsg = errMsg + 'invalid campaign endtime,'
    
    if 'campaign_starttime' in event and 'campaign_endtime' in event and len(event['campaign_starttime'].strip())>0 and len(event['campaign_endtime'].strip())>0:
        if not isEndGreatherThanStart(event['campaign_starttime'].strip(),event['campaign_endtime'].strip()):
            errMsg = errMsg + 'invalid start/end date,,'

    if 'segment_id' not in event:
        errMsg = errMsg + 'segment id,'
    elif  len(event['segment_id'].strip())<1:
        errMsg = errMsg + 'segment id,'

    if 'campaign_channel' not in event:
        errMsg = errMsg + 'campaign channel,'  
    elif len(event['campaign_channel'].strip())<1:
         errMsg = errMsg + 'campaign channel,'   
    elif event['campaign_channel'].strip().upper() not in ('SMS','EMAIL'):
        errMsg  = errMsg + "Campaign channel should be 'SMS|EMAIL,"  
    
    if errMsg:
        errMsg = "Invalid Request Body - Missing " + errMsg[:len(errMsg)-1]
    return errMsg  

@tracer.capture_method
def validateRunCampaignKeyW(event):
    logger.info('validateRunCampaignKeyW')
    errMsg = validateRunCampaignKey(event)
    if 'campaign_run_id' not in event:
        errMsg = errMsg +  "campaign run id," if errMsg else "campaign run id missing,"
    
    return errMsg    


@tracer.capture_method
def getCampName(campname,segmentname):    
    ab = list([i for i in locale if i.replace("-","_") in segmentname.upper()])
    if ab:
        return campname + "_" + datetime.now().strftime("%Y%m%d%H%M") + "_" + ab[0]
               
import uuid
from dateutil import tz
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()

@tracer.capture_method
def getCampaignRequestItem(body):
    logger.info('getCampaignRequestItem')   
    return {
            'campaign_id': str(uuid.uuid4()) if 'campaign_id' not in body else body['campaign_id'].strip(),
            'campaign_name': body['campaign_name'].strip(),
            'campaign_starttime': body['campaign_starttime'].strip(),
            'campaign_endtime': body['campaign_endtime'].strip(),
            'campaign_status': body['campaign_status'].strip(),
            'pinpointprojectid': body['pinpointprojectid'].strip(),
            'campaign_quiettimes': body['campaign_quiettimes'],
            'campaign_channel': body['campaign_channel'].strip(),
            'campaign_origination_num': "+1" + str(body['campaign_origination_num'])  if len(body['campaign_origination_num'])==10 else "1" + str(body['campaign_origination_num']) if len(body['campaign_origination_num'])==11 else body['campaign_origination_num'] ,
            'campaign_msg_type': body['campaign_msg_type'].strip(),
            'campaign_email_address': body['campaign_email_address'].strip(),
            'campaign_lastupdated': datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')
        }


@tracer.capture_method
def getCampaignRunRequest(body,run_id,cmpRunName,camptype):
    logger.info('getCampaignRequestItem')   
    return {
            'campaign_run_id': run_id,
            'pinpoint_campaign_id': body['campaign_id'].strip(),
            'campaign_run_name': cmpRunName,
            'campaign_starttime': body['campaign_starttime'].strip(),
            'campaign_endtime': body['campaign_endtime'].strip(),
            'campaign_type': camptype,
            'campaign_quiettimes': {
                'Start': body['campaign_quiettimes']["0"][0]["start"],
                'End': body['campaign_quiettimes']["1"][0]["end"]
            },
            'segment_id': body['segment_id'],
            'email_template': body['email_template'].strip() if 'email_template' in body else None,
            'sms_template': body['sms_template'].strip() if 'sms_template' in body else None
        }


@tracer.capture_method    
def getCreateCampaignRequest(campname,body,campCls):
    logger.info('getCreateCampaignRequest')
    try:
        tmplConfig = ''
        msgConfig =''
        startDateTime = datetime.strptime(body['campaign_starttime'].strip(), "%Y%m%dT%H:%M%z").replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        endDateTime = datetime.strptime(body['campaign_endtime'].strip(), "%Y%m%dT%H:%M%z").replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        campQuiet = ''
        if 'campaign_quiettimes' in body:
            campQuiet = {
                            'End': body['campaign_quiettimes']['0'][0]["start"],
                            'Start': body['campaign_quiettimes']["0"][1]['end']
                        }
        if body['campaign_channel'].upper() == "SMS":
            tmplConfig = {
                'SMSTemplate': {
                    'Name':body['sms_template']
                }
            }

            msgConfig = {
                'SMSMessage' : {
                    'MessageType' : campCls.camp_msg_type,
                    'OriginationNumber': "+1" + str(campCls.camp_orig_num)  if len(campCls.camp_orig_num)==10 else "1" + str(campCls.camp_orig_num) if len(campCls.camp_orig_num)==11 else campCls.camp_orig_num ,
                    'SenderId': 'MASSHEALTH'
                }
            }
        else:
            tmplConfig = {
                'EmailTemplate': {
                    'Name':body['email_template']
                }
            }    
            msgConfig = {
                'EmailMessage': {
                    'FromAddress': campCls.camp_email
                }
            }

        return {
                'Name':campname,
                'Description':campname,
                'SegmentId':body['segment_id'].strip(),
                'TemplateConfiguration': tmplConfig,
                'Schedule': {
                    'EndTime':endDateTime,
                    'Frequency':'DAILY',
                    'IsLocalTime': True,
                    'QuietTime': campQuiet if campQuiet else { },
                    'StartTime': startDateTime,
                    'Timezone': 'UTC-05'                
                },
                'MessageConfiguration': msgConfig
            }
    except Exception as er:
        logger.error(er)

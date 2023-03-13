import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()

pinpoint = boto3.client("pinpoint")

@tracer.capture_method
def checkPinpointidExist(project_id):   
    logger.debug({'checkPinpointidExist->project id:':project_id}) 
    try:
        rtn = pinpoint.get_app(ApplicationId =project_id)  
        logger.debug({'checkPinpointidExist->':str(rtn)})      
        if 'ApplicationResponse' in rtn and 'Arn' in rtn['ApplicationResponse']:            
            return True
    except Exception as er:
        logger.error({'checkPinpointidExist->':str(er)})
    return False    
        
@tracer.capture_method    
def getSegmentName(project_id,segment_id):
    logger.debug({'getSegmentName ->Segment ID->':segment_id , 'project Id->' : project_id})    
    try:        
        rtn = pinpoint.get_segment(ApplicationId=project_id.strip(),SegmentId=segment_id.strip())
        logger.debug({'getSegmentName->':str(rtn)})
        if 'SegmentResponse' in rtn and 'Arn' in rtn['SegmentResponse']:
            return rtn['SegmentResponse']['Name']
    except Exception as er:
        logger.error({'getSegmentName exception->':str(er)})
        

@tracer.capture_method
def getSMSTemplate(templateName):
    logger.debug({'getSMSTemplate->templateName:':templateName}) 
    try:
        rtn = pinpoint.get_sms_template(
                    TemplateName=templateName.strip()
        )
        logger.debug({'getSMSTemplate->':str(rtn)})     
        if 'SMSTemplateResponse' in rtn and 'Arn' in rtn['SMSTemplateResponse']:
            return rtn['SMSTemplateResponse']['Arn']
    except Exception as er:
        logger.debug({'getSMSTemplate->':str(er)})
        
@tracer.capture_method
def getEmailTemplate(templateName):
    logger.debug({'getEmailTemplate->templateName:':templateName}) 
    try:
        rtn = pinpoint.get_email_template(
                    TemplateName=templateName )
        logger.debug({'getEmailTemplate->':str(rtn)})            
        if 'EmailTemplateResponse' in rtn and 'Arn' in rtn['EmailTemplateResponse']:            
            return rtn['EmailTemplateResponse']['Arn']
    except Exception as er:
        logger.debug({'getEmailTemplate->':str(er)})
       

@tracer.capture_method
def createCampaign(camp,pinpointid):
    logger.debug({'createCampaign->pinpointid:': pinpointid , 'camp->' : str(camp)}) 
    try:        
        rtn = pinpoint.create_campaign(
                    ApplicationId = pinpointid,
                    WriteCampaignRequest=camp
                )
            
        logger.debug({'createCampaign->':str(rtn)})      
        if 'CampaignResponse' in rtn:
            return {
                    'Run_id': rtn['CampaignResponse']['Id'],
                    'State': rtn['CampaignResponse']['State']['CampaignStatus']
            }
    except Exception as er:        
        logger.error({'unable to create campaign->':str(er)})

@tracer.capture_method
def updateCampaignpp(camp,pinpointid,campid):
    logger.debug({'createCampaign->pinpointid:': pinpointid , 'camp->' : str(camp)}) 
    print(campid)
    print('camp id')
    try:        
        rtn = pinpoint.update_campaign(
                    ApplicationId = pinpointid,
                    CampaignId = campid,
                    WriteCampaignRequest=camp
                )
            
        logger.debug({'createCampaign->':str(rtn)})      
        if 'CampaignResponse' in rtn:
            return {
                    'Run_id': rtn['CampaignResponse']['Id'],
                    'State': rtn['CampaignResponse']['State']['CampaignStatus']
            }
    except Exception as er:        
        logger.error({'unable to update campaign->':str(er)})


@tracer.capture_method
def getCampaignStatus(pinpointid,campid):
    logger.debug({'getCampaignStatus->pinpointid:': pinpointid , 'campid->' : campid}) 
    try:        
        rtn = pinpoint.get_campaign(
                    ApplicationId = pinpointid,
                    CampaignId=campid
                )
            
        logger.debug({'getCampaignStatus->':str(rtn)})      
        if 'CampaignResponse' in rtn:
            rtn['CampaignResponse']['State']['CampaignStatus']
    except Exception as er:        
        logger.error({'getCampaignStatus->':str(er)})
    return ''

@tracer.capture_method
def deleteCampaignpp(pinpointid,campid):
    logger.debug({'deleteCampaignpp->pinpointid:': pinpointid , 'campid->' : campid}) 
    try:        
        rtn = pinpoint.delete_campaign(
                    ApplicationId = pinpointid,
                    CampaignId=campid
                )
            
        logger.debug({'deleteCampaignpp->':str(rtn)})      
        if 'CampaignResponse' in rtn:
            return True
    except Exception as er:        
        logger.error({'deleteCampaignpp->':str(er)})

@tracer.capture_method
def updateCampaignStatuspp(pinpointid,campid,status):
    logger.debug({'updateCampaignStatuspp->pinpointid:': pinpointid , 'campid->' : campid , 'status:': status }) 
    try:
        rtn = pinpoint.update_campaign(
                    ApplicationId = pinpointid,
                    CampaignId = campid,
                    WriteCampaignRequest={
                        "IsPaused": status
                    }
                )
        return rtn['CampaignResponse']['State']['CampaignStatus']        

    except Exception as er:
        logger.error({'updateCampaignStatus->':str(er)})

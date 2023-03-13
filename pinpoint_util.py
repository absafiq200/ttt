import boto3
import json
from http_util import response_hdr
from aws_lambda_powertools import Logger, Tracer

locale = ["AR-AR","CMN-CN","EN-US","ES-ES","ES-US","FR-FR","HT-HT","IT-IT","KM-KM","KO-KO","LO-LO","PT-PT","RU-RU","VI-VI","ZH-YUE"] 

tracer = Tracer()
logger = Logger()
pinpoint = boto3.client("pinpoint")

def getSegmentsPP(pinpointid,segmentGroup,type):
    try:
        
        resp = pinpoint.get_segments(
                                    ApplicationId=pinpointid
                        )
        print(resp)
        rtnData = []
        if 'SegmentsResponse' in resp:
            print('1')
            for itm in resp['SegmentsResponse']['Item']:
                print(itm)
                if 'ImportDefinition' in itm:
                    print('1.1')
                    if type.upper() in itm["ImportDefinition"]["ChannelCounts"] and itm["Name"].lower().startswith(segmentGroup.lower()):
                        print('22')
                        tmp = {
                            "segment_id" : itm["Id"],
                            "segment_name" : itm["Name"],
                            "creation_date" : itm["CreationDate"],
                            "segment_channel" : 'SMS' if 'SMS' in itm["ImportDefinition"]["ChannelCounts"] else 'EMAIL',
                            "channel_count": itm["ImportDefinition"]["ChannelCounts"]['SMS'] if 'SMS' in itm["ImportDefinition"]["ChannelCounts"] else itm["ImportDefinition"]["ChannelCounts"]['EMAIL'],
                            "format" : itm["ImportDefinition"]["Format"],
                            "segment_language" : getLang(itm["Name"]),
                            "segment_group": segmentGroup,
                            "lastmodified_date" : itm["LastModifiedDate"]
                        }
                        rtnData.append(tmp)
            while 'NextToken' in resp['SegmentsResponse']:
                print('4')
                resp = pinpoint.get_segment(
                                    ApplicationId=pinpointid,
                                    Token = resp['SegmentsResponse']['NextToken']
                            )
                for itm in resp['SegmentResponse']['Item']:
                    if 'ImportDefinition' in itm:
                        if type.upper() in itm["ImportDefinition"]["ChannelCounts"] and itm["Name"].lower().startswith(segmentGroup.lower()):
                        
                            tmp = {
                                "segment_id" : itm["Id"],
                                "segment_name" : itm["Name"],
                                "creation_date" : itm["CreationDate"],
                                "segment_channel" : 'SMS' if 'SMS' in itm["ImportDefinition"]["ChannelCounts"] else 'EMAIL',
                                "channel_count": itm["ImportDefinition"]["ChannelCounts"]['SMS'] if 'SMS' in itm["ImportDefinition"]["ChannelCounts"] else itm["ImportDefinition"]["ChannelCounts"]['EMAIL'],
                                "format" : itm["ImportDefinition"]["Format"],
                                "segment_language" : getLang(itm["Name"]),
                                "segment_group": segmentGroup,
                                "lastmodified_date" : itm["LastModifiedDate"]
                            }
                            rtnData.append(tmp)


        return rtnData
    except Exception as er:
        print(er)    

def getLang(segmentName):
    ab = list([i for i in locale if i.replace("-","_") in segmentName.upper()])    
    if ab:
        return ab[0]    
    

def getSegmentIdsPP(pinpointid,segmentGroup):
    try:
        
        resp = pinpoint.get_segments(
                                    ApplicationId=pinpointid
                        )
        print(resp)
        rtnData = []
        if 'SegmentsResponse' in resp:
            print('1')
            for itm in resp['SegmentsResponse']['Item']:
                print(itm)
                if itm["Name"].lower().startswith(segmentGroup.lower()):
                    print('22')
                    rtnData.append(itm["Id"])
                    
            while 'NextToken' in resp['SegmentsResponse']:
                print('4')
                resp = pinpoint.get_segment(
                                    ApplicationId=pinpointid,
                                    Token = resp['SegmentsResponse']['NextToken']
                            )
                for itm in resp['SegmentResponse']['Item']:
                    
                    if type.upper() in itm["ImportDefinition"]["ChannelCounts"] and itm["Name"].lower().startswith(segmentGroup.lower()):
                        rtnData.append(itm["Id"])
                    
        return rtnData
    except Exception as er:
        print(er)    



def deleteSegmentPP(pinpointid,segmentID):
    try:
        
        resp = pinpoint.delete_segment(
                                    ApplicationId=pinpointid,
                                    SegmentId=segmentID
                        )   
        return '' 
    except Exception as er:
        print(er)    
    return 'unable to delete'    

def getCampaigns(pinpointid):
    try:
        resp = pinpoint.get_campaigns(
                    ApplicationId=pinpointid
                )
        #print(resp)
        rtnData = []
        if resp:
            if 'CampaignsResponse' in resp:
                print('1')
                for itm in resp["CampaignsResponse"]["Item"]:
                    print('2')
                    print(itm)
                    tmp = {
                        "segment_id" : itm["SegmentId"],
                        "state" : itm["State"]["CampaignStatus"],
                        "name": itm["Name"],
                        "camp_id": itm["Id"]
                    }
                    rtnData.append(tmp)
                    print('3')
                while 'NextToken' in resp["CampaignsResponse"]["Item"]:
                    print('4')
                    resp = pinpoint.get_campaigns(
                                    ApplicationId=pinpointid,
                                    Token = resp["NextToken"]
                                )
                    for itm in resp["CampaignsResponse"]:
                        tmp = {
                            "segment_id" : itm["SegmentId"],
                            "state" : itm["State"]["CampaignStatus"],
                            "name": itm["Name"],
                            "camp_id": itm["Id"]
                        }
                        rtnData.append(tmp)

        return rtnData
    except Exception as er:
        print(er)       

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
    return False

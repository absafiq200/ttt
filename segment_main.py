import json,os
from cust_date_util import getCurrentDateTime
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.event_handler import (Response,content_types)
from pinpoint_util import getSegmentsPP,deleteSegmentPP,getSegmentIdsPP,getCampaigns,deleteCampaignpp

tracer = Tracer()
logger = Logger()
router = APIGatewayHttpRouter()
from http_util import (response_hdr)


@router.post("/segment/create/status")
@tracer.capture_method   
def getSegmentStatus():
    error_400=''
    error_500=''
    try:
        bdy = router.current_event.json_body
        if 'file_name' not in  bdy:
            error_400 = "segment name does not exist"                
        else:
            segResp = getSegmentIdsPP(bdy["pinpointprojectid"],bdy["file_name"])
            if segResp:
                resp = getCampSegmentStatus(bdy["pinpointprojectid"],segResp)
                if resp:
                    return Response(
                        status_code = 200,
                        body = json.dumps({
                                "status": resp,
                                "message" : "ok" 
                        }),
                        headers = response_hdr,
                        content_type = content_types.APPLICATION_JSON 
                    )                

    except Exception as er:
        print(er)        

    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )          


@router.post("/segment/<type>/get")
@tracer.capture_method   
def getSegment(type):
    error_400=''
    error_500=''
    try:
        bdy = router.current_event.json_body
        if 'pinpointprojectid' not in  bdy:
            error_400 = "pinpoint project id does not exist"                
        elif 'segmentgroup' not in bdy:
            error_400 = "segment group does not exist" 
        elif type.upper()  not in ('SMS','EMAIL'):
            error_400 = "Invalid path parameter should be SMS or Email"
        else:
            segResp = getSegmentsPP(bdy["pinpointprojectid"],bdy["segmentgroup"],type)
            return Response(
                                status_code = 200,
                                body = json.dumps(segResp),
                                headers = response_hdr,
                                content_type = content_types.APPLICATION_JSON 
                            )

    except Exception as er:
        print(er)        

    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )          

@router.delete("/segment/delete")
@tracer.capture_method   
def deleteSegment():
    error_400=''
    error_500=''
    try:
        bdy = router.current_event.json_body
        
        if 'pinpointprojectid' not in  bdy:
            error_400 = "pinpoint project id does not exist"                
        elif 'segment_group'  in bdy:
            segResp = getSegmentIdsPP(bdy["pinpointprojectid"],bdy["segment_group"])
            if segResp:
                err = delCampSegment(bdy["pinpointprojectid"],segResp)
                if er:
                    return Response(
                        status_code = 400,
                        body = json.dumps({
                                "error": err 
                        }),
                        headers = response_hdr,
                        content_type = content_types.APPLICATION_JSON 
                    )
                else:
                    return Response(
                                    status_code = 200,
                                    body = json.dumps({
                                        'segment_group' :    bdy["segment_group"],
                                        'segment_deletedate' : getCurrentDateTime()    
                                    }),
                                    headers = response_hdr,
                                    content_type = content_types.APPLICATION_JSON 
                                ) 
            else:
                error_400 = "Segment Does not exist"    
        elif 'segment_id' in bdy:
            err = delCampSegment(bdy["pinpointprojectid"],list[bdy["segment_id"]])
            if er:
                return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": err 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )
            else:
                return Response(
                                status_code = 200,
                                body = json.dumps({
                                     'segment_id' :    bdy["segment_id"],
                                     'segment_deletedate' : getCurrentDateTime()    
                                }),
                                headers = response_hdr,
                                content_type = content_types.APPLICATION_JSON 
                            )    

    except Exception as er:
        print(er)        

    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )          




def delCampSegment(pinpointid,lstSegmentid):
    error = ''
    
    try:
        campResp = getCampaigns(pinpointid)
        
        if campResp:
            print("campaign exist")
            isInProgress = False
            lstCampId = []
            for iSeg in lstSegmentid:
                for cr in campResp:
                    if cr["segment_id"] == iSeg:
                        print('campaign segment matches') 
                        lstCampId.append(cr["camp_id"])
                        if cr["state"]["CampaignStatus"].lower() != "completed":
                            print('campaign is in progress')
                            isInProgress = True
                            error = "Campaign is in progress"
                            break
                    
            if not isInProgress: 
                if lstCampId:
                    for iCamp in lstCampId:
                        if not deleteCampaignpp(pinpointid,iCamp):      
                            error = "Unable to delete campaign(id):" + iCamp     
                    if not error:
                        for iSeg in lstSegmentid:
                            segResp = deleteSegmentPP(pinpointid,iSeg)
                            if segResp:
                                error = segResp
                else:
                    for iSeg in lstSegmentid:
                        segResp = deleteSegmentPP(pinpointid,iSeg)
                        if segResp:
                            error = segResp         
                                          
        else:
            for iSeg in lstSegmentid:
                segResp = deleteSegmentPP(pinpointid,iSeg)
                if segResp:
                    error = segResp
                
    except Exception as er:
        print(er)                        

    return error


def getCampSegmentStatus(pinpointid,lstSegmentid):
    error = ''
    
    try:
        campResp = getCampaigns(pinpointid)
        
        if campResp:
            print("campaign exist")
            isCompleted = False
            isScheduled = False
            isProcessing = False
            isPaused = False
            isDeleted = False
            for iSeg in lstSegmentid:
                for cr in campResp:
                    if cr["segment_id"] == iSeg:
                        if cr["state"]["CampaignStatus"].lower() == "completed":
                            isCompleted = True
                        elif cr["state"]["CampaignStatus"].lower() == "scheduled":
                            isScheduled = True
                        elif cr["state"]["CampaignStatus"].lower() == "paused":
                            isPaused = True
                        elif cr["state"]["CampaignStatus"].lower() == "deleted":
                            isDeleted = True
                        else:
                            isProcessing = True                
                        
            if isProcessing:
                return "Processing"
            if isPaused:
                return "Paused"
            if isScheduled:
                return "Scheduled"
            if isDeleted:
                return "Deleted"
            if isCompleted:
                return "Completed"                                
                    
                
    except Exception as er:
        print(er)                        

    

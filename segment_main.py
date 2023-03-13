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
        #return getCampaigns(bdy["pinpointprojectid"])
        if 'pinpointprojectid' not in  bdy:
            error_400 = "pinpoint project id does not exist"                
        elif 'segment_group'  in bdy:
            segResp = getSegmentIdsPP(bdy["pinpointprojectid"],bdy["segment_group"])
            if segResp:
                for ids in segResp:
                    segResp = deleteSegmentPP(bdy["pinpointprojectid"],bdy["segment_id"])
                    if segResp:
                        error_500 = segResp
                    
                if not error_500:
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
            campResp = getCampaigns(bdy["pinpointprojectid"])
            bSuccess = False
            if campResp:
                isInProgress = False
                lstCampId = []
                for cr in campResp:
                    if cr["segment_id"] == bdy["segment_id"]: 
                        lstCampId.append(cr["camp_id"])
                        if cr["state"].lower() != "completed":
                            isInProgress = True
                            error_400 = "Campaign is in progress"
                if not isInProgress: 
                    if lstCampId:
                        for iCamp in lstCampId:
                            if not deleteCampaignpp(bdy["pinpointprojectid"],iCamp):      
                                error_500 = "Unable to delete campaign(id):" + iCamp     
                        if not error_500:
                            segResp = deleteSegmentPP(bdy["pinpointprojectid"],bdy["segment_id"])
                            if segResp:
                                error_500 = segResp
                    else:
                        segResp = deleteSegmentPP(bdy["pinpointprojectid"],bdy["segment_id"])
                        if segResp:
                            error_500 = segResp
    
                            
                                   






                            if deleteCampaignpp(bdy["pinpointprojectid"],cr["camp_id"]):
                                segResp = deleteSegmentPP(bdy["pinpointprojectid"],bdy["segment_id"])
                                if segResp:
                                    error_500 = segResp
                                else:
                                    bSuccess = True   
                        else:
                            error_500 = "Campaign is in progress"

            if not bSuccess:            
                segResp = deleteSegmentPP(bdy["pinpointprojectid"],bdy["segment_id"])
                if segResp:
                    error_500 = segResp
                else:
                    bSuccess = True    
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

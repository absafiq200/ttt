import json
import os
from validation import  validateCampaignKey,validateRunCampaignKey,getCampName,validateRunCampaignKeyW
from http_entity_util import getCampaignRequestItem,getCreateCampaignRequest,getCampaignRunRequest
from dynamodb_util import * 
from pinpoint_util import checkPinpointidExist,getSegmentName,getSMSTemplate,getEmailTemplate,createCampaign,getCampaignStatus,deleteCampaignpp,updateCampaignpp,updateCampaignStatuspp
from http_util import (response_hdr)
from cust_date_util import getCurrentDateTime,isStartDateBefore30Mts
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.event_handler import (Response,content_types)

tracer = Tracer()
logger = Logger()
router = APIGatewayHttpRouter()

@router.post("/create_campaign")
@tracer.capture_method
def create_campaign():        
    logger.info(router.current_event.json_body)
    error_400=''
    error_500=''
    try:
        campaign = router.current_event.json_body
        rtn = validateCampaignKey(campaign)   
        if not rtn:
           req = getCampaignRequestItem(campaign)  
           logger.debug({'create_campaig request->':str(req)})
           chkPP = checkPinpointidExist(req["pinpointprojectid"])
           logger.debug({'check pinpoint project id exist->':str(chkPP)})
           if not chkPP:
                error_400 = 'Pinpoint Project ID does not exist'                
           else:      
                chkexit = check_campaign_exist(os.environ.get('CAMPAIGN_TABLE'), req['campaign_name'])   
                logger.debug({'check campaign already exist->':str(chkexit)})
                if chkexit:
                    error_400 = 'Campaign already exist'                    
                else:
                    cmpResp = create_dyno_item(os.environ.get('CAMPAIGN_TABLE'), req)
                    if cmpResp:
                        return Response(
                                status_code = 201,
                                body = json.dumps(cmpResp),
                                headers = response_hdr,
                                content_type = content_types.APPLICATION_JSON 
                            )
                    else:      
                        error_500  = 'Internal Error-unable to create campaign'                         
        else:
            error_400 = 'Bad Request missing required parameters'
            
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
 

@router.put("/update_campaign")
@tracer.capture_method
def update_campaign():        
    logger.info(router.current_event.json_body)
    error_400=''
    error_500=''

    try:
        bdy = router.current_event.json_body
        if 'campaign_id' not in bdy:        
            error_400 = "Bad Request campaign id missing"
        else:
            campResp = getCampaigndb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id']) 
            if not campResp:
                error_400 = 'Campaign does not exist'
            else:
                rtn = validateCampaignKey(bdy)
                if rtn:
                    error_400 = 'Bad Request missing required parameters'
                else:
                    req = getCampaignRequestItem(bdy)  
                    if campResp.camp_status.upper()  in ("NEW","COMPLETED"):
                        
                        chkPP = checkPinpointidExist(req["pinpointprojectid"])
                        if not chkPP:
                            error_400 = 'Pinpoint Project ID does not exist'                
                        else:
                            cmpResp = create_dyno_item(os.environ.get('CAMPAIGN_TABLE'), req)
                            if cmpResp:
                                return Response(
                                        status_code = 200,
                                        body = json.dumps(cmpResp),
                                        headers = response_hdr,
                                        content_type = content_types.APPLICATION_JSON 
                                    )
                            else:      
                                error_500  = 'Internal Error-unable to update campaign'
                    elif campResp.camp_status.lower()  in ("scheduled","processing","running"):   
                        cmpResp = update_campaigndb(os.environ.get('CAMPAIGN_TABLE'), req)
                        if cmpResp:
                            return Response(
                                    status_code = 200,
                                    body = json.dumps(cmpResp),
                                    headers = response_hdr,
                                    content_type = content_types.APPLICATION_JSON 
                                )
                        else:      
                            error_500  = 'Internal Error-unable to update campaign'      

                    else:
                        error_400 = "Unable to update campaign status is - " + campResp.camp_status    

    except Exception as er:
        logger.error(er)

    return Response(
                status_code = 400 if error_400 else 500,
                body = json.dumps({
                        "error": error_400 if error_400 else error_500 
                }),
                headers = response_hdr,
                content_type = content_types.APPLICATION_JSON 
            )


@router.post("/create_campaign/run")
@tracer.capture_method
def create_run_campaign(): 
    logger.info(router.current_event.json_body)   
    error_400=''
    error_500='' 
    try:
        campaign = router.current_event.json_body
        rtn = validateRunCampaignKey(campaign)        
        if rtn:
            error_400 = rtn            
        else:           
            campResp = getCampaigndb(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id']) 
            if not campResp:
                error_400 = "Invalid campaign id"                 
            else:
                segmentRtn = getSegmentName(campResp.pinpointprojid,campaign['segment_id']) 
                if not segmentRtn:
                    error_400 = "Invalid Segment ID"                     
                else:
                    rep2=''
                    if campaign['campaign_channel'].upper() == "SMS":
                        rep2 = getSMSTemplate(campaign['sms_template'])
                    else:
                        rep2 = getEmailTemplate(campaign['email_template'])    
                    if not rep2:
                        error_400 = "Invalid template name"                        
                    else:                  
                        cmpName =  getCampName(campResp.camp_name,segmentRtn)   
                        logger.info({'Campaign name:',cmpName}) 
                        if not cmpName:
                            error_400 = "Segment file name does not contain language"                                                    
                        else:
                            campRequest = getCreateCampaignRequest(cmpName, campaign,campResp)     
                            logger.info({'campRequest':campRequest})
                            if not campRequest:
                                error_500 = "Internal error"                                 
                            else:
                                crtn = createCampaign(campRequest,campResp.pinpointprojid)        
                              
                                if crtn:                                    
                                    campRunReq = getCampaignRunRequest(campaign,crtn['Run_id'],cmpName,campResp.camp_msg_type)
                                  
                                    lst = getCampaignRuns(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id'],'','')
                                    
                                    if not lst:                                        
                                        lst = []
                                    lst.append(campRunReq)        
                                    succ = update_campaignstatusdb(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id'],lst,crtn['State'],crtn['Run_id'],campResp.lstRunId)
                                    if not succ:
                                        error_500 = "Campaign Scheduled Unable to update in database"                                        
                                    else:
                                        return Response(
                                            status_code = 201,
                                            body = json.dumps(succ),
                                            headers = response_hdr,
                                            content_type = content_types.APPLICATION_JSON 
                                        )                                    
                                else:
                                    error_400 = "unable to create run campaign"
                                    

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


@router.put("/update_campaign/run")
@tracer.capture_method
def update_run_campaign(): 
    logger.info(router.current_event.json_body)   
    error_400=''
    error_500='' 
    try:
        campaign = router.current_event.json_body
        rtn = validateRunCampaignKeyW(campaign)        
        if rtn:
            error_400 = rtn            
        else:           
            if not isStartDateBefore30Mts(campaign["campaign_starttime"]):
                error_400 = "Campaign can not be updated within 30 minutes of start datetime."
            else:
                campResp = getCampaignRundb(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id'],campaign["campaign_run_id"]) 
                print('11')
                if not campResp:
                    error_400 = "campaign Id does not exist" 
                elif not campResp.lstRunId:
                    error_400 = "campaign run id does not exist"                 
                else:
                    print('22')
                    segmentRtn = getSegmentName(campResp.pinpointprojid,campaign['segment_id']) 
                    if not segmentRtn:
                        error_400 = "Invalid Segment ID"                     
                    else:
                        rep2 =''
                        if campaign['campaign_channel'].upper() == "SMS":
                            rep2 = getSMSTemplate(campaign['sms_template'])
                        else:
                            rep2 = getEmailTemplate(campaign['email_template'])    
                        if not rep2:
                            error_400 = "Invalid template name"                        
                        else:
                            print('33')
                            cmpName =  getCampName(campResp.camp_name,segmentRtn)   
                            logger.info({'Campaign name:',cmpName}) 
                            if not cmpName:
                                error_400 = "Segment file name does not contain language"                                                    
                            else:
                                print('444')
                                campRequest = getCreateCampaignRequest(cmpName, campaign,campResp)    
                                print('555')
                                print(type(campRequest))
                              
                                logger.info({'campRequest':campRequest})
                                if not campRequest:
                                    error_500 = "Internal error"                                 
                                else:
                                    print('55')
                                    crtn = updateCampaignpp(campRequest,campResp.pinpointprojid,campaign["campaign_run_id"])                            
                                    if crtn: 
                                        print('66')
                                        campRunReq = getCampaignRunRequest(campaign,crtn['Run_id'],cmpName,campResp.camp_msg_type)
                                        print('77')
                                        lst = getCampaignRuns(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id'],crtn['Run_id'],campRunReq)
                                        print('88')
                                        if not lst:
                                            error_400 = "unable to find campaign runs"
                                        else:
                                            succ = update_campaignstatusdb(os.environ.get('CAMPAIGN_TABLE'),campaign['campaign_id'],lst,crtn['State'],crtn['Run_id'],True)
                                            if not succ:
                                                error_500 = "Campaign Scheduled Unable to update in database"                                        
                                            else:
                                                return Response(
                                                    status_code = 201,
                                                    body = json.dumps(succ),
                                                    headers = response_hdr,
                                                    content_type = content_types.APPLICATION_JSON 
                                                )                                    
                                    else:
                                        error_400 = "unable to update run campaign"
                                        
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


@router.get("/list_campaign")
@tracer.capture_method
def listCampaigns():
    return Response(
                    status_code = 200,
                    body = json.dumps(getAllCampaignsdb(os.environ.get('CAMPAIGN_TABLE'))),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )

    

@router.delete("/delete_campaign")
@tracer.capture_method
def delete_campaign():
    logger.info(router.current_event.json_body)    
    error_400=''
    error_500=''
    try:
        bdy = router.current_event.json_body
        if 'campaign_id' not in bdy:        
            error_400 = "Bad Request"            
        else:
             campResp = getCampaigndb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'])  
             if not campResp:
                error_400 = "Campaign does not exist"                
             else:  
                if campResp.camp_status .upper() in("NEW", "COMPLETED"):
                    if campResp.lstRunId:
                        for rid in campResp.lstRunId:
                            campDelResp = deleteCampaignpp(campResp.pinpointprojid,rid)
                    delCampRtn = delete_campaigndb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'])
                    print(delCampRtn)
                    if delCampRtn:
                        print('aaaaaaa')
                        return Response(
                            status_code = 200,
                            body = json.dumps({
                                        "campaign_id": bdy["campaign_id"],
                                        "campaign_name": campResp.camp_name,
                                        "campaign_deletedate" :getCurrentDateTime()
                                    }),
                            headers = response_hdr,
                            content_type = content_types.APPLICATION_JSON 
                        )
                    else:
                        print('bbbbb')
                        error_400 = "Unable to delete Campaign"                                    
                else:
                    error_400 = "Unable to delete, campaign status is " + campResp.camp_status
                
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


@router.delete("/delete_campaign/run")
@tracer.capture_method
def delete_run_campaign():
    logger.info(router.current_event.json_body)    
    error_400=''
    error_500=''
    try:
        bdy = router.current_event.json_body
        if 'campaign_id' not in bdy:        
            error_400 = "Bad Request - campaign id missing"
        elif 'campaign_run_id' not in bdy:
            error_400 = "Bad Request - campaign run id missing"        
        else:
            print('z1')
            campResp = getCampaigndb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'])  
            if not campResp:
                error_400 = "Campaign does not exist"                
            elif not campResp.lstRunId:
                error_400 = "Campaign run does not exist"                
            else:
                if campResp.camp_status .upper() in("NEW", "COMPLETED"):
                 
                    for rid in campResp.lstRunId:
                        if rid == bdy['campaign_run_id']:                        
                            print('z4')
                            campDelResp = deleteCampaignpp(campResp.pinpointprojid,rid)
                            
                            lst = getCampaignRunsExcept(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'],rid)
                            
                            print(type(lst))
                            print(lst)
                            succ = delete_campaignRundb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'],rid,lst)
                            print('z7')
                            print(succ)
                            if not succ:
                                print('z77')
                                error_500 = "Campaign deleted in pinpoint but Unable to update in database"                                        
                            else:
                                print('z8')
                                return Response(
                                    status_code = 200,
                                    body = json.dumps(succ),
                                    headers = response_hdr,
                                    content_type = content_types.APPLICATION_JSON 
                                )
                            break                                           
                        
                else:     
                    error_400 = "Unable to delete, campaign status is " + campResp.camp_status

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


@router.post("/get_campaign")
@tracer.capture_method
def getCampaign():
    logger.info(router.current_event.json_body)    
    try:
        bdy = router.current_event.json_body
        if 'campaign_id' not in bdy:        
            return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "Bad Request missing parameter"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )            
        else:
            lst = getCampdb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'])
            return Response(
                    status_code = 200,
                    body = json.dumps(lst) if lst else [],
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )
    except Exception as er:   
        logger.error(er)         

    return Response(
                    status_code = 500,
                    body = json.dumps({
                            "error": "Internal Error"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )

@router.post("/start_campaign")
@tracer.capture_method
def start_campaign():
    logger.info(router.current_event.json_body)    
    
    bdy = router.current_event.json_body
    if 'campaign_id' not in bdy:        
        error_400 = "Bad Request - campaign id missing"
    elif 'campaign_run_id' not in bdy:
        error_400 = "Bad Request - campaign run id missing"        
    else:
        if bdy['campaign_run_id'].lower() == "all":
            return reset_all_campaign(bdy['campaign_id'],False)
        else:
            return reset_single_campaign(bdy['campaign_id'],bdy['campaign_run_id'],False)  


@router.post("/stop_campaign")
@tracer.capture_method
def stop_campaign():
    logger.info(router.current_event.json_body)    
    
    bdy = router.current_event.json_body
    if 'campaign_id' not in bdy:   
        return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "Bad Request - campaign id missing"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )
    elif 'campaign_run_id' not in bdy:
        
        return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "Bad Request - campaign run id missing"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )      
    else:
        if bdy['campaign_run_id'].lower() == "all":
            return reset_all_campaign(bdy['campaign_id'],True)
        else:
            return reset_single_campaign(bdy['campaign_id'],bdy['campaign_run_id'],True)    


def reset_single_campaign(campid,camp_run_id,status):
    error_400=''
    error_500=''
    try:
        campResp = getCampaignRundb(os.environ.get('CAMPAIGN_TABLE'),campid,camp_run_id)            
        if not campResp:
            error_400 = "Campaign does not exist"                
        elif not campResp.lstRunId:
            error_400 = "Campaign run does not exist"                
        else:
            rtnStatus = updateCampaignStatuspp(campResp.pinpointprojid,campid,False)
            if rtnStatus:
                updateDate = update_campaignLastUpdatedb(os.environ.get('CAMPAIGN_TABLE'),campid,rtnStatus)
                if updateDate:
                    return Response(
                                status_code = 200,
                                body = json.dumps({
                                    "campaign_run_id" : campid,
                                    "campaign_lastupdated": updateDate
                                }),
                                headers = response_hdr,
                                content_type = content_types.APPLICATION_JSON 
                            )
                else:
                    error_400 = "Campaign started but unable to update in table"                            
    except Exception as er:
        logger.error(er)    

    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )      

def reset_all_campaign(campid,status):
    error_400=''
    error_500=''
    try:
        campResp = getCampaigndb(os.environ.get('CAMPAIGN_TABLE'),campid)
        if not campResp:
            error_400 = "Campaign does not exist"                
        elif not campResp.lstRunId:
            error_400 = "Campaign run does not exist"                
        else:
            isError = False
            for rid in campResp.lstRunId:
                rtnStatus = updateCampaignStatuspp(campResp.pinpointprojid,rid,False)
                if not rtnStatus:
                    error_400 = "some campaign could not be started"
                    isError = True
                if not isError:
                    updateDate = update_campaignLastUpdatedb(os.environ.get('CAMPAIGN_TABLE'),campid,rtnStatus)
                    if updateDate:
                        lstcp = []
                        for k in campResp.lstRunId:
                            lstcp.append({
                                "campaign_run_id":k
                            })
                        return Response(
                                    status_code = 200,
                                    body = json.dumps({                                        
                                        "campaign_lastupdated": updateDate,
                                        "Items": lstcp
                                    }),
                                    headers = response_hdr,
                                    content_type = content_types.APPLICATION_JSON 
                                )
                    else:
                        error_400 = "Campaign started but unable to update in table"                            
    
    except Exception as er:
        logger.error(er)

    return Response(
                    status_code = 400 if error_400 else 500,
                    body = json.dumps({
                            "error": error_400 if error_400 else error_500 
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )          

@router.post("/get_campaign/run")
@tracer.capture_method
def get_run_campaign():
    logger.info(router.current_event.json_body)    
    
    bdy = router.current_event.json_body
    if 'campaign_id' not in bdy:   
        return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "Bad Request - campaign id missing"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )
    elif 'campaign_run_id' not in bdy:        
        return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "Bad Request - campaign run id missing"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )      
    else:
        resp = getCampRunOnlydb(os.environ.get('CAMPAIGN_TABLE'),bdy['campaign_id'],bdy['campaign_run_id'])
        if resp:
            return Response(
                status_code = 200,
                    body = json.dumps({
                            "campaign_run_id": resp["campaign_run_id"],
                            "campaign_id": resp["campaign_id"],
                            "campaign_type": resp["campaign_channel"], 
                            "email_template": resp["email_template"], 
                            "sms_template": resp["sms_template"], 
                            "segment_id": resp["segment_id"], 
                            "campaign_quiettimes": resp["campaign_quiettimes"], 
                            "campaign_run_name": resp["campaign_run_name"],
                            "campaign_starttime": resp["campaign_starttime"],
                            "campaign_endtime": resp["campaign_endtime"],
                            "campaign_run_status" : getCampaignStatus(resp['pinpointprojectid'],resp["campaign_run_id"])
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
            )
        else:
            return Response(
                    status_code = 400,
                    body = json.dumps({
                            "error": "campaign run does not exist"
                    }),
                    headers = response_hdr,
                    content_type = content_types.APPLICATION_JSON 
                )      

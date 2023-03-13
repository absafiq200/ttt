from pinpoint_util import create_sms_template_pp,update_sms_template_pp,delete_sms_template_pp
from validation_util import getTypePathParameter,getRequestBody,getTemplatePathParameter
from http_util import response_hdr
import json
import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.event_handler import (Response,content_types)

tracer = Tracer()
logger = Logger()
router = APIGatewayHttpRouter()

@router.post("/reports/<type>/create")
@tracer.capture_method
def create_report(type):
    logger.info({'type':type })
   
@router.put("/reports/<type>/update")
@tracer.capture_method   
def update_report(type):
    logger.info({'type':type })
   
@router.delete("/reports/<type>/delete/<reportid>")    
@tracer.capture_method       
def delete_report(type,reportid):
    logger.info({'type':type , 'ReportId:':reportid})
   
@router.get("/reports/<type>/get/<reportid>")    
@tracer.capture_method       
def get_report(type,reportid):
    logger.info({'type':type , 'reportid:':reportid})

@router.get("/reports/list_reports")    
@tracer.capture_method       
def get_allreports():
    print()


    
    

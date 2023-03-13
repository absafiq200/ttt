import boto3
import json
from http_util import response_hdr


pinpoint = boto3.client("pinpoint")

def delete_sms_template_pp(template_name):
    try:
        response = pinpoint.delete_sms_template(
                        TemplateName = template_name
                    )
        print(response)            
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return ''
    except Exception as em:
        print('update_sms_template_pp error:',em)
        return str(em).split(':')[1]
    return 'Unable to delete sms template'

def update_sms_template_pp(event):
    try:
        response = pinpoint.update_sms_template(
                      
                        SMSTemplateRequest = {
                                'Body': event['template_sms'],
                                'DefaultSubstitutions': json.dumps(event['template_default_attributes']) if event['template_default_attributes'] else '{}',
                                'TemplateDescription': event['template_name']
                            },
                        TemplateName = event['template_name'] 
                    )
        print(response)            
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return ''   
    except Exception as em:
        print('update_sms_template_pp error:',em)
        return str(em).split(':')[1]   
    return 'Unable to update sms template'

    
def create_sms_template_pp(event):
    print(event)
    print('s1')
    try:
        
        response = pinpoint.create_sms_template(
            
                    SMSTemplateRequest = {
                                'Body': event['template_sms'],
                                'DefaultSubstitutions': json.dumps(event['template_default_attributes']) if event['template_default_attributes'] else '{}',
                                'TemplateDescription': event['template_name']
                            },
                        TemplateName = event['template_name'] 
                    )
        print('s2')
        print(response)
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return (response['CreateTemplateMessageBody']['Arn'],'')
        
    except Exception as em:
        print('create_sms_template_pp error:',em)
        return ('',str(em).split(':')[1])    
    return('','Unable to create sms template')        

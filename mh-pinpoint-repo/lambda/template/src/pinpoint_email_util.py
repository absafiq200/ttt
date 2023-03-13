import boto3
import json
from http_util import response_hdr


pinpoint = boto3.client("pinpoint")

def delete_email_template_pp(template_name):
    print('del')
    print(template_name)
    try:
        response = pinpoint.delete_email_template(
                        TemplateName = template_name
                    )
        print(response)            
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return ''    
    except Exception as em:
        print('delete_email_template_pp error:',em)
        return str(em).split(':')[1]
    return 'Unable to delete email template'


def update_email_template_pp(event):
    try:
        response = pinpoint.update_email_template(
                        EmailTemplateRequest = {
                                'HtmlPart': event['template_email']['html'] ,
                                'DefaultSubstitutions': json.dumps(event['template_default_attributes']) if event['template_default_attributes'] else '{}',
                                'TemplateDescription': event['template_name'],
                                'Subject': event['template_email']['subject'] ,
                                'TextPart': event['template_email']['plaintext'] 
                     
                            },
                        TemplateName = event['template_name'] 
                    )
        print(response)            
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return ''   
    except Exception as em:
        print('update_email_template_pp error:',em)
        return str(em).split(':')[1]  
    return 'Unable to update email template'

def create_email_template_pp(event):
    print(event)
    print('s1')
    try:
        
        response = pinpoint.create_email_template(
            
                    EmailTemplateRequest = {
                                'HtmlPart': event['template_email']['html'] if 'html' in event['template_email'] else '',
                                'DefaultSubstitutions': json.dumps(event['template_default_attributes']) if event['template_default_attributes'] else '{}',
                                'TemplateDescription': event['template_name'],
                                'Subject': event['template_email']['subject'] ,
                                'TextPart': event['template_email']['plaintext'] 
                            },
                        TemplateName = event['template_name'] 
                    )
                    
        print('s2')
        print(response)
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']:
            return (response['CreateTemplateMessageBody']['Arn'],'')
        
    except Exception as em:
        print('create_email_template error:',em)
        return ('',str(em).split(':')[1])    
    return('','Unable to create email template')    

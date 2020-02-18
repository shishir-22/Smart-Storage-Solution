import boto3
import json
import time
from botocore.exceptions import ClientError

session=boto3.Session(region_name='us-east-1',aws_access_key_id='AKIAI4344ZBMKIEDIFLQ',aws_secret_access_key='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')
sns_client=session.client('sns')
sns_resource=session.resource('sns')
iam_client = session.client('iam')
lambda_client = session.client('lambda')
cloudwatch_events = session.client('events')

class infrastructure:
    def __init__(self,status_code,access_method,username,cron,url,subscribers):
        self.username=str(username)
        self.status_code=str(status_code)
        self.url=str(url)
        self.subscribers=subscribers
        self.cron=cron
        self.access_method=access_method

    def createTopic(self):
        self.topic_response =sns_client.create_topic(
                Name=self.username
            )
#####    FOR JOINING SUBSCRIBERS TO A SPECIFIC TOPIC ########

    def attachSubscriber(self):
        for email in self.subscribers:
            targetarn=sns_client.subscribe(
                TopicArn=self.topic_response['TopicArn'],
                Protocol='email',
                Endpoint=email
            )

######   FOR SENDING MAIL TO A TOPIC ######

    # def sendmail(self,status,response_time):
    #     message="your website status is "+str(status) +" and response time is = "+str(response_time)
    #     send=sns_client.publish(
    #         TargetArn=self.topic_response['TopicArn'],
    #         Message=message,
    #         Subject='pingdom'
    #     )
    ######################## Lambda function creation ####################
    def createLambdaStack(self):
        role=iam_client.get_role(RoleName='sns-lambda')
        fn_name = self.username
        fn_arn = role['Role']['Arn']
        try:
            self.lambda_response=lambda_client.create_function(
            FunctionName=fn_name,
            Runtime='python3.6',
            Role=str(fn_arn),
            Handler="{0}.listf".format('url2'),
            Code={'ZipFile': open("/home/ronozor/Downloads/Projects/code/thanosback/form/hello.zip", 'rb').read(),},
            Environment={
                'Variables':{
                    'url':self.url,
                    'status':self.status_code,
                    'user':self.username,
                    'topic_arn':self.topic_response['TopicArn'],
                }
                } 
            )
        except Exception as e2:
            print(e2)
            string1="An error occurred (ResourceConflictException) when calling the CreateFunction operation: Function already exist: " + fn_name 
            if str(e2)==string1:
                print("The Lambda Function already exists.")

        payload = {
            "Name1":"Yash",
            "Name2":"Shivansh"
        }

        try:
        ## Invoking lambda function manually ###
            invoke_response = lambda_client.invoke(
            FunctionName=fn_name,
            InvocationType='Event',
            Payload=json.dumps(payload),
            LogType='None',
            )
            #print(invoke_response)
        except Exception as e:
            print(e)


    # Put an event rule
        rule_response = cloudwatch_events.put_rule(
            Name=fn_name,
            ScheduleExpression='rate('+str(self.cron)+' minutes)',
            State='ENABLED'
        )
        
    # print(rule_response['RuleArn'])
    ### Adding permission to lambda, so that cloudwatch rule can invoke it ### 
        lambda_perm=lambda_client.add_permission(
            FunctionName=fn_name,
            StatementId='1',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_response['RuleArn']
        )

    # print(f"lambda Permission{lambda_perm}\n")
    ### Adding trigger ###
        target_response = cloudwatch_events.put_targets(
            Rule=fn_name,
            Targets=[
                {
                    'Arn': self.lambda_response['FunctionArn'],
                    'Id': '1',
                }
            ]
        )


        

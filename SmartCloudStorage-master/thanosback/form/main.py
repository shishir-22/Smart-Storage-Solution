import stack_build as infra
# import boto3
# session=boto3.Session(region_name='us-east-1',aws_access_key_id='AKIAJQEGX7NLY7BBWGAA',aws_secret_access_key='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')
    obj=infra.infrastructure('200','POST','yash2','5','http://www.tothenew.com',subscriber)
    obj.createTopic()
    obj.attachSubscriber()
    obj.createLambdaStack()


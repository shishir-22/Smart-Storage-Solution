from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Userdata
from .forms import Formsignup
from django.shortcuts import redirect
import form.stack_build as infra
from django import template
import logging
import boto3
from botocore.exceptions import ClientError
import subprocess
from django.core.files.storage import FileSystemStorage



def index(request):

    access_key= 'AKIAIONRI7KJDWQX44CQ'
    secret_key= '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'
    bucket_name="scs-sqlite"
    version_name=''
    file_name="db.sqlite3"
    object_name=file_name
    a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+""",'object_name':"""+object_name+""",'version_name':"""+version_name+""",'file_name':"""+file_name+"""}" download_obj.yaml""") 
    print(a)

    return render(request,'form/landing.html')

def login_form(request):
    return render(request,'form/login.html')

def signup_form(request):
    return render(request,'form/registration.html')

def entry_signup_data(request):
    access_key= 'AKIAIONRI7KJDWQX44CQ'
    secret_key= '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'
    
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            post=Userdata()
            post.email= request.POST.get('email')
            post.password= request.POST.get('password')
            post.user_name=request.POST.get('user_name')
            post.id=request.POST.get('id')
            post.save()
            bucket_name="sbucketscs"+str(post.id)
            print(bucket_name)
            user_id= post.user_name

            a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'aws_access_key':"""+access_key+""",'aws_secret_key':"""+secret_key+""",'user_id':"""+user_id+"""}" create_bucket_and_tag.yaml""")
            print(a)
            
            bucket_name="scs-sqlite"
            version_name=''
            file_name="db.sqlite3"
            object_name=file_name
            a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+""",'object_name':"""+object_name+""",'version_name':"""+version_name+""",'file_name':"""+file_name+"""}" upl_obj.yaml""") 
            print(a)
            return render(request, 'form/logindone.html')  


def entry_form(request):
    if request.method == 'POST':
        context={
            'id':request.session['id'],
        }
        return render(request,'form/user/entry1.html',context)

def entry_login_data(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email=request.POST.get('email')
            password=request.POST.get('password')
            result=Userdata.objects.all()
            flag=0
            for i in result:
                if i.email==email and i.password==password:
                    flag=1
                    request.session['id']=i.id
                    request.session['user_name']=i.user_name
                    print(request.session['id'])
                    break
                else:
                    flag=0
            if flag==1:
                # return render(request, '/form/user/check/', {"id" : id})
                return redirect('/form/user/check/'+str(i.id))
            else:
                # return render('/form/login')
                return redirect('/form/login')

def entry_form_data(request):
    if request.method=='POST':
        ids=request.POST.get('value')
        post=User_url_info()
        post1=Userdata.objects.all()
        for i in post1:
            if i.id == int(ids):
                post.userid=i
                break
        post.url=request.POST.get('url')
        post.subscribers=request.POST.get('subscriber')
        post.status=request.POST.get('status')
        post.access=request.POST.get('access')
        post.cron=request.POST.get('cron')
        subscribers=post.subscribers.split(",")
        # print(i.user_name)
        last_id=User_url_info.objects.all()   
        username=i.user_name+str(last_id[len(last_id)-1].id+1)
        obj=infra.infrastructure(post.status,post.access,username,post.cron,post.url,subscribers)
        obj.createTopic() 
        obj.attachSubscriber()
        obj.createLambdaStack()
        post.save()
        ids=request.POST.get('value')
        response=redirect('/form/user/check/'+ids)
        return response

def data_display(request,objects):

    post1 = Userdata.objects.all()
    
    # a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'aws_access_key':"""+access_key+""",'aws_secret_key':"""+secret_key+""",'user_id':"""+user_id+"""}" create_bucket_and_tag.yaml""")
    # print(a)

        # return render(request,'form/user/entry1.html',context)

        #SHOW DASHBOARD

        #PYTHON SCRIPT TO RUN ANSIBLE PLAYBOOK - CREATE BUCKET


    return render(request,'form/dashboard.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        access_key= 'AKIAIONRI7KJDWQX44CQ'
        secret_key= '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'

        uid=request.session['id']
        bucket_name="sbucketscs"+str(uid)
        object_name=uploaded_file_url
        file_name=uploaded_file_url
        version_name=''
        a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+""",'object_name':"""+object_name+""",'version_name':"""+version_name+""",'file_name':"""+file_name+"""}" upl_obj.yaml""") 
        print(a)


        return render(request, 'form/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'form/simple_upload.html')

def list_files(request):
    if request.method == 'GET':
        user_name=request.GET.get('user_name')
        print(user_name)
        uid=request.session['id']
        bucket_name="sbucketscs"+str(uid)
        print(bucket_name)
        access_key= 'AKIAIONRI7KJDWQX44CQ'
        secret_key= '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'

        a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+"""}" list_objects.yaml""") 
        print(a)
        print(a[1])
        b=a[1].split("{\n")[1].split("\n}")[0]
        print(b)
        b=b.replace('"msg": [\n',"").replace("]","").replace(",","").replace('"',"").split("\n")
        for i in range(0,len(b)):
            b[i]=b[i].strip()
        b=b[:-1]
        print(b)
        context={'b':b}
        return render(request, 'form/list_files.html',context)
    return render(request, 'form/list_files.html')


def delete_filesPage(request):
    return render(request, 'form/delete_files.html')

def delete_files(request):
    if request.method == "POST":
        user_name=request.POST.get('user_name')
        print(user_name)
        uid=request.session['id']
        bucket_name="sbucketscs"+str(uid)
        print(bucket_name)
        access_key= 'AKIAIONRI7KJDWQX44CQ'
        secret_key= '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'
        object_name=''
        object_name=object_name+request.POST.get('file_name')

        file_name=object_name
        version_name=''
        a=subprocess.getstatusoutput("""ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+""",'object_name':"""+object_name+""",'version_name':"""+version_name+"""}" deleteobj.yaml""") 


        print(a)
        b=object_name
        context={'b':b}
        return render(request, 'form/deleted.html',context)
    return render(request, '/form/delete_files.html')


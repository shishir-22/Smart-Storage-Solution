import subprocess
bucket_name='tfuesbucket'
access_key= 'AKIAIONRI7KJDWQX44CQ'
secret_key= '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'
a=subprocess.getstatusoutput("""sudo ansible-playbook --extra-vars="{'bucket_name':"""+bucket_name+""",'access_key':"""+access_key+""",'secret_key':"""+secret_key+"""}" list_objects.yaml""") 
b=a[1].split("{\n")[1].split("\n}")[0]
b=b.replace('"msg": [\n',"").replace("]","").replace(",","").replace('"',"").split("\n")
for i in range(0,len(b)):
	b[i]=b[i].strip()
b=b[:-1]
print(b)

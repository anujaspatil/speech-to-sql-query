import os

from numpy import append
from sql.models import Sql
import speech_recognition as sr
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from sql.nlp import *
from django.db import connection
import json

def home(request):
    if request.user.is_authenticated:
        sqls = Sql.objects.filter(user=request.user)
        all_users = User.objects.filter(queries__isnull=False).distinct()
        newList=[]
        for ia in sqls.values():
            temp=[]
            
            ia['output']=ia['output'].replace("(","")
            ia['output']=ia['output'].replace("'","")
            print(ia['output'])
            for jb in ia.get('output').split(")"):
                if(len(jb)==0): continue
                temp2=[]
                for k in jb.split(","):
                        if(len(k)!=0):
                            temp2.append(k)
                temp.append(temp2)
            ia['output']=temp
            newList.append(ia)

        
        ctx = {
            'home': 'active',
            'sql': newList,
            'allusers': all_users
        }
        return render(request, 'sql.html', ctx)
    else:
        return render(request, 'base.html', None)


def upload(request):
    customHeader = request.META['HTTP_MYCUSTOMHEADER']

    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    filename = str(Sql.objects.count())
    filename = filename + "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    # put additional logic like creating a model instance or something like this here
    r = sr.Recognizer()
    harvard = sr.AudioFile(filename)
    with harvard as source:
        audio = r.record(source)
    qry = r.recognize_google(audio)
    os.remove(filename)
    # sql_query1 = Sql(user=request.user, query1=qry)
    # if qry != '':
    #     sql_query1.save()
    # return redirect('/')
    msg=integ(qry)
    cursor = connection.cursor()
        
    cursor.execute(msg)
    row = cursor.fetchall()
    sql_query1 = Sql(user=request.user, query1=qry, output=row)
        
    if qry != '':
        sql_query1.save()   
        # integ(qry)
        # sql_query2 = Sql(user=request.user, output=msg)
        # sql_query2.save()
        print('query is', msg)

        return JsonResponse({'qry': qry, 'output':row})
    else:
        return HttpResponse('Request should be POST.')

def integ(msg1):
    # msg = input(integ1)
    print("User:",msg1)
    msg = msg1.split()
    columns_present = []

    for i in range(len(msg)):
        if msg[i] in Table_name:
            msg[i] = "<table_name>"
    for j in range(len(msg)):
        if msg[j] in columns:
            columns_present.append(msg[j])
            msg[j] = "<column_1>"
    query = " ".join(msg)
    ans = chatbot_response(query)
    ans = ans.replace("<table_name>",Table_name[0])
    col_present_str = ",".join(columns_present)
    #for i in columns_present:
    ans = ans.replace("<column_1>",col_present_str)   

    print("query predicted: ",ans)   
    return ans     


def post(request):
    if request.method == "POST":
        qry = request.POST.get('qrybox', None)
        print('Our value = ', qry)
        msg=integ(qry)
        # str1=msg
        cursor = connection.cursor()
        
        cursor.execute(msg)
        row = cursor.fetchall()
        
        sql_query1 = Sql(user=request.user, query1=qry, output=row)
        
        if qry != '':
            sql_query1.save()   
        # integ(qry)
        # sql_query2 = Sql(user=request.user, output=msg)
        # sql_query2.save()
        print('query is', msg)

        return JsonResponse({'qry': qry, 'output':json.dumps(row)})
    else:
        return HttpResponse('Request should be POST.')


def queries(request):
    sql = Sql.objects.filter(user=request.user)
    return render(request, 'queries.html', {'sql': sql})




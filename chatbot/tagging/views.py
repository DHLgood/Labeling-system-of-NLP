

# Create your views here.
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time

from tagging.forms import UserForm
from tagging.models import Sentence, UserProfile


def index(request):
    return render(request, 'tagging/index.html', {})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Hash the password with the set_password method.
            # Once hashed, update the user object.
            user.set_password(user.password)
            user.save()
            registered = True
            # 为每个用户创建表
            cnx = connect_mysql()  # 连接mysql
            cus = cnx.cursor()     # 创建一个游标对象    try:
            try:
                cus.execute(create_sql%(user.username))
                cus.close()
                cnx.commit()
            except Exception as err:
                cnx.rollback()
                raise err
            finally:
                cnx.close()

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request,
                  'tagging/register.html',
                  {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:
                return render(request, 'super/superlogin.html', {})
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/tagging/')
            else:
                return HttpResponse("Your Tagging account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'tagging/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/tagging/')


def about(request):
    return render(request, 'tagging/about.html', {})


# @login_required
def tag(request):
    if request.user.username:
        return render(request, 'tagging/tag.html', {})
    else:
        return render(request, 'tagging/login.html', {})

    # return render(request, 'tagging/tag.html', {})

import random
@login_required
@csrf_exempt
def ajax_for_tokens_list(request):
    if request.method == 'POST':
        # username = request.POST['username']
        # tag_model_name = request.POST['tag_model_name']
        # #  TODO     tag_type
        # cus.execute("SELECT * FROM "+username+" WHERE tagged=0 AND tag_type='"+tag_model_name+"';" )
        # sentence_test = cus.fetchall()[:5]
        # tokens_and_pos_list = [{'id': sent[0], 'tokens_and_pos': json.loads(sent[4])} for sent in sentence_test]
        # return JsonResponse(tokens_and_pos_list, safe=False)
        username = request.POST['username']
        tag_model_name = request.POST['tag_model_name']
        cus.execute("SELECT * FROM "+username+" WHERE tagged='0' and tag_type='"+tag_model_name+"';" )
        sentence_test = cus.fetchall()[:5]
        tokens_and_pos_list = [{'id': sent[0], 'tokens_and_pos': json.loads(sent[4])} for sent in sentence_test]
        return JsonResponse(tokens_and_pos_list, safe=False)







from tkinter import filedialog
import os
@login_required
@csrf_exempt
def ajax_tag_model_list_get(request):
    if request.method == 'POST':
        pwd = os.getcwd()
        file_dir = pwd+'/model_list/'
        model_list_ = os.listdir(file_dir)
        model_list = [x.split('.')[0] for x in model_list_]
        return JsonResponse(model_list, safe=False)

@login_required
@csrf_exempt
def ajax_tag_model_get(request):
    if request.method == 'POST':
        tag_name=request.POST['tag_model_name']
        model_path = os.getcwd()+"/model_list/"+tag_name+".json"
        if model_path:
            try:
                with open(model_path, 'r') as load_f:
                    model_tag_data_list = json.load(load_f)
            except:
                model_tag_data_list = []
            return JsonResponse(model_tag_data_list, safe=False)











@login_required
@csrf_exempt
def ajax_for_save_tagged_tokens(request):
    if request.method == 'POST':
        data = json.loads(request.POST['taggedResult'])
        tag_model_name = request.POST['tag_model_name']
        username = data['username']
        sents = data['sents']
        current_user = User.objects.filter(username=username)[0]
        cnx = connect_mysql()  # 连接mysql
        cus = cnx.cursor()  # 创建一个游标对象    try:
        for sent in sents:
            sent_id = sent['id']
            last_changed_by_id = current_user
            tokens_and_pos = json.dumps(sent['tagged'], ensure_ascii=False)
            tagged = True
            checked=False
            last_changed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            try:
                cus.execute("""UPDATE """ + username + """ SET last_changed_time='{last_changed_time}',changed_times=changed_times+1,tokens_and_pos='{tokens_and_pos}',tagged='{tagged}',checked='{checked}',last_changed_by_id='{last_changed_by_id}' WHERE id='{id}' AND tag_type='{tag_type}';"""
                .format( last_changed_time=last_changed_time,
                        tokens_and_pos=tokens_and_pos, tagged=int(tagged),
                        checked=int(checked), last_changed_by_id=current_user.id, id=sent_id,tag_type=tag_model_name)
                    # TODO tag_type
                )
            except Exception as err:
                cnx.rollback()
                raise err
            finally:
                # cnx.close()
                pass

        cnx.commit()
        #TODO  tag_type
        cus.execute("SELECT * FROM "+username+" WHERE tagged=0 AND tag_type='"+tag_model_name+"';" )
        sentence_test = cus.fetchall()[:5]
        tokens_and_pos_list = [{'id': sent[0], 'tokens_and_pos': json.loads(sent[4])} for sent in sentence_test]
        return JsonResponse(tokens_and_pos_list, safe=False)


# import re
# from tkinter.filedialog import askdirectory
# from tkinter import filedialog
# import tkinter
# @login_required
# @csrf_exempt
# def export_data_do(request):
#     # if request.method == 'POST':
#         # data_type=request.POST['data_name']
#         # data_user_name=request.POST['username']
#     data_user_name = request.GET.get('p1')
#     data_type = request.GET.get('p2')
#     data_user_name =re.findall("\'(.*?)\'",data_user_name)[0]
#     response = HttpResponse(content_type='text/plain')
#     response['Content-Disposition'] = 'attachment; filename=my.txt'
#     root = tkinter.Tk()
#     root.withdraw()
#     data_save_path = askdirectory()
#     root.destroy()
#
#     cnx = connect_mysql()  # 连接mysql
#     cus = cnx.cursor()  # 创建一个游标对象    try:
#     cus.execute("select distinct file_name from "+data_user_name+";")
#     data_file_type=cus.fetchall()
#     d_s_p=''
#     if_save_sucess=False
#     try:
#         if data_type=="全部类型":
#             pwd = os.getcwd()
#             file_dir = pwd + '/model_list/'
#             model_list_ = os.listdir(file_dir)
#             model_list = [x.split('.')[0] for x in model_list_]
#             for file_type in data_file_type:
#                 for dt in model_list:
#                     cus.execute(
#                         "SELECT tokens_and_pos FROM " + data_user_name + " WHERE tagged>0 AND tag_type='" + dt + "' AND file_name=" + str(file_type[0]) + ";")
#                     sentences = cus.fetchall()
#                     if len(sentences) > 0:
#                         d_s_p = data_save_path + '/' + str(file_type[0]) + data_user_name + data_type + '_sentences.txt'
#                         with open(d_s_p, 'w', encoding='utf-8') as f:
#                             for x in sentences:
#                                 row_data = ''
#                                 data_string = re.findall(r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M | re.I)
#                                 for y in data_string:
#                                     row_data = row_data + y[0] + '/' + y[1] + ' '
#                                 f.write(row_data + '\n')
#                                 response.write(row_data)
#                             f.close()
#                         if_save_sucess = True
#                         d_s_p=data_save_path
#                     else:
#                         d_s_p = 'no data of the tag_type'
#         else:
#             for file_type in data_file_type:
#                 cus.execute("SELECT tokens_and_pos FROM " + data_user_name + " WHERE tagged>0 AND tag_type='" + data_type + "' AND file_name="+str(file_type[0])+";")
#                 sentences = cus.fetchall()
#                 if len(sentences)>0:
#                     d_s_p = data_save_path + '/' +str(file_type[0])+ data_user_name + data_type + '_sentences.txt'
#                     with open(d_s_p, 'w', encoding='utf-8') as f:
#                         for x in sentences:
#                             row_data=''
#                             data_string=re.findall( r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M|re.I)
#                             for y in data_string:
#                                 row_data = row_data +y[0]+'/'+y[1]+' '
#                             f.write(row_data+'\n')
#                             response.write(row_data)
#                         f.close()
#                     if_save_sucess = True
#                 else:
#                     d_s_p='no data of the tag_type'
#
#         message=[if_save_sucess,d_s_p]
#         return response.write(row_data)
#         # return JsonResponse(message, safe=False)
#     except:
#         if_save_sucess = False
#         message = [if_save_sucess,d_s_p ]
#         # return JsonResponse(message, safe=False)










from django.utils.encoding import escape_uri_path
from django.http import HttpResponse
import re
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import tkinter
@login_required
@csrf_exempt
def export_data_do(request):

    data_user_name = request.GET.get('p1')
    data_type = request.GET.get('p2')
    file_name = 'data_file.txt'


    cnx = connect_mysql()  # 连接mysql
    cus = cnx.cursor()  # 创建一个游标对象    try:
    cus.execute("select distinct file_name from "+data_user_name+";")
    data_file_type=cus.fetchall()
    d_s_p=''
    if_save_sucess=False
    content=''
    response = HttpResponse(content, content_type='application/octet-stream')
    try:
        if data_type=="全部类型":
            pwd = os.getcwd()
            file_dir = pwd + '/model_list/'
            model_list_ = os.listdir(file_dir)
            model_list = [x.split('.')[0] for x in model_list_]
            for file_type in data_file_type:
                for dt in model_list:
                    cus.execute(
                        "SELECT tokens_and_pos FROM " + data_user_name + " WHERE tagged>0 AND tag_type='" + dt + "' AND file_name=" + str(file_type[0]) + ";")
                    sentences = cus.fetchall()
                    file_name=data_user_name+str(file_type[0])+dt+".txt"
                    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
                        escape_uri_path(file_name))

                    if len(sentences) > 0:

                        for x in sentences:
                            row_data = ''
                            data_string = re.findall(r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M | re.I)
                            for y in data_string:
                                row_data = row_data + y[0] + '/' + y[1] + ' '
                            response.write(row_data + '\n')
                        if_save_sucess = True
                    else:
                        d_s_p = 'no data of the tag_type'
        else:
            for file_type in data_file_type:
                cus.execute("SELECT tokens_and_pos FROM " + data_user_name + " WHERE tagged>0 AND tag_type='" + data_type + "' AND file_name="+str(file_type[0])+";")
                sentences = cus.fetchall()

                file_name = data_user_name + str(file_type[0]) + data_type + ".txt"
                response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
                    escape_uri_path(file_name))
                if len(sentences)>0:
                    content=''
                    for x in sentences:
                        row_data=''
                        data_string=re.findall( r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M|re.I)
                        for y in data_string:
                            row_data = row_data +y[0]+'/'+y[1]+' '
                        response.write(row_data + '\n')
                    if_save_sucess = True
                else:
                    d_s_p='no data of the tag_type'

        return response
    except:
        if_save_sucess = False
        response.status_code=500
        return response









import MySQLdb


def connect_mysql():
    db_config = dict(host="127.0.0.1", port=3306, db="name", charset="utf8", user="root", passwd="123456")
    try:
        cnx = MySQLdb.connect(**db_config)
    except Exception as err:
        raise err
    return cnx








db_config = dict(host="127.0.0.1", port=3306, db="name", charset="utf8", user="root", passwd="123456")
try:
    cnx = MySQLdb.connect(**db_config)
except Exception as err:
    raise err
cus = cnx.cursor()  # 创建一个游标对象    try:


create_sql="""
CREATE TABLE `name`.%s (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_changed_time` datetime NOT NULL,
  `changed_times` int(11) NOT NULL,
  `text` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tokens_and_pos` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tagged` tinyint(1) NOT NULL,
  `checked` tinyint(1) NOT NULL,
  `last_changed_by_id` int(11) NOT NULL,
  `tag_type` varchar(255)  NOT NULL DEFAULT 0,
  `file_name` varchar(255)  NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`,`tag_type`) USING BTREE
);
"""
#CHARACTER SET utf8 COLLATE utf8_general_ci





from django.utils.encoding import escape_uri_path
from django.http import HttpResponse

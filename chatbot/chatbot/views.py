import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time

# from PosTagging.forms import UserForm
from tagging.models import Sentence, UserProfile
import random

# tag type
# 词性标注:PosTagging_sentencetest
# 实体标注:tagging_sentence
# tag_type_list=['tagging_sentence','PosTagging_sentencetest']

global check_num
check_num=0

def super_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)


        if user:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect('/destribution/')
            else:
                login_message="Your Tagging super user account is disabled."
                return render(request, 'super/superlogin.html', {'login_message':login_message})
        else:
            login_message="Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'super/superlogin.html', {'login_message':login_message})
    else:
        login_message='login error'
        return render(request, 'super/superlogin.html', {'login_message':login_message})


@login_required
def destribution(request):
    destribution_if = False
    destribution_message=''
    task_executor=''
    if request.user.is_superuser:
        if request.method == 'POST':
            destribution_form = request.POST
            user_name_list_ = list(models.User.objects.all().values_list('username'))
            user_name_list = [str(list(i)[0]) for i in user_name_list_]
            if destribution_form['executor'] in user_name_list:
                tag_name=destribution_form['labeltype'].replace(' ', '')
                if tag_name :
                    cnx = connect_mysql()  # 连接mysql
                    cus = cnx.cursor()  # 创建一个游标对象    try:
                    cus.execute('SELECT MIN(id) FROM tagging_sentence;')
                    id_list_start = int(cus.fetchall()[0][0])
                    cus.execute('SELECT MAX(id) FROM tagging_sentence;')
                    id_list_end = int(cus.fetchall()[0][0])
                    if int(destribution_form['missionvolumestart']) >= id_list_start and int(destribution_form['missionvolumeend']) <= id_list_end:
                        task_executor = destribution_form['executor']
                        try:
                            cus.execute(
                                """INSERT INTO """+destribution_form['executor']+""" (id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id,tag_type,file_name) SELECT id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id,tag_type,file_name FROM tagging_sentence WHERE id BETWEEN """+str(destribution_form['missionvolumestart'])+""" AND """ +str(destribution_form['missionvolumeend'])+""";"""
                                        )
                            cus.execute("""UPDATE """+destribution_form['executor']+""" SET tag_type='"""+tag_name+"""' WHERE id BETWEEN """+destribution_form['missionvolumestart']+ """ AND """+destribution_form['missionvolumeend']+""" ;""")
                            cus.execute("FLUSH PRIVILEGES;")
                            cus.close()
                            cnx.commit()
                            destribution_if = True
                            global C_R
                            C_R={}
                            global seen_result
                            seen_result=False
                        except Exception as err:
                            destribution_message = '存在重复分配,已为您忽略!'
                            cnx.rollback()
                            try:
                                cus.execute(
                                    """ INSERT IGNORE INTO """ + destribution_form['executor'] + """ (id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id,tag_type,file_name) SELECT id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id,tag_type ,file_name FROM tagging_sentence WHERE id BETWEEN """ + destribution_form['missionvolumestart']+ """ AND """ + destribution_form['missionvolumeend'] + """;"""
                                )
                                cus.execute("""UPDATE IGNORE """+destribution_form['executor']+""" SET tag_type='"""+tag_name+"""' WHERE tag_type=0 AND (id BETWEEN """+destribution_form['missionvolumestart']+ """ AND """+destribution_form['missionvolumeend']+""");""")
                                cus.execute("""DELETE FROM """+destribution_form['executor']+""" WHERE tag_type = '0';""")
                                cus.execute("FLUSH PRIVILEGES;")
                                cus.close()
                                cnx.commit()
                                destribution_if = True
                                # global C_R
                                C_R = {}
                                # global seen_result
                                seen_result = False
                            except :
                                destribution_message='分配失败!'
                                cnx.close()
                        #     # raise err
                        # finally:
                        #     destribution_if = False
                        #     destribution_message = '分配失败!'
                        #     task_status = {}
                        #     cnx.close()

                    else:
                        task_executor = ''
                        destribution_message = destribution_message + 'Out of sentence range:'+str(id_list_start)+'-----'+str(id_list_end)+'.'

                else:
                    task_executor = ''
                    destribution_message = destribution_message + destribution_form['labeltype']+'tag type does not exist! '
            else:
                task_executor=destribution_form['executor']
                if task_executor == '':
                    destribution_message = '请填写完整信息! '
                else:
                    destribution_message=destribution_message+'executor user does not exist! '
        else:
            destribution_form=[]
            task_executor = ''
        return render(request,
                      'super/destribution.html',
                      {'destribution_form': destribution_form, 'destribution_if': destribution_if,'destribution_message':destribution_message,
                       'task_executor':task_executor})
    else:
        destribution_message='你不是管理员，不能分配任务！'
        return render(request,
                      'super/destribution.html',
                      { 'destribution_if': destribution_if,
                       'destribution_message': destribution_message,
                       'task_executor': request.user.username})





@login_required
def SuperUserCheck(request):
    start_check=False
    check_message=''
    try:
        examined_person=request.POST['examined']
    except:
        examined_person=''
        return render(request, 'super/SuperUserCheck.html', {
            'check_message': check_message, 'examined_person': examined_person, 'start_check': start_check

        })
    if examined_person:
        user_name_list_ = list(models.User.objects.all().values_list('username'))
        user_name_list = [str(list(i)[0]) for i in user_name_list_]
        if examined_person in user_name_list:
            check_sents_num = int(request.POST['examined_sents_num'])
            if check_sents_num>0:
                start_check = True
                global check_num
                check_num = check_sents_num
                # cnx = connect_mysql()  # 连接mysql
                # cus = cnx.cursor()  # 创建一个游标对象    try:
                # cus.execute("""SELECT id FROM tagging_sentence WHERE tag_type='"""++"""';""")
            else:
                check_message = '请填写检查句子的数量!'
        else:
            check_message = '请填写要检查的人!'
    else:
        check_message='用户不存在!'
    return render(request, 'super/SuperUserCheck.html', {
        'check_message': check_message, 'examined_person': examined_person, 'start_check': start_check

    })


def back_check(request):
    check_message=''
    examined_person=''
    start_check=False
    return render(request, 'super/SuperUserCheck.html', {
        'check_message': check_message, 'examined_person': examined_person, 'start_check': start_check

    })


@login_required
@csrf_exempt
def all_data_source(request):
    if request.method == 'POST':
        cnx = connect_mysql()  # 连接mysql
        cus = cnx.cursor()  # 创建一个游标对象    try:
        cus.execute("select distinct file_name from tagging_sentence;")
        data_source = cus.fetchall()
        data_source_list=[]
        if len(data_source)>0:
            for i in data_source:
                data_source_list.append(str(i[0]))
        else:
            data_source_list=False
        return JsonResponse(data_source_list, safe=False)


import re
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import tkinter
# @login_required
# @csrf_exempt
# def export_data_from_database(request):
#     if request.method == 'POST':
#         data_source_selected = request.POST['data_source_selected']
#         data_tag_type_selected = request.POST['data_tag_type_selected']
#         root = tkinter.Tk()
#         root.withdraw()
#         data_save_path = askdirectory()
#         root.destroy()
#         d_s_p = ''
#         try:
#             cnx = connect_mysql()  # 连接mysql
#             cus = cnx.cursor()  # 创建一个游标对象    try:
#             cus.execute(
#                 "SELECT tokens_and_pos FROM tagging_sentence WHERE checked>0 AND tag_type='" + data_tag_type_selected + "' AND file_name=" +data_source_selected+ ";"
#             )
#             sentences = cus.fetchall()
#
#             if_save_sucess = False
#
#             if len(sentences) > 0:
#                 d_s_p = data_save_path + '/' +data_source_selected+ '_'+data_tag_type_selected+'_sentences.txt'
#                 with open(d_s_p, 'w', encoding='utf-8') as f:
#                     for x in sentences:
#                         row_data = ''
#                         data_string = re.findall(r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M | re.I)
#                         for y in data_string:
#                             row_data = row_data + y[0] + '/' + y[1] + ' '
#                         f.write(row_data + '\n')
#                     f.close()
#                 if_save_sucess = True
#                 d_s_p = data_save_path
#             else:
#                 d_s_p = 'no data'
#
#             message = [if_save_sucess, d_s_p]
#             return JsonResponse(message, safe=False)
#         except:
#             if_save_sucess = False
#             message = [if_save_sucess, d_s_p]
#             return JsonResponse(message, safe=False)

from django.utils.encoding import escape_uri_path
from django.http import HttpResponse
@login_required
@csrf_exempt
def export_data_from_database(request):
    data_source_selected = request.GET.get('p1')
    data_tag_type_selected = request.GET.get('p2')
    file_name = 'data_file.txt'

    cnx = connect_mysql()  # 连接mysql
    cus = cnx.cursor()  # 创建一个游标对象    try:
    d_s_p = ''
    if_save_sucess = False
    content = ''
    response = HttpResponse(content, content_type='application/octet-stream')

    try:
        cnx = connect_mysql()  # 连接mysql
        cus = cnx.cursor()  # 创建一个游标对象    try:
        cus.execute(
            "SELECT tokens_and_pos FROM tagging_sentence WHERE checked>0 AND tag_type='" + data_tag_type_selected + "' AND file_name=" +data_source_selected+ ";"
        )
        sentences = cus.fetchall()

        if_save_sucess = False

        if len(sentences) > 0:
            file_name = data_source_selected+ '_'+data_tag_type_selected+'_sentences.txt'
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
                escape_uri_path(file_name))
            for x in sentences:
                row_data = ''
                data_string = re.findall(r': \"(.*?)\", \"pos\": \"(.*?)\"}', x[0], re.M | re.I)
                for y in data_string:
                    row_data = row_data + y[0] + '/' + y[1] + ' '
                response.write(row_data + '\n')
            if_save_sucess = True
        else:
            d_s_p = 'no data'

        return response
    except:

        if_save_sucess = False
        response.status_code=500
        return response






@login_required
@csrf_exempt
def ajax_for_tokens_list(request):
    if request.method == 'POST':
        username = request.POST['username']
        tag_model_name = request.POST['tag_model_name']
        examined_person = request.POST['examined_person']
        # current_user = User.objects.filter(username=username)[0]
        # user_profile = UserProfileTest.objects.filter(user=current_user)[0]
        cus.execute("SELECT * FROM %s WHERE checked=0 and tag_type='%s';" % (examined_person,tag_model_name))
        sent_list = cus.fetchall()
        global check_num
        if len(sent_list)>check_num:
            if sent_list:
                # global check_num
                if check_num > 0 and check_num >= 5:
                    sentence_test = random.sample(sent_list, 5)
                    check_num = check_num - 5
                elif check_num >0 and check_num < 5:
                    sentence_test = random.sample(sent_list, check_num)
                    check_num = 0
                else:
                    sentence_test = []
            else:
                sentence_test = []
        else:
            sentence_test = []
        tokens_and_pos_list = [{'id': sent[0], 'tokens_and_pos': json.loads(sent[4])} for sent in sentence_test]
        return JsonResponse(tokens_and_pos_list, safe=False)



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









import datetime
@login_required
@csrf_exempt
def ajax_for_save_tagged_tokens(request):
    if request.method == 'POST':
        data = json.loads(request.POST['taggedResult'])
        tag_model_name = request.POST['tag_model_name']
        username = data['username']
        examined_person = request.POST['examined_person']
        sents = data['sents']
        current_user = User.objects.filter(username=username)[0]
        # cnx = connect_mysql()  # 连接mysql
        # cus = cnx.cursor()  # 创建一个游标对象    try:
        for sent in sents:
            sent_id = sent['id']
            # current_sent = Sentence.objects.filter(id=sent_id)[0]
            last_changed_by_id = current_user
            tokens_and_pos = json.dumps(sent['tagged'], ensure_ascii=False)
            checked = True
            last_changed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # current_sent.save()
            try:
                # cus.execute("""INSERT INTO %s(id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by,tag_type)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1)"""
                #             %(username,sent_id,current_sent.pt_last_changed_time,current_sent.changed_times,current_sent.text,current_sent.tokens_and_pos,current_sent.tagged,current_sent.checked,current_sent.last_changed_by.id))
                cus.execute(
                    """UPDATE """ + examined_person + """ SET last_changed_time='{last_changed_time}',changed_times=changed_times+1,tokens_and_pos='{tokens_and_pos}',tagged=True,checked='{checked}',last_changed_by_id='{last_changed_by_id}' WHERE id='{id}' AND tag_type='{tag_type}';"""
                    .format(last_changed_time=last_changed_time,
                            tokens_and_pos=tokens_and_pos,
                            checked=int(checked), last_changed_by_id=current_user.id, id=sent_id, tag_type=tag_model_name)
                    )
            except Exception as err:
                cnx.rollback()
                raise err
            finally:
                # cnx.close()
                pass
            # else:
            #     # forget_tag_sents_id_list.append(sent_id)
        # cus.close()
        cnx.commit()
        cus.execute("SELECT * FROM %s WHERE checked=0 and tag_type='%s';" % (examined_person, tag_model_name))
        sent_tupl=cus.fetchall()
        if sent_tupl:
            global check_num
            if check_num > 0 and check_num >= 5:
                sentence_test = random.sample(sent_tupl, 5)
                check_num = check_num - 5
            elif check_num > 0 and check_num < 5:
                sentence_test = random.sample(sent_tupl, check_num)
                check_num = 0
            else:
                sentence_test = []
        else:
            sentence_test = []
        tokens_and_pos_list = [{'id': sent[0], 'tokens_and_pos': json.loads(sent[4])} for sent in sentence_test]
        # UserProfileTest.objects.select_for_update().filter(user_id=current_user.id).update(sentence_id=sents[-1]['id'] + 1)
        # user_profile = UserProfileTest.objects.filter(user=current_user)[0]

        return JsonResponse(tokens_and_pos_list, safe=False)


from django.shortcuts import render_to_response
global C_R
C_R={}




@login_required
@csrf_exempt
def check_result(request):
    if request.method == 'POST':
        data = json.loads(request.POST['CheckResult'])
        e_r=int(data['red_num']) / int(data['all_num'])
        Error_rate = '{:.3%}'.format(e_r)
        check_message="可供修改的地方为:'{all_num}'，修改处为:'{red_num}'，修改率为:'{Error_rate}'。 检查人：'{checker}',标注人:'{tagger}'。".format(
            all_num=data['all_num'],red_num=data['red_num'],Error_rate=Error_rate,checker=data['checker'],tagger=data['examined_person'],
        )
        global C_R
        C_R['check_message']=check_message
        C_R['all_num'] = data['all_num']
        C_R['red_num'] = data['red_num']
        C_R['checker'] = data['checker']
        C_R['tag_person'] = data['examined_person']
        return JsonResponse(check_message,safe=False)


@login_required
@csrf_exempt
def seen_result_html(request):
    global C_R
    return render(request, 'super/CheckResult.html', {
        'check_message': C_R['check_message'],'checker': C_R['checker'],'tag_person' : C_R['tag_person'],
    })


@login_required
@csrf_exempt
def passcheck(request):
    message = False
    examined_person = request.POST['examined_person']
    try:
        cus.execute("""REPLACE INTO tagging_sentence (id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id ,tag_type,file_name) 
        SELECT id,last_changed_time,changed_times,text,tokens_and_pos,tagged,checked,last_changed_by_id ,tag_type ,file_name FROM """ +examined_person+""" WHERE tagged=1;""")
        cus.execute("""UPDATE IGNORE tagging_sentence SET checked=1 WHERE tagged=1;""")
        # cus.execute("""DELETE FROM """+examined_person+""" WHERE tagged=1;""")
        cnx.commit()
        cnx.rollback()
        message=True
    except Exception as err:
        cnx.rollback()
        raise err

    return JsonResponse(message, safe=False)



@login_required
@csrf_exempt
def no_pass(request):
    message = False
    examined_person = request.POST['examined_person']
    try:
        cus.execute("""UPDATE IGNORE """+examined_person+""" SET tagged=0 WHERE tagged=1 AND checked=0;""")
        cnx.commit()
        cnx.rollback()
        message = True
    except Exception as err:
        cnx.rollback()
        raise err

    return JsonResponse(message, safe=False)














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


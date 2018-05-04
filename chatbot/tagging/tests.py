import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")
from django.conf import settings

import sys;
sys.path.append("/path/chatbot")

import django

django.setup()

import json
from tagging.models import Sentence
from django.contrib.auth.models import User


def populate():
    populate_text = """
    君不见，黄河之水天上来，奔流到海不复回。
    君不见，高堂明镜悲白发，朝如青丝暮成雪！
    人生得意须尽欢，莫使金樽空对月。
    天生我材必有用，千金散尽还复来。
    烹羊宰牛且为乐，会须一饮三百杯。
    岑夫子，丹丘生，将进酒，杯莫停。
    与君歌一曲，请君为我倾耳听。
    钟鼓馔玉不足贵，但愿长醉不复醒。
    古来圣贤皆寂寞，惟有饮者留其名。
    陈王昔时宴平乐，斗酒十千恣欢谑。
    主人何为言少钱，径须沽取对君酌。
    五花马、千金裘，呼儿将出换美酒，与尔同销万古愁！
    """

    user = User.objects.filter(username='name')[0]
    text_list = [seg.strip() for seg in populate_text.split('\n') if len(seg.strip()) > 0]
    Sentence.objects.all().delete()
    for seg in text_list:
        tokens_and_pos = [{'token': token} for token in seg]
        sent = Sentence.objects.get_or_create(last_changed_by_id=user, text=seg, tagged=False,
                                              tokens_and_pos=json.dumps(tokens_and_pos, ensure_ascii=False))[0]
        sent.save()
    # print(len(text_list))


def insert_people_daily_data():
    Sentence.objects.all().delete()
    user = User.objects.filter(username='name')[0]
    with open('../ten_thousand_sentences.txt', 'r', encoding='utf-8') as f:
        sent_ends = set(['。', '！', '？', '?', '!', '.', '……'])
        for line in f.readlines():
            tokens = line.strip().split(' ')[1:]
            tokens_and_pos = []
            for token in tokens:
                segs = token.split('/')
                if len(segs) == 2:
                    tokens_and_pos.append({'token': segs[0],'pos':segs[1]})
                    # if segs[1].startswith('w') and segs[0] in sent_ends:
                    #     add_sent(tokens_and_pos, user)
                    #     tokens_and_pos = []
            if len(tokens_and_pos) > 0:
                add_sent(tokens_and_pos, user)


def add_sent(tokens_and_pos, user):
    text = "".join([x['token'] for x in tokens_and_pos])
    sent = Sentence.objects.get_or_create(last_changed_by=user, text=text, tagged=False,
                                          tokens_and_pos=json.dumps(tokens_and_pos, ensure_ascii=False))[0]
    sent.save()

# for sent in Sentence.objects.filter(checked=False):
#     tokens = [x for x in sent.text]
#     sent.tokens = json.dumps(tokens, ensure_ascii=False)
#     sent.save()

if __name__ == '__main__':
    # populate()
    # insert_people_daily_data()
    # import jieba
    # test_text = """19980101-01-002-003/m 刚刚/d 过去/v 的/u 一/m 年/q ，/w 大气磅礴/i ，/w 波澜壮阔/i 。/w 在/p 这/r 一/m 年/q ，/w 以/p 江/nr 泽民/nr 同志/n 为/v 核心/n 的/u 党中央/nt ，/w 继承/v 邓/nr 小平/nr 同志/n 的/u 遗志/n ，/w 高举/v 邓小平理论/n 的/u 伟大/a 旗帜/n ，/w 领导/v 全党/n 和/c 全国/n 各族/r 人民/n 坚定不移/i 地/u 沿着/p 建设/v 有/v 中国/ns 特色/n 社会主义/n 道路/n 阔步/d 前进/v ，/w 写/v 下/v 了/u 改革/v 开放/v 和/c 社会主义/n 现代化/vn 建设/vn 的/u 辉煌/a 篇章/n 。/w 顺利/a 地/u 恢复/v 对/p 香港/ns 行使/v 主权/n ，/w 胜利/v 地/u 召开/v 党/n 的/u 第十五/m 次/q 全国/n 代表大会/n ———/w 两/m 件/q 大事/n 办/v 得/u 圆满/a 成功/a 。/w 国民经济/n 稳中求进/l ，/w 国家/n 经济/n 实力/n 进一步/d 增强/v ，/w 人民/n 生活/vn 继续/v 改善/v ，/w 对外/vn 经济/n 技术/n 交流/vn 日益/d 扩大/v 。/w 在/p 国际/n 金融/n 危机/n 的/u 风浪/n 波及/v 许多/m 国家/n 的/u 情况/n 下/f ，/w 我国/n 保持/v 了/u 金融/n 形势/n 和/c 整个/b 经济/n 形势/n 的/u 稳定/a 发展/vn 。/w 社会主义/n 精神文明/n 建设/vn 和/c 民主/a 法制/n 建设/vn 取得/v 新/a 的/u 成绩/n ，/w 各项/r 社会/n 事业/n 全面/ad 进步/v 。/w 外交/n 工作/vn 取得/v 可喜/a 的/u 突破/vn ，/w 我国/n 的/u 国际/n 地位/n 和/c 国际/n 威望/n 进一步/d 提高/v 。/w 实践/v 使/v 亿万/m 人民/n 对/p 邓小平理论/n 更加/d 信仰/v ，/w 对/p 以/p 江/nr 泽民/nr 同志/n 为/v 核心/n 的/u 党中央/nt 更加/d 信赖/v ，/w 对/p 伟大/a 祖国/n 的/u 光辉/n 前景/n 更加/d 充满/v 信心/n 。/w """
    # tokens = test_text.strip().split(' ')[1:]
    # sent = ''
    # for token in tokens:
    #     segs = token.split('/')
    #     if len(segs) == 2:
    #         sent += segs[0]
    # print(sent)
    # print('/ '.join(jieba.cut(sent)))

    # for index, number in enumerate([1, 2, 3]):
    #     print(index, number)
    # from tkinter
    # filename = tkinter.filedialog.askopenfilename(initialdir='C:/Users/feng/Desktop/computer计算机网络资料')
    # print(filename)












#     # import MySQLdb
# import pymysql
#
# def connect_mysql():
#     db_config = dict(host="127.0.0.1", port=3306, db="name", charset="utf8", user="root", passwd="namenlp")
#     try:
#         cnx = pymysql.connect(**db_config)
#     except Exception as err:
#         raise err
#     return cnx
#
#
# db_config = dict(host="127.0.0.1", port=3306, db="name", charset="utf8", user="root", passwd="namenlp")
# try:
#     cnx = pymysql.connect(**db_config)
# except Exception as err:
#     raise err
# cus = cnx.cursor()  # 创建一个游标对象    try:
# print('111111111111111')
#
#
#








    #
    # import re
    # tag_set=set()
    # with open('../199801.txt', 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         tag=re.findall('[a-zA-Z]{1,2}', line)
    #         for i in tag:
    #             tag_set.add(i)
    # print(tag_set)
    # tag_set=json.dumps(list(tag_set))
    # print(tag_set)
    #
    #
    # def write_txt(data):
    #     try:
    #         # json_stream = get_txt_stream(data)
    #         response = HttpResponse(content_type='text/plain')
    #         from urllib import parse
    #         response['Content-Disposition'] = 'attachment;filename=my.txt'
    #         response.write(data)
    #         return response
    #     except Exception as e:
    #         print(e)
    #
    #
    # def get_txt_stream(data):
    #     # 开始这里我用ByteIO流总是出错，但是后来参考廖雪峰网站用StringIO就没问题
    #     file = StringIO()
    #     data = json.dumps(data)
    #     file.write(data)
    #     res = file.getvalue()
    #     file.close()
    #     return res
    import MySQLdb



    from django.shortcuts import HttpResponse
    from io import StringIO, BytesIO
    from MySQLdb.cursors import DictCursor
    import re

    db_config = dict(host="127.0.0.1", port=3306, db="name", charset="utf8", user="root", passwd="123456")
    try:
        cnx = MySQLdb.connect(**db_config)
    except Exception as err:
        raise err
    cus = cnx.cursor()

    # from download.core import FileHandle


    sql = 'select tokens_and_pos from dong'

    cus.execute(sql)  # 执行sql语句
    result=cus.fetchall()  # 获取查询结果
    response =  HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=my.txt'

    row = 1
    for list in result:
        row_data = ''
        data_string = re.findall(r': \"(.*?)\", \"pos\": \"(.*?)\"}', list[0], re.M | re.I)
        for y in data_string:
            row_data = row_data + y[0] + '/' + y[1] + ' '
        # write_txt(row_data + '\n')
        response.write( list[0]+"\n")

    # output = StringIO()
    # output.seek(0)
    # print(output.getvalue())
    # print(response)



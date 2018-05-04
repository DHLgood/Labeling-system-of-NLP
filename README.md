# Labeling-system-of-NLP
本标注系统用于nlp中的词性标注、实体标注等，根据标注类型的配置文件生成不同标注类型。
>- Django 2.0.3
>- Python 3.6
>- mysql 5.7.21
运行环境
chrome/firefox 等主流浏览器


总体结构
├───chatbot                    # 标注管理app
│    ├───settings.py
│    ├───urls.py
│    ├───view.py 
│    ├───wsgi.py 
├───media              #标注图标等图片文件夹
├───model_list         #标注模式配置文件所在文件夹目录
├───static             #js css bootstrap等文件
├───tagging            用户标注app
│    ├───models.py
│    ├───urls.py
│    ├───views.py
├───templates               # Django 标注静态文件目录 模板视图(*.html)
│    ├───super              #管理员静态文件目录
│    ├───tagging            #用户标注静态文件目录
├───chatbot_nginx.conf               #标注系统nginx配置文件
├───uwsgi_params                     #标注系统uwsgi配置文件
├───uwsgi.ini                     #标注系统部署文件
└───manage.py 

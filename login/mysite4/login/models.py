#coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django import forms
from django.contrib import admin
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')
    
#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码 ',widget=forms.PasswordInput())


cpunum_choice = ( 
    ('', u"---------"), 
    (2, u"2"),         
    (4, u"4"),         
    (8, u"8"), 
    (16, u"16"), 
)

CONSULTANT_CHOICES = (
            ('', u"所有"),
            ('1', u"顾问"),         
            ('0', u"非顾问"),       
    )
ORDER_CHOICES = (
            ('', u"所有"),
            ('1', u"已下单"),         
            ('0', u"未下单"),       
    )
CITY_CHOICES = (
            (''                ,'所有'             ),
            ('北京市'          ,'北京市'           ),
            ('天津市'          ,'天津市'           ),
            ('上海市'          ,'上海市'           ),
            ('重庆市'          ,'重庆市'           ),
            ('河北省'          ,'河北省'           ),
            ('山西省'          ,'山西省'           ),
            ('台湾省'          ,'台湾省'           ),
            ('辽宁省'          ,'辽宁省'           ),
            ('吉林省'          ,'吉林省'           ),
            ('黑龙江省'        ,'黑龙江省'         ),
            ('江苏省'          ,'江苏省'           ),
            ('浙江省'          ,'浙江省'           ),
            ('安徽省'          ,'安徽省'           ),
            ('福建省'          ,'福建省'           ),
            ('江西省'          ,'江西省'           ),
            ('山东省'          ,'山东省'           ),
            ('河南省'          ,'河南省'           ),
            ('湖北省'          ,'湖北省'           ),
            ('湖南省'          ,'湖南省'           ),
            ('广东省'          ,'广东省'           ),
            ('甘肃省'          ,'甘肃省'           ),
            ('四川省'          ,'四川省'           ),
            ('山东省'          ,'山东省'           ),
            ('贵州省'          ,'贵州省'           ),
            ('海南省'          ,'海南省'           ),
            ('云南省'          ,'云南省'           ),
            ('青海省'          ,'青海省'           ),
            ('陕西省'          ,'陕西省'           ),
            ('广西壮族自治区'  ,'广西壮族自治区'   ),
            ('西藏自治区'      ,'西藏自治区'       ),
            ('宁夏回族自治区'  ,'宁夏回族自治区'   ),
            ('新疆维吾尔自治区','新疆维吾尔自治区' ),
            ('内蒙古自治区'    ,'内蒙古自治区'     ),
            ('澳门特别行政区'  ,'澳门特别行政区'   ),
            ('香港特别行政区'  ,'香港特别行政区'   ),      
    )
 
class QueryForm(forms.Form):
    consultant = forms.ChoiceField(label=u'顾问',widget=forms.RadioSelect, choices=CONSULTANT_CHOICES,required=False,initial = '') 
    order      = forms.ChoiceField(label=u'下单',widget=forms.RadioSelect, choices=ORDER_CHOICES,required=False,initial = '')
    city       = forms.ChoiceField(label=(u"省份"),widget=forms.Select, choices=CITY_CHOICES,required=False,initial = '')
    depth      = forms.IntegerField(label=(u"转发传播深度前几？"),min_value=0,max_value=5,required=False)
    span       = forms.IntegerField(label=(u"转发传播广度前几？"),min_value=0,max_value=5,required=False)
    shareid    = forms.CharField(max_length=100 ,label='查找指定ShareID:',required=False,initial = ' ')
    #timestart  = forms.DateTimeField(required=True,label='时间',widget=widgets.AdminDateWidget())

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'consultant',
        'order',
        Field('city', css_class='input-medium'),
        Field('depth', css_class='input-medium'),
        Field('span', css_class='input-medium'),
        FormActions(
            Submit('query', '条件查询', css_class="btn-primary"),
            Submit('cityDiff', '省份趋势图'),
            Submit('ageDiff', '年龄趋势图'),
            Submit('timeDiff', '日期趋势图'),
        ),
        Field('shareid', css_class='input-xlarge'),
        FormActions(
            Submit('shareId', '精确查找', css_class="btn-primary"),
        ),
    )




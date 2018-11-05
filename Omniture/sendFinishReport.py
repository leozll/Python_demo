#  -*-  coding:  UTF-8  -*-
import sendEmailFunc as sef
import datetime

to_list=['leo.zhai@bizfocus.cn']                      #收件人(列表)
sub='Omniture finished at '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')                    #邮件名
print datetime.datetime.now()

#sef.send_mail()
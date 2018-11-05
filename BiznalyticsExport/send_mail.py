#  -*-  coding:  UTF-8  -*-
import sqlite3
import cx_Oracle
import xlwt
import smtplib
import datetime
import time
from  email.mime.text  import  MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def sqlite_query(file_name,query_sql):
    con = sqlite3.connect(sqlite3_file)
    cur = con.cursor()
    cur.execute(query_sql)
    return cur.fetchall()

def oracle_query(con_string,query_sql):
    conn = cx_Oracle.connect(con_string)
    c = conn.cursor()
    x = c.execute(query_sql)
    conn.commit()
    return (x.fetchall(),x.rowcount,x.description)
    #return x


def query_to_workbook_title(ws,sql_cursor,row_start):
    global data_length
    global title_start
    pattern= xlwt.Pattern()  # Create the Pattern
    pattern.pattern_fore_colour = 1
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    style = xlwt.XFStyle()  # Create the Pattern
    style.pattern = pattern  # Add Pattern to Style
    for i in xrange(0,100):
        for j in xrange(0,20):
            ws.write(i, j, '', style)

    alignment4 = xlwt.Alignment()
    alignment4.horz = xlwt.Alignment.HORZ_CENTER
    font4 = xlwt.Font()
    font4.name = 'Microsoft YaHei'
    font4.bold = 'true'
    font4.colour_index = 0x01 #1=White
    font4.height = 280  #font=14
    pattern4 = xlwt.Pattern()  # Create the Pattern
    pattern4.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern4.pattern_fore_colour = 158
    style4 = xlwt.XFStyle()  # Create the Pattern
    style4.font = font4
    style4.pattern = pattern4  # Add Pattern to Style
    style4.alignment = alignment4
    for colx, heading in enumerate(tuple[0] for tuple in sql_cursor[2]):
        ws.write(row_start-1, colx+2, heading.decode('utf-8'),style4)
        ws.write(row_start-1, 2, u'指标', style4)
        #ws.col(colx+2).width = 6000  # 3333 = 1" (one inch).
        data_length=colx



    borders1 = xlwt.Borders()
    borders1.bottom = xlwt.Borders.MEDIUM
    style.borders = borders1
    for i in xrange(1,data_length+4):
        ws.write(title_start, i, '', style)
    borders2 = xlwt.Borders()
    borders2.left = xlwt.Borders.MEDIUM
    style.borders = borders2
    for i in xrange(1,7):
        ws.write(title_start+i, 1, '', style)
    borders3 = xlwt.Borders()
    borders3.right = xlwt.Borders.MEDIUM
    style.borders = borders3
    for i in xrange(1,7):
        ws.write(title_start+i, data_length+3, '', style)

    font1 = xlwt.Font()
    font1.name = 'Microsoft YaHei'
    font1.bold = 'true'
    font1.colour_index = 0x9e #158
    font1.height = 360  #font=18

    style1 = xlwt.XFStyle()  # Create the Pattern
    style1.font = font1
    style1.alignment = alignment4
    #style1.borders = borders
    style1.pattern = pattern
    ws.write_merge(title_start+2, title_start+2, 2, data_length+2, u'东亚携程联名信用卡业务数据日报',style1)


    font2 = xlwt.Font()
    font2.name = 'Microsoft YaHei'
    font2.colour_index = 0x9f #158
    font2.height = 320  #font=16
    style2 = xlwt.XFStyle()  # Create the Pattern
    style2 = xlwt.XFStyle()  # Create the Pattern
    style2.font = font2
    style2.alignment = alignment4
    #style2.borders = borders
    style2.pattern = pattern
    ws.write_merge(title_start+3, title_start+3, 2, data_length+2, u'信用卡事业部',style2)

    font3 = xlwt.Font()
    font3.name = 'Microsoft YaHei'
    font3.bold = 'true'
    font3.colour_index = 0x17 #23
    font3.height = 240  #font=12
    alignment3 = xlwt.Alignment()
    alignment3.horz = xlwt.Alignment.HORZ_RIGHT
    style3 = xlwt.XFStyle()  # Create the Pattern
    style3.font = font3
    style3.alignment = alignment3
    #style3.borders = borders
    style3.pattern = pattern
    time_string=datetime.datetime.now().strftime('%Y年%m月%d日').decode('utf-8')
    ws.write_merge(title_start+4, title_start+4, 2, data_length+2, time_string,style3)
    #ws.insert_bitmap('./bea.bmp', 1, 1,0,0,scale_x=1, scale_y=1)



def query_to_workbook(ws,sql_cursor,row_start):
    global data_length
    style9 = xlwt.XFStyle()
    borders2 = xlwt.Borders()
    borders2.left = xlwt.Borders.MEDIUM
    pattern9 = xlwt.Pattern()  # Create the Pattern
    pattern9.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern9.pattern_fore_colour = 1
    style9.borders = borders2
    style9.pattern = pattern9

    style10 = xlwt.XFStyle()
    borders3 = xlwt.Borders()
    borders3.right = xlwt.Borders.MEDIUM
    pattern10 = xlwt.Pattern()  # Create the Pattern
    pattern10.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern10.pattern_fore_colour = 1
    style10.borders = borders3
    style10.pattern = pattern10

    style11 = xlwt.XFStyle()
    borders4 = xlwt.Borders()
    borders4.top = xlwt.Borders.MEDIUM
    pattern11 = xlwt.Pattern()  # Create the Pattern
    pattern11.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern11.pattern_fore_colour = 1
    style11.borders = borders4
    style11.pattern = pattern11

    alignment1 = xlwt.Alignment()
    alignment1.horz = xlwt.Alignment.HORZ_CENTER

    font5 = xlwt.Font()
    font5.name = 'Microsoft YaHei'
    font5.bold = 'true'
    font5.height = 240  #font=12
    pattern5 = xlwt.Pattern()  # Create the Pattern
    pattern5.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern5.pattern_fore_colour = 159   
    style5 = xlwt.XFStyle()  # Create the Pattern
    style5.font = font5
    style5.pattern = pattern5  # Add Pattern to Style

    for colx, heading in enumerate(tuple[0] for tuple in sql_cursor[2]):
        ws.write(row_start, colx+2, heading.decode('utf-8'),style5)
        #ws.col(colx + 2).width = 6500  # 3333 = 1" (one inch).#
        ws.col(colx + 2).width = int(20000/(data_length+1.5)*1.5)  # 3333 = 1" (one inch).#
        if colx>0:
            ws.write(row_start, colx + 2, '',style5)
            #ws.col(colx + 2).width = 4000  # 3333 = 1" (one inch).#
            ws.col(colx + 2).width = int(22000/(data_length+1.5))  # 3333 = 1" (one inch).#
        ws.write(row_start, 1, '', style9)
        ws.write(row_start, data_length + 3, '', style10)


    font6 = xlwt.Font()
    font6.name = 'Arial'
    font6.height = 240  #font=12
    pattern6 = xlwt.Pattern()  # Create the Pattern
    pattern6.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern6.pattern_fore_colour = 1
    style6 = xlwt.XFStyle()  # Create the Pattern
    style6.num_format_str = '#,##0'
    style6.font = font6
    style6.alignment = alignment1
    style6.pattern = pattern6
    font7 = xlwt.Font()
    font7.name = 'Microsoft YaHei'
    font7.height = 240  #font=12
    style7 = xlwt.XFStyle()  # Create the Pattern
    style7.font = font7
    style7.pattern = pattern6
    font8 = xlwt.Font()
    font8.name = 'Arial'
    font8.height = 240  #font=12
    style8 = xlwt.XFStyle()  # Create the Pattern
    style8.num_format_str = '0.00%'
    style8.font = font6
    style8.alignment = alignment1
    style8.pattern = pattern6
    for rowy, row in enumerate(sql_cursor[0]):
        for colx, text in enumerate(row):
            #ws.write(row_start+rowy + 1, colx+2, str(text).decode('utf-8'))
            if str(text).isdigit():
                ws.write(row_start + rowy + 1, colx + 2, int(text),style6)
            elif str(text)[0:-1].isdigit() and str(text)[-1]=='%':
                #ws.write(row_start + rowy + 1, colx + 2, str(text).decode('utf-8'),style8)
                ws.write(row_start + rowy + 1, colx + 2, int(str(text)[0:-1])/100, style8)
            else:
                ws.write(row_start + rowy + 1, colx + 2, str(text).decode('utf-8'),style7)
        ws.write(row_start + rowy+1, 1, '', style9)
        ws.write(row_start + rowy+1, data_length + 3, '', style10)
        ws.write(row_start + rowy+2, 1, '', style9)
        ws.write(row_start + rowy+2, data_length + 3, '', style10)

    for i in xrange(1,data_length + 4):
        ws.write(row_start + sql_cursor[1]+2, i, '', style11)
        ws.write(row_start + sql_cursor[1]+2, i, '', style11)
def server_infos():
    #循环邮件发送配置信息，取出数据源和sql(只会有1个数据源和一句sql)
    for info in sqlite_query(sqlite3_file,server_info_sql):
        #连接邮件发送配置信息的sql数据源
        for dbinfo in sqlite_query(sqlite3_file,DB_info_Sql % info[0]):
            con_string1 = '%s/%s@%s:%d/%s' %(dbinfo[2],dbinfo[3],dbinfo[0],dbinfo[4],dbinfo[1])
        #执行邮件发送配置信息的sql（一张报表发送配置是一行结果,可能有多行）
        for server_info in oracle_query(con_string1, info[1])[0]:
            # info_tuple=(mail_host,mail_port,mail_user,mail_pass,)
            info_tuple=(server_info[0],server_info[1],server_info[2])
    return info_tuple
#
def mail_infos():
    info_list=[]
    #循环邮件发送配置信息，取出数据源和sql(只会有1个数据源和一句sql)
    for info in sqlite_query(sqlite3_file,mail_info_sql1):
        #连接邮件发送配置信息的sql数据源
        for dbinfo in sqlite_query(sqlite3_file,DB_info_Sql % info[0]):
            con_string1 = '%s/%s@%s:%d/%s' %(dbinfo[2],dbinfo[3],dbinfo[0],dbinfo[4],dbinfo[1])
        #执行邮件发送配置信息的sql（一张报表发送配置是一行结果,可能有多行）
        for mail_info in oracle_query(con_string1,mail_info_sql2 % info[1])[0]:
            #info_tuple=(report_subject,report_name,schedule,time,mailto_list,)
            info_tuple=(mail_info[0],mail_info[1],mail_info[2],mail_info[3],mail_info[4],mail_info[5])
            info_list.append(info_tuple)
    return info_list

def is_sendmail(mail_info):
    schedule_time = time.strptime(mail_info[4], "%H:%M")
    date_diff = (datetime.datetime.now() - datetime.datetime(*schedule_time[:6])).seconds
    if mail_info[2] == 'daily':
        return 1 if abs(date_diff)<150 else 0
    elif mail_info[2] == 'weekly':
        #如果是星期日（系统默认为0）那么就转为7
        #cur_week=7 if datetime.datetime.now().weekday()==0 else datetime.datetime.now().weekday()
        return 1 if abs(date_diff) < 150 and datetime.datetime.now().weekday()+1 == mail_info[3] else 0
    elif mail_info[2] == 'monthly':
        return 1 if abs(date_diff) < 150 and datetime.datetime.now().strftime('%d').strip('0')==mail_info[3] else 0
    elif mail_info[2] == 'one-time':
        return 1
    else:
        return 0
def send_mail(mail_host,mail_port,mail_user,to_list, sub, content,attachment):
    msg = MIMEMultipart()
    msg['Subject'] = 'leo.zhai@bizfocus.cn'
    msg['From'] = 'leo.zhai@bizfocus.cn'
    msg['To'] = 'leo.zhai@bizfocus.cn'  # 将收件人列表以‘；’分隔

    # 下面是文字部分，也就是纯文本
    puretext = MIMEText(content)
    msg.attach(puretext)
    # 首先是xlsx类型的附件
    xlsxpart = MIMEApplication(open(script_path+'files/'+attachment+'.xls', 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename=sub+'.xls')
    msg.attach(xlsxpart)
    try:
        server = smtplib.SMTP()
        server.connect('mail.bizfocus.cn',25)  # 连接服务器
        server.sendmail('leo.zhai@bizfocus.cn', 'leo.zhai@bizfocus.cn', msg.as_string())
        server.close()
        return True
    except (TypeError, ValueError) as e:
        print  (e)
        return False

def main():
    #获取邮件服务器信息
    server_infos_list = server_infos()
    print server_infos_list
    #循环所有的邮件配置
    for mail_info in mail_infos():
        #判断是否要发送邮件,1表示发送，0表示不发送
        if is_sendmail(mail_info)==1:
            w = xlwt.Workbook()
            ws = w.add_sheet(sheet_name, cell_overwrite_ok=True)
            global title_start
            global row_start
            global data_length
            title_start = 4
            row_start = 11
            data_length = 0
            print '准备发送',mail_info[2],mail_info[3],mail_info[4],mail_info[5]
            report_subject=mail_info[0]
            report_name=mail_info[1]
            #file_name=mail_info[0]+'-'+mail_info[1]+'-'+datetime.datetime.now().strftime('%Y-%m-%d')
            file_name=report_subject+'-'+report_name+'-'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            att_name=report_subject+'-'+report_name+'-'+datetime.datetime.now().strftime('%Y-%m-%d')
            report_info_list={}
            #循环报表中的每一个可视化
            for i in sqlite_query(sqlite3_file, report_sql %(mail_info[0],mail_info[1])):
                report_info_list[i]=eval(i[4].replace('"',"'"))['top']
            #根据可视化的top位置进行排序

            for chart_seq,report_infos in enumerate(sorted(report_info_list.items(),key=lambda item:item[1])):
                report_info=report_infos[0]
                #如果是数据表
                if report_info[3]==7:
                    report_data_sql = 'select ' + (report_info[5]+','+report_info[6]).strip(',') + ' from (' + report_info[2] + ') a '
                # 如果是透视表
                if report_info[3] == 6:
                    report_data_sql = 'select ' + (report_info[5] + ',' + report_info[6]).strip(',') + ' from (' + report_info[2] + ') a group by '+report_info[7].strip(',')+' order by '+report_info[7].strip(',')
                for dbinfo in sqlite_query(sqlite3_file, DB_info_Sql % report_info[1]):
                    con_string3 = '%s/%s@%s:%d/%s' % (dbinfo[2], dbinfo[3], dbinfo[0], dbinfo[4], dbinfo[1])
                # 数据行数
                row_count=oracle_query(con_string3, report_data_sql)[1]


                if chart_seq==0:
                    query_to_workbook_title(ws,oracle_query(con_string3, report_data_sql),row_start)



                #将可视化写入excel文件
                query_to_workbook(ws,oracle_query(con_string3, report_data_sql),row_start)

                #从写入的行数开始继续写入
                row_start=row_start+row_count+1


            ws.insert_bitmap('./bea.bmp', 1, 1)
            # global data_length
            ws.insert_bitmap('./ctrip.bmp', 1, data_length + 3)
            # 保存excel文件
            w.save(script_path + 'files/' + file_name + '.xls')
            #send_mail(mail_host, mail_user, mail_pass, mail_info[5], att_name, content,file_name)
            send_mail(server_infos_list[0], server_infos_list[1], server_infos_list[2], mail_info[5], att_name, content, file_name)
        else:
            print '不发送',mail_info[2],mail_info[3],mail_info[4]

if __name__ == "__main__":

    script_path='/opt/scripts/'
    mail_info_sql1 = open(script_path+'mail_info_sql1.sql', 'r').read()
    mail_info_sql2 = open(script_path+'mail_info_sql2.sql', 'r').read()
    server_info_sql = open(script_path + 'server_info_sql.sql', 'r').read()
    DB_info_Sql = open(script_path+'DB_info_Sql.sql', 'r').read()
    report_sql = open(script_path+'report_sql.sql', 'r').read()
    sqlite3_file = '/opt/reporttool/sqliteDB/bi_setting1.s3db'

    #mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
    #mail_user = "z_llong@163.com"  # 用户名
    #mail_pass = "zllong145511"  # 密码

    #mail_host = "?"
    #mail_user = "yuantz@hkbea.com"  # 用户名
    #mail_pass = "Aysphoelia13"  # 密码#
    content=' '
    sheet_name=u'简报'

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title_start = 4
    row_start = 11
    data_length = 0
    main()
    print '--------------------------------------------------------------------------------------'

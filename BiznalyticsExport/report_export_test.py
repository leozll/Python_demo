#  -*-  coding:  UTF-8  -*-
import sqlite3
import xlrd
import csv, codecs, cStringIO


csvFile2 = open('ReportChartDimesion.csv','wb')
writer = csv.writer(csvFile2)

sqlite3_file='D:\\Project\\BEA\\bi_setting1.s3db'
con = sqlite3.connect(sqlite3_file)
cur = con.cursor()
cur.execute('select * from ReportChartDimesion limit 5')
for res in cur.fetchall():
    writer.writerow(res)
csvFile2.close()



sqlite3_file2='D:\\Project\\BEA\\test.s3db'
con2 = sqlite3.connect(sqlite3_file2)
cur2 = con2.cursor()
csv_file = 'ReportChartDimesion.csv'
for row in csv.reader(open('ReportChartDimesion.csv', "rb")):
    print 1
    csvsql="INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4],row[5])
    cur2.execute(csvsql)#


con2.commit()
con2.close()
print('ok')##
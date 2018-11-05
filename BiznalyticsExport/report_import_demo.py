#  -*-  coding:  UTF-8  -*-
import sqlite3
import xlrd
import csv, codecs, cStringIO


def csv2table(csv_file,csv_sql):
    #csv_file = 'ReportChartDimesion.csv'
    for row in csv.reader(open(csv_file, "rb")):
        #csvsql = "INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s','%s','%s','%s')" % (row[0], row[1], row[2], row[3], row[4], row[5])
        cur2.execute(csvsql)  #


table_sql="""select %s.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join BusinessPackageTable on BusinessPackage.id=BusinessPackageTable.BusinessPackageId
        inner join BusinessPackageColumn on BusinessPackageTable.id=BusinessPackageColumn.BusinessPackageTableId
        where BusinessSubject.name='%s' and Report.name='%s'
"""

#print table_sql %('BusinessSubject','风险','简报')
subject_name='风险报表'
report_name='简报'

sqlite3_file2='test.s3db'
con2 = sqlite3.connect(sqlite3_file2)
cur2 = con2.cursor()
for row in csv.reader(open('BusinessSubject.csv', "rb")):
    csv_sql="INSERT INTO BusinessSubject  VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
    cur2.execute(csv_sql)
for row in csv.reader(open('Report.csv', "rb")):
    csv_sql="INSERT INTO Report  VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4],row[5],row[6])
    cur2.execute(csv_sql)
for row in csv.reader(open('ReportChart.csv', "rb")):
    csv_sql="INSERT INTO ReportChart  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)
for row in csv.reader(open('BusinessPackage.csv', "rb")):
    csv_sql="INSERT INTO BusinessPackage  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)
for row in csv.reader(open('BusinessPackageTable.csv', "rb")):
    csv_sql="INSERT INTO BusinessPackageTable  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)
for row in csv.reader(open('BusinessPackageColumn.csv', "rb")):
    csv_sql="INSERT INTO BusinessPackageColumn  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)

for row in csv.reader(open('Semantics.csv', "rb")):
    csv_sql="INSERT INTO Semantics  VALUES ('%s','%s')" %(row[0], row[1])
    cur2.execute(csv_sql)
for row in csv.reader(open('ReportChartMeasure.csv', "rb")):
    csv_sql="INSERT INTO ReportChartMeasure  VALUES ('%s','%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4],row[5])
    cur2.execute(csv_sql)
for row in csv.reader(open('ReportChartDimesion.csv', "rb")):
    csv_sql="INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)
for row in csv.reader(open('ReportAuth.csv', "rb")):
    csv_sql="INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s)" %(row[0], row[1], row[2])
    cur2.execute(csv_sql)
for row in csv.reader(open('DataSource.csv', "rb")):
    csv_sql="INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
    cur2.execute(csv_sql)
for row in csv.reader(open('ReportFilter.csv', "rb")):
    csv_sql="INSERT INTO ReportChartDimesion  VALUES ('%s','%s','%s','%s','%s')" %(row[0], row[1], row[2], row[3], row[4])
    cur2.execute(csv_sql)
con2.commit()

con2.close()
print('ok')##
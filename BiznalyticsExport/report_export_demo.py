#  -*-  coding:  UTF-8  -*-
import sqlite3
import xlrd
import csv, codecs, cStringIO


table_sql="""select %s.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join BusinessPackageTable on BusinessPackage.id=BusinessPackageTable.BusinessPackageId
        inner join BusinessPackageColumn on BusinessPackageTable.id=BusinessPackageColumn.BusinessPackageTableId
        where BusinessSubject.name='%s' and Report.name='%s'
"""

ReportChartDimesion_sql="""select ReportChartDimesion.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join BusinessPackageTable on BusinessPackage.id=BusinessPackageTable.BusinessPackageId
        inner join BusinessPackageColumn on BusinessPackageTable.id=BusinessPackageColumn.BusinessPackageTableId
        inner join ReportChartDimesion on BusinessPackageColumn.id=ReportChartDimesion.BusinessPackageColumnId and ReportChartDimesion.ReportChartId=ReportChart.id
        where BusinessSubject.name='%s' and Report.name='%s'
"""

ReportChartMeasure_sql="""select ReportChartMeasure.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join BusinessPackageTable on BusinessPackage.id=BusinessPackageTable.BusinessPackageId
        inner join BusinessPackageColumn on BusinessPackageTable.id=BusinessPackageColumn.BusinessPackageTableId
        inner Join ReportChartMeasure on BusinessPackageColumn.id=ReportChartMeasure.BusinessPackageColumnId and ReportChartMeasure.ReportChartId=ReportChart.id
        where BusinessSubject.name='%s' and Report.name='%s'
"""

Semantics_sql="""select Semantics.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join BusinessPackageTable on BusinessPackage.id=BusinessPackageTable.BusinessPackageId
        inner join BusinessPackageColumn on BusinessPackageTable.id=BusinessPackageColumn.BusinessPackageTableId
        inner Join Semantics on Semantics.id=BusinessPackageColumn.SemanticsId
        where BusinessSubject.name='%s' and Report.name='%s'
"""

ReportAuth_sql="""select ReportAuth.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportAuth on Report.id=ReportAuth.reportid
        where BusinessSubject.name='%s' and Report.name='%s'
"""

ReportFilter_sql="""select ReportFilter.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportFilter on Report.id=ReportFilter.reportid
        where BusinessSubject.name='%s' and Report.name='%s'
"""

DataSource_sql="""select DataSource.*
        from BusinessSubject 
        inner join Report on BusinessSubject.id=Report.BusinessSubjectId
        inner join ReportChart on Report.id=ReportChart.reportid
        inner join BusinessPackage on BusinessPackage.id=Report.BusinessPackageId
        inner join DataSource on DataSource.id=BusinessPackage.DataSourceId
        where BusinessSubject.name='%s' and Report.name='%s'
"""

#print table_sql %('BusinessSubject','风险','简报')
subject_name='风险报表'
report_name='简报'

sqlite3_file = 'bi_setting1.s3db'
con = sqlite3.connect(sqlite3_file)
cur = con.cursor()
for table_name in ['BusinessSubject','Report','ReportChart','BusinessPackage','BusinessPackageTable','BusinessPackageColumn']:
    csvFile2 = open(table_name+'.csv','wb')
    writer = csv.writer(csvFile2)
    cur.execute(table_sql % (table_name,subject_name,report_name))
    for res in cur.fetchall():
        writer.writerow([unicode(s).encode("utf-8") for s in res])
    csvFile2.close()

for table_name in ['ReportChartDimesion','ReportChartMeasure','Semantics','ReportAuth','ReportFilter','DataSource']:
    if table_name=='ReportChartDimesion':
        table_sql=ReportChartDimesion_sql
    elif table_name=='ReportChartMeasure':
        table_sql=ReportChartMeasure_sql
    elif table_name=='Semantics':
        table_sql=Semantics_sql
    elif table_name=='ReportAuth':
        table_sql=ReportAuth_sql
    elif table_name=='ReportFilter':
        table_sql=ReportFilter_sql
    elif table_name=='DataSource':
        table_sql=DataSource_sql
    csvFile3 = open(table_name+'.csv','wb')
    writer = csv.writer(csvFile3)
    cur.execute(table_sql % (subject_name,report_name))
    for res in cur.fetchall():
        writer.writerow([unicode(s).encode("utf-8") for s in res])
    csvFile3.close()

con.commit()
con.close()
print('ok')##
from tablestore import *
import time

table_name = 'OTSGetRowSimpleExample'

def create_table(client):
    schema_of_primary_key = [('uid', 'INTEGER'), ('gid', 'INTEGER')]
    table_meta = TableMeta(table_name, schema_of_primary_key)
    table_options = TableOptions()
    reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
    client.create_table(table_meta, table_options, reserved_throughput)
    print ('Table has been created.')

def delete_table(client):
    client.delete_table(table_name)
    print ('Table \'%s\' has been deleted.' % table_name)

def put_row(client,tbl,pk,attr):
    row = Row(pk, attr)
    condition = Condition(RowExistenceExpectation.IGNORE)
    try:
        consumed, return_row = client.put_row(tbl, row, condition)
    except OTSClientError as e:
        print ("put row failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
        # 服务端异常，一般为参数错误或者流控错误。
    except OTSServiceError as e:
        print ("put row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))

    #print ('Write succeed, consume %s write cu.' % consumed.write)

def get_col(client,tbl,pk,cols,cond):
    #cond = CompositeColumnCondition(LogicalOperator.AND)
    #cond.add_sub_condition(SingleColumnCondition("status", 'running', ComparatorType.EQUAL))
    #cond.add_sub_condition(SingleColumnCondition("name", '杭州', ComparatorType.EQUAL))

    #cond = SingleColumnCondition("status", 'running', ComparatorType.EQUAL)

    #cond=None

    try:
        consumed, return_row, next_token = client.get_row(tbl, pk, cols, cond, 1)
        if return_row is None:
            return 'NoData'
        else:
            #print('PK: %s Value of attribute: %s' % (str(pk), return_row.attribute_columns))
            #for att in return_row.attribute_columns:
            #    print ('name:%s\tvalue:%s\ttimestamp:%d' % (att[0], att[1], att[2]))
            return return_row.attribute_columns[0][1]
    except OTSClientError as e:
        print("get row failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    # 服务端异常，一般为参数错误或者流控错误。
    except OTSServiceError as e:
        print ("get row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))

def list_table(client):
    print ('Begin ListTable')
    tables = client.list_table()
    print ('All the tables you have created:')
    for table in tables:
        print (table)
    print ('End ListTable')
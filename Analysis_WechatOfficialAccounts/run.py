#  -*-  coding:  UTF-8  -*-
import datetime
from func.func_sendmail import *

if __name__ == "__main__":
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    handler('a','b')
    print ('--------------------------------------------------------------------------------------')

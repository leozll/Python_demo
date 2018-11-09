#  -*-  coding:  UTF-8  -*-

def write_to_file(data_list,file_name,mode):
	f = open(file_name,mode)
	f.writelines(data_list)
	f.close()
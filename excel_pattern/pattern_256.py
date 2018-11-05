# -*- coding: utf-8 -*-
import xlwt
#新建一个excel文件
file=xlwt.Workbook()
#新建一个sheet
table=file.add_sheet('sheet name',cell_overwrite_ok=True)
# 可以通过set_colour_RGB来自定义RGB颜色
xlwt.add_palette_colour("custom_colour1", 0x21)
file.set_colour_RGB(0x21, 54, 96, 146)
for i in range(0,256):
        stylei= xlwt.XFStyle()            #初始化样式
        patterni= xlwt.Pattern()          #为样式创建图案
        patterni.pattern=1                #设置底纹的图案索引，1为实心，2为50%灰色，对应为excel文件单元格格式中填充中的图案样式
        patterni.pattern_fore_colour=i    #设置底纹的前景色，对应为excel文件单元格格式中填充中的背景色
        #patterni.pattern_back_colour=0   #设置底纹的背景色，对应为excel文件单元格格式中填充中的图案颜色
        stylei.pattern=patterni           #为样式设置图案
        table.write(i,0,i,stylei)         #使用样式

        style_custom=xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour1')
        table.write(i, 1, i, style_custom)

file.save('D:/colour2.xls')
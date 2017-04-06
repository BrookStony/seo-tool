# -*- coding: utf-8 -*-
import xlrd
import xlwt

def open_excel(file= 'file.xls'):
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name("cloud")
    val = sheet.cell(0, 0).value
    print(sheet.ncols)
    print(sheet.nrows)
    print(val)


def set_style(name ,height, bold=False):
    style = xlwt.XFStyle() # 初始化样式

    font = xlwt.Font() # 为样式创建字体
    # font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


# 写excel
def write_excel():
    # 创建工作簿
    f = xlwt.Workbook()

    # 创建sheet
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    row0 = [u'业务',u'状态',u'北京',u'上海',u'广州',u'深圳',u'状态小计',u'合计']
    column0 = [u'机票',u'船票',u'火车票',u'汽车票',u'其它']
    status = [u'预订',u'出票',u'退票',u'业务小计']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

        # 生成第一列和最后一列(合并4行)
        i, j = 1, 0
        while i < 4*len(column0) and j < len(column0):
            sheet1.write_merge(i, i+3, 0, 0, column0[j], set_style('Arial',220,True)) #第一列
            sheet1.write_merge(i, i+3, 7, 7) #最后一列"合计"
            i += 4
            j += 1

            sheet1.write_merge(21,21,0,1,u'合计',set_style('Times New Roman',220,True))

        # 生成第二列
        i = 0
        while i < 4*len(column0):
            for j in range(0, len(status)):
                sheet1.write(j+i+1, 1, status[j])
                i += 4

    f.save('D:\dev\python\seo-tool\conf\demo.xls') #保存文件

open_excel("D:\dev\python\seo-tool\conf\IBM Landing Page.xls")
write_excel()
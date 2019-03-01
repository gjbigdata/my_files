import xlrd
import pymysql
from datetime import datetime
from xlrd import xldate_as_tuple
import sys

#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告 （2019年第一期）\\201901041644525004\\新建文件夹\\2019年第一期不合格.xlsx"
#file = "D:\\data_syj_cjxx\泸州市食品药品监督管理局食品安全监督抽检信息公告 （2018年第二期）\\201805241055204832\\食品抽检不合格-2018年第二期信息发布.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2017年第九期）\\201801101025165911.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2017年第六期）\\201710301054547215\\食品安全抽检不合格--2017年第六期信息发布.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2017年第十期）\\201803050923086468.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第八期）\\不合格.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第九期）\\201811301130172266\\第九期不合格定稿.xlsx"
#file = "D:\\data_syj_cjxx\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第七期）\\201809291704130745\食品抽检第七期\\第七 期不合格.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第十期）\\201812211135438102\\第十期不合格定稿.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第四期）\\201807301743099597\\第四期不合格.xlsx"
#file = "D:\\data_syj_cjxx\\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第五期）\\201808310935262398\\第五期不合格.xlsx"
file = "D:\\data_syj_cjxx\泸州市食品药品监督管理局食品安全监督抽检信息公告（2018年第一期）\\201803231603535218.xlsx"
wb = xlrd.open_workbook(file)
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
print(rows)
db = pymysql.connect('localhost','root','1111','syjgsxx')
cusor = db.cursor()
for i in range(2,rows):
    cybh = str(sheet.cell_value(i,0))
    id = str(sheet.cell_value(i,1) )
    nominal_enterprise_name = str(sheet.cell_value(i,2))
    nominal_enterprise_address = str(sheet.cell_value(i,3))
    sampled_enterprise_name = str(sheet.cell_value(i,4))
    sampled_enterprise_address = str(sheet.cell_value(i,5))
    food_name=str(sheet.cell_value(i,6))
    spec_type=str(sheet.cell_value(i,7))
    trademark=str(sheet.cell_value(i,8))
    if sheet.cell_type(i,9)==3:
        product_date=datetime(*xldate_as_tuple(sheet.cell_value(i,9), 0)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        product_date = sheet.cell_value(i,9)
    print(product_date)
    Unqualified_info=str(sheet.cell_value(i,10))
    fenlei=str(sheet.cell_value(i,11))
    gonggaohao=str(sheet.cell_value(i,12))
    gonggaoriqi=datetime(*xldate_as_tuple(sheet.cell_value(i,13), 0)).strftime('%Y-%m-%d %H:%M:%S')
    rewulaiyuan=str(sheet.cell_value(i,14))
    inspection_org=str(sheet.cell_value(i,15))
    remark=str(sheet.cell_value(i,16))
    sql = "INSERT INTO `gsxx` VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' );"%(
                                                                                                cybh,id,nominal_enterprise_name,\
                                                                                                 nominal_enterprise_address,\
                                                                                                 sampled_enterprise_name,\
                                                                                                 sampled_enterprise_address,\
                                                                                                 food_name,\
                                                                                                 spec_type,\
                                                                                                 trademark,\
                                                                                                 product_date,\
                                                                                                 Unqualified_info,\
                                                                                                 fenlei,\
                                                                                                 gonggaohao,\
                                                                                                 gonggaoriqi,\
                                                                                                 rewulaiyuan,\
                                                                                                 inspection_org,\
                                                                                                 remark
                                                                                                 )

    try:
        cusor.execute(sql)
        db.commit()
        print("success")
    except Exception as e:
        print(e)
        db.rollback()
db.close()
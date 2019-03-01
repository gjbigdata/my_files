import pandas as pd
import os
from sqlalchemy import create_engine
import re
from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://root:1111@localhost:3306/syjgsxx')

path  = "D:\\data_syj_cjxx"
file_list = []
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        if ".xlsx" in name:
            file_list.append(os.path.join(root, name))
def get_area(string):
    if not isinstance(string,float):
        string.encode("utf-8")
        pattern = "(合江|叙永|龙马潭|江阳|古蔺|纳溪|泸县)"
        regx = re.compile(pattern)
        data_list = regx.findall(string)
        area = data_list[0] if data_list else "不详"
    else:
        return "不详"
    return area
def get_len(string):
    if isinstance(string,str):
        return len(string)
    else:
        return len(str(string))
def int_to_datime(data):
    if isinstance(data,int):
        return datetime(1900, 1, 1) + timedelta(days=data-1)
    else:
        return data
df_all = []
for fi in file_list:
    df = pd.read_excel(fi,header=None)
    df = df.drop(index=0,axis=0)
    len_ = len(df.columns)
    print(len_)
    if len_ == 17:
        columns = ['抽样编号', '序号', '标称生产企业名称', '标称生产企业地址', '被抽样单位名称', '被抽样单位地址', '食品名称',
                   '规格型号', '商标', '生产加工、购进）日期/批号', '不合格项目║检验结果║标准值', '分类', '公告号', '公告日期',
                   '任务来源/项目名称', '检验机构', '备注']
        df.columns = columns
        #print(df["不合格项目║检验结果║标准值"])
        df = df.drop(index=1,axis=0)
        try:
            df["地区"] = df["被抽样单位地址"].map(get_area)
        except Exception as e:
            print(str(e),fi)
        df.drop("被抽样单位地址",axis=1,inplace=True)
        df = df.drop("不合格项目║检验结果║标准值", axis=1).join(df["不合格项目║检验结果║标准值"].str.split('；', expand=True).stack().reset_index(level=1, drop=True).rename('不合格项目║检验结果║标准值'))
        # df = df.drop("不合格项目║检验结果║标准值",axis=1).join(df["不合格项目║检验结果║标准值"].str.split("║|‖",expand=True))
        df["是否合格"] = False
        try:
            #df["不合格信息长度"] = df["不合格项目║检验结果║标准值"].map(get_len)
            df["公告日期"].map(int_to_datime)
        except Exception as e:
            print(df)
        df_all.append(df)
    elif len_== 16:
        columns = ['抽样编号', '序号', '标称生产企业名称', '标称生产企业地址', '被抽样单位名称', '被抽样单位地址', '食品名称',
                   '规格型号', '商标', '生产加工、购进）日期/批号', '分类', '公告号', '公告日期',
                   '任务来源/项目名称', '检验机构', '备注']
        df.columns = columns
        df = df.drop(index=1,axis=0)
        try:
            df["地区"] = df["被抽样单位地址"].map(get_area)
        except Exception as e:
            print(str(e),fi)
            df["地区"] = "不详"
        df.drop("被抽样单位地址",axis=1,inplace=True)
        df["是否合格"] = True
        df_all.append(df)
    else:
        print("格式错误无法解析",fi)

data = pd.concat(df_all,axis=0,join='outer',join_axes=None,ignore_index=True,keys=None,levels=None,names=None,sort=False)
print(data)
data.to_sql('my_data_new', engine, index= False)
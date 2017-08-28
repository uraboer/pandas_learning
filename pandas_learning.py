# learn from:http://www.cnblogs.com/en-heng/p/5630849.html

'''
1.引言
Pandas是一个开源的Python数据分析库。Pandas把结构化数据分为三类：
Series：1维，可视作没有column名的，只有一个column的DataFrame；
DataFrame：同Spark SQL中的DataFrame一样，其概念来自于R语言，为多column并schema化的2维结构化数据，可视作为Series的容器；
Panel：为3维的结构化数据，可视作DataFrame的容器；
'''

import pandas as pd
import numpy as np

# df = pd.DataFrame({
#     "total_bill": [16.99, 10.34, 23.68, 23.68, 24.59],
#     "tip": [1.01, 1.66, 3.50, 3.31, 3.61],
#     "sex": ["Female", "Male", "Male", "Male", "Female"]
# })

# 对于DataFrame固有属性：
# print(df)
# print(df.dtypes) #data type of columns
# print(df.index) #indexes
# print(df.columns) #return pandas.Index
# print(df.values) #each row,return array
# print(df.shape) #a tuple representing the dimensionality of df

'''
.index:行索引
.columns:列名称
.dtype:数据类型
'''

# 2.SQL操作
# Select
# loc，基于列label，可选取特定行（根据行index）;

# iloc，基于行/列的position;
# print(df.loc[1:3, ["total_bill", "tip"]])
# print(df.loc[1:3,"tip":"total_bill"])
# print(df.iloc[1:3,[1,2]])
# print(df.iloc[1:3,1:3])

# at:根据指定行index及列label，快速定位DataFrame的元素；
# iat，与at类似，不同的是根据position来定位的；
# print(df.at[3,"tip"])
# print(df.iat[3,1])

# ix，为loc与iloc的混合体，既支持label也支持position;
# print(df.ix[1:3,[1,2]])
# print(df.ix[1:3,["total_bill","tip"]])

# print(df[1:3])
# print(df.ix[["total_bill","tip"]])

# where
# print(df[df["sex"]=="Female"])
# print(df[df["total_bill"]>20])
# print(df.query("total_bill>20"))

# and,or,in,not
# print(df[(df["sex"]=="Female") & (df["total_bill"]>20)])
# print(df[(df["sex"]=="Female")|(df["total_bill"]>20)])
# print(df[df["total_bill"].isin([20.01,23.68,24.59])])

# print(df[-(df["sex"]=="Male")])
# print(df[-df["total_bill"].isin([20.01,23.68,24.59])])

# print(df=df[(-df["app"].isin(sys_app))&(-df.app.str.contains('^微信\d+$'))])

# 对where条件筛选后只有一行的dataframe取其中某一列的值，其两种实现方式如下：
# 1.use
# total=df.loc[df["tip"]==1.66,"total_bill"].values[0]
#
2.
# total = df.get_value(df.loc[df["tip"] == 1.66].index.values[0],"total_bill")
# print(total)

# distinct
# print(df.drop_duplicates(subset=["sex"],keep="first",inplace=True))
'''
subset:为选定的列做distinct，默认为所有列；
keeep:值选项｛"first","last",False｝,保留重复元素的第一个，最后一个，或全部删除；
inplace:默认为False，返回一个新的dataframe；若为True，则返回去重后的原dataframe
'''

# group
# print(df)
# print(df.groupby("sex").size())
# print(df.groupby("sex").count())

# 多合计函数：select sex,max(tip),sum(total_bill) from tips_tb group by sex;
# print(df.groupby("sex").agg({"tip":np.max,"total_bill":np.sum}))

# print(df.groupby("tip").agg({"sex":pd.Series.nunique}))

# as
# df.columns=["total","pit","xes"]
# print(df)
# df.rename(columns={"total_bill":"total","tip":"pit","sex":"xes"},inplace=True)
# print(df)

# join
# df.join(df2,how="left"...)
# pd.merge(df1,df2,how="left",left_on="app",right_on="app")

# 第一种方法是按DataFrame的index进行join的，而第二种方法才是按on指定的列做join。left、right、inner、full outer四种方式

# order
# print(df.sort_values(["total_bill","tip"],ascending=[False,True]))

# top
# 对于全局的top:
# print(df)
# print(df.nlargest(3,columns=["total_bill"]))

'''
对于分组top,MySQL的实现（采取自join的方式）
select a.sex,a.tip
from tips_tb a
where (
    select count(*)
    from tips_tb b
    where b.sex=a.sex and b.tip>a.tip
)<2
order by a.sex,a.tip desc;
'''

# pandas的等价实现：
# 1.use
# df.assign(rn=df.sort_values(["total_bill"],ascending=False)
#           .groupby("sex")
#           .cumcount()+1)\
#     .query("rn<3")\
#     .sort_values(["sex","rn"])
# 2.
# df.assign(rn=df.groupby("sex")["total_bill"]
#           .rank(method="first",ascending=False))\
#     .query("rn<3")\
#     .sort_values(["sex","rn"])
#
# replace
# overall replace
# df.replace(to_replace="Female",value="Sansa",inplace=True)
# print(df)

# dict replace
# df.replace({"sex":{"Female":"Sansa","Male":"Leone"}},inplace=True)
# print(df)

# replace on where condition
# df.loc[df.sex == "Male","sex"] = "Leone" #只替换sex部分
# print(df)

# 自定义
# map(func):为Series的函数，DataFrame不能直接调用，需取列后再调用；
# apply(func):对DataFrame中的某一列/行进行func操作；
# applymap(func):为element-wise函数，对每一个元素做func操作

# print(df["tip"].map(lambda x:x-1))
# print(df[["total_bill","tip"]].apply(sum))
# print(df.applymap(lambda x:x.upper() if type(x) is str else x))


# df = pd.read_csv("E:/workspace_python/data_pandas_learning.csv", names=["id", "os", "dim", "uv", "pv"], sep="\t")
# print(df)

# Add
# row_df = pd.DataFrame(np.array([["2", "ios", "苹果-iPad 4", 3287509, 32891811]]), columns=["id", "os", "dim", "uv", "pv"])
# df = df.append(row_df, ignore_index=True)

# print(df)

# 增加一列
# df["time"]="2017-08-28"
# print(df)

# To Dict
# def where(df, column_name, id_value):
#     df = df[df[column_name] == id_value]
#     return df
#
# def to_dict(df):
#     """
#     {"pv" or "uv ->{"os":os_value}}
#     :return:dict
#     """
#     df = where(df, "id", 0)
#     df_dict = df.set_index("os")[["uv", "pv"]].to_dict()
#     print(df_dict)
#
# if __name__ == '__main__':
#     to_dict(df)


# # Top
# # group某列后的top值，比如android、ios的UV top 2的厂商：
# def group_top(df, group_col, sort_col, top_n):
#     """
#     get top(`sort_col`) after group by `group_col`
#     :param df: dataframe
#     :param group_col: string, column name
#     :param sort_col: string, column name
#     :param top_n: int
#     :return: dataframe
#     """
#     return df.assign(rn=df.sort_values([sort_col], ascending=False)
#                      .groupby(group_col)
#                      .cumcount() + 1) \
#         .query('rn < ' + str(top_n + 1)) \
#         .sort_values([group_col, 'rn'])
#
#
# #全局top值加上group某列后的top值，并去重：
# def top(df,group_col,sort_col,top_n):
#     all_top_df=df.nlargest(top_n,columns=sort_col)
#     grouped_top_df=group_top(df,group_col,sort_col,top_n)
#     grouped_top_df=grouped_top_df.ix[:,0:-1]
#     result_df=pd.concat([all_top_df,grouped_top_df]).drop_duplicates()
#     print(result_df)
#
# if __name__ == '__main__':
#     top(df,"os","uv",2)


#编号排序
#对某列排序后并编号，相当于给出排序名次。比如，对UV的排序编号：
# df["rank"]=df["uv"].rank(method="first",ascending=False).apply(lambda x:int(x))
# print(df)

#Left Join
#Pandas的left join对NULL的列没有指定默认值：
# def left_join(left,right,on,right_col,default_value):
#     df=pd.merge(left,right,how="left",on=on)
#     df[right_col]=df[right_col].map(lambda x:default_value if pd.isnull(x) else x)
#     return df

#自定义
#对某一列做较为复杂的自定义操作，比如，厂商的UV占比：
# def percentage(part,whole):
#     return round(100*float(part)/float(whole),2)
#
# os_dict=to_dict(df)
# all_uv=sum(os_dict["uv"].values())
# df=where(df,"id",1)
# df["per"]=df.apply(lambda r:percentage(r["uv"],all_uv),axis=1)

#重复值:某列的重复值的行,返回True or False
# duplicate=df.duplicated(subset="dim",keep=False)
# print(duplicate)
# print(df)

#写入MySQL
#sshtunnel模块提供ssh通道
# import MySQLdb
# from sshtunnel import SSHTunnelForwarder
#
# with SSHTunnelForwarder(
#         ("porxy host",port),
#         ssh_password="os passwd",
#         ssh_username="os user name",
#         remote_bind_address=("mysql host",3306)
# )as server:
#     conn=MySQLdb.connect(host="127.0.0.1",user="mysql user name",passwd="mysql passwd",db="db name",port=server.local_bind_port,charset="utf-8")
#     df.to_sql(name="tb name",con=conn,flavor="mysql",if_exists="append",index=False)
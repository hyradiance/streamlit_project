import streamlit as st
import numpy as np
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
def sql_to_data(str_sql):
    with SSHTunnelForwarder(
        # 指定ssh登录的跳转机的address
        ssh_address_or_host = ('8.140.143.128',22),
        # 设置密钥
        # ssh_pkey = private_key,
        # 如果是通过密码访问，可以把下面注释打开，将密钥注释即可。
        ssh_password = "AScbM6PUL8mrNdGxS6DpcBpu",
        # 设置用户
        ssh_username = 'wisdom',
        # 设置数据库服务地址及端口
        remote_bind_address= ('pc-2ze8ov6i9ri93ujpc.rwlb.rds.aliyuncs.com',3306)) as server:
        conn = pymysql.connect(database='dongpin_db',
                                user='dp_read_user',
                                password='wqzozQKuaePvXU68',
                                host='127.0.0.1',  # 因为上面没有设置 local_bind_address,所以这里必须是127.0.0.1,如果设置了，取设置的值就行了。
                                port=server.local_bind_port) # 这里端口也一样，上面的server可以设置，没设置取这个就行了
        df = pd.read_sql(str_sql,conn)
    return df

#df转换为csv
def convert_df(df):
    return df.to_csv().encode('gbk')


with st.expander('客服-用户下单金额'):
    user=st.text_input(label='输入用户ID',placeholder='少量用户ID直接输入用空格隔开,多个用户ID从excel复制一列粘贴到此')
    str_user=user.replace(' ',',')  #把输入的ID用逗号隔开
    date_start=st.date_input(label='输入开始时间',help='00:00:00开始')
    date_end=st.date_input(label='输入结束时间',help='23:59:59结束')
    sql_user_gmv="""select o.user_id 用户ID,sum(o.order_money) 下单金额
                from mall_order o
                where o.order_status in (2,5,9) and o.depot_id=1 and  #完成+北京仓
                o.order_time between '"""+str(date_start)+" 00:00:00' AND '"+str(date_end)+""" 23:59:59' and
                o.user_id in ("""+str_user+") group by o.user_id"

    if st.button(label='点此展示结果'):
        df_user_gmv = sql_to_data(sql_user_gmv)  #读取数据库 生成df
        st.write(df_user_gmv)  #展示结果
        csv = convert_df(df_user_gmv)  #df转换为csv
        st.download_button(label="点此下载,用excel打开或另存为xlsx后进行操作", data=csv,file_name=str(date_end)+'用户.csv')

# 指定店铺在上周的用户ID和下单金额
with st.expander('客服-用户下单店铺'):
    user=st.text_input(label='输入用户ID',placeholder='少量用户ID直接输入用空格隔开,多个用户ID从excel复制一列粘贴到此',key=1)
    str_user=user.replace(' ',',')  #把输入的ID用逗号隔开
    date_start=st.date_input(label='输入开始时间',help='00:00:00开始',key=1)
    date_end=st.date_input(label='输入结束时间',help='23:59:59结束',key=1)
    sql_store_gmv="""select o.user_id 用户ID,o.store_id 店铺ID,sum(o.order_money) 下单金额
                    from mall_order o
                    where o.order_status in (2,5,9) and o.depot_id=1 and  #完成+北京仓
                    o.order_time between '"""+str(date_start)+" 00:00:00' AND '"+str(date_end)+""" 23:59:59' and
                    o.user_id in ("""+str_user+") group by o.store_id"

    if st.button(label='点此展示结果',key=1):
        df_store_gmv = sql_to_data(sql_store_gmv)  #读取数据库 生成df
        st.write(df_store_gmv)  #展示结果
        csv = convert_df(df_store_gmv)  #df转换为csv
        st.download_button(label="点此下载,用excel打开或另存为xlsx后进行操作", data=csv,file_name=str(date_end)+'店铺.csv',key=1)

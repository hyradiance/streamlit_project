import streamlit as st
import numpy as np
import pandas as pd
from mypackage.on_line_mysql import sql_to_data

#df转换为csv
def convert_df(df):
    return df.to_csv().encode('gbk')

#指定用户在上周的下单金额
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

#指定用户在上周的店铺ID和下单金额
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

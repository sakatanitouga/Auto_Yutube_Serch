#!/usr/bin/env python
# coding: utf-8

# In[2]:





# In[2]:


from apiclient.discovery import build
import pandas as pd
import calendar
import datetime

YOUTUBE_API_KEY = input("APIキーを入力してください")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_statistics(id):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']
    df = [statistics['viewCount']]  
    return df
def get_video_info(this_part, this_order, this_type, this_num,this_publishedAfter,this_q,view_count):
    dic_list = []
    search_response = youtube.search().list(part=this_part,order=this_order,type=this_type,publishedAfter=this_publishedAfter,q=this_q)
    output = youtube.search().list(part=this_part,order=this_order,type=this_type,publishedAfter=this_publishedAfter,q=this_q).execute()
    no_reserch=False
    #実際に検索を行う
    for i in range(this_num):
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        if search_response==None:
            no_reserch=True
            break    
        output = search_response.execute()    
        
    df3=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)    
    if no_reserch==True :
        print("検索できなかったキーワード:"+this_q)
        return df3
    df = pd.DataFrame(dic_list)
    if df.empty:
        return df3
    #各動画毎に一意のvideoIdを取得
    df1 = pd.DataFrame(list(df['id']))['videoId']
       #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','title']]
    
    df2['url'] = "https://www.youtube.com/watch?v="+df1
    df1_count=0
    #検索を行った動画のコメント、視聴回数を取得
    df1_count=0
    for c in df1:
        count_info=get_statistics(c)
        if int(count_info[0])<=view_count:
            df3=df2[:df1_count]
            break
        df1_count+=1
    if df1_count==this_num*5:
        df3=df2       
    
    return df3
def time_calculate(serch_minutes):
    #現在時刻を取得
    date1 = datetime.datetime.now()
    date2 = datetime.timedelta(hours=-9)
    date_now = date1+date2
    #時間計算
    date_method = datetime.timedelta(minutes=serch_minutes)
    date_result=date_now+date_method
    
    ret=date_result.strftime('%Y-%m-%dT%H:%M:%SZ')
    return ret
    
df_use_skip = pd.read_excel('youtuber.xlsx', usecols=[0], skiprows=[0])
df_use_list = df_use_skip['チャンネル名'].values.tolist()


#検索ワード
user_list=['しばなん']
df3=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

date_result= datetime.datetime.now()
time_int=int(date_result.strftime('%H'))

#2018-08-01T00:00:00Z 
if time_int<18:
    time=time_calculate(serch_minutes=-1440)
else:
    time=time_calculate(serch_minutes=-120)
for name in df_use_list:
    df1 = get_video_info(this_part='snippet',this_order='viewCount',this_type='video',this_num = 1,this_publishedAfter=time,this_q=name,view_count=1000)
    df3 = pd.concat([df3, df1])            
df3.to_excel('resultl.xlsx', sheet_name='new_sheet_name')
print("resultl.xlsxに検索結果作成完了しました。")


# In[2]:




# In[3]:





# In[ ]:





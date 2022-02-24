import pandas as pd
import numpy as np
pd.options.display.precision = 2
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.rc('font', family='BIZ UDGothic')
import plotly
from PIL import Image

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

'''
# GoogleTrends分析アプリ
#### →GoogleTrendsのURL:https://trends.google.co.jp/trends/?geo=JP
###### 現状はプログラミング言語のカテゴリーで「Python、Java、C++、C言語」の組み合わせでの検索結果のみの対応。
'''
image = Image.open('search.png')
st.image(image, caption='↑こちらのようにGoogleTrendsで検索を行ってください。')
''
'''
#### ①地域選択
'''
geo  = st.radio("分析する地域を選択してください", ['日本', 'すべての国'])
'''
#### ②データアップロード
'''
file = st.file_uploader('こちらより検索結果のCSVファイルをアップリロードして下さい。')
if file is not None:
  df=pd.read_csv(file,header=1)
  if len(df.columns)==5:
    if f'Python: ({geo})' in df.columns:
      '''
      ##### ↓入力データをそのまま表示しています。
      ※期間内の最大検索数を１００とした相対値となっています。
      '''
      df
      '''
      ##### 各期間における各言語の検索比率をパーセント（％）で表示しています。
      '''
      index=df.columns[0]      
      df['C/C++']=df[f'C++: ({geo})']+df[f'C言語: ({geo})']
      df['Python']=100*df[f'Python: ({geo})']/df.sum(axis=1)
      df['Java']=100*df[f'Java: ({geo})']/df.sum(axis=1)
      df['C/C++']=100*df['C/C++']/df.sum(axis=1)
      st.dataframe(df[[f'{index}','Python','Java','C/C++']])       
      csv = convert_df(df)
      st.download_button(
          label="Download data as CSV",
          data=csv,
          file_name='trend_data.csv',
          mime='text/csv',
      )
      fig, ax1 = plt.subplots(figsize=(12, 8))
      ax1.plot(df[f'{index}'],df['Python'],label=f"Python",color="red")
      ax1.plot(df[f'{index}'],df['Java'],label=f"Java",color="blue")
      ax1.plot(df[f'{index}'],df['C/C++'],label=f"C/C++",color="green")
      ax1.set_xlabel(f'{index}', fontsize=20)
      ax1.set_ylabel("割合", fontsize=20)
      ax1.legend(bbox_to_anchor=(0.2,0.99), loc='upper left', borderaxespad=0, fontsize=20)
      ax1.set_title(f"GoogleTrends比較＜世界の人気の動向＞", fontsize=20)
      plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
      plt.gcf().autofmt_xdate() 
      plt.tight_layout();
      st.plotly_chart(fig)
    
    else:
      st.error('地域を選択し直すか、選択中の地域のデータを含むファイルをアプロードし直してください。')
  else:
    x=len(df.columns)-1
    st.error(f'検索ワード数が{x}になっています。現状は[Python,Java,C++,C言語]の４つの組み合わせのみしか対応しておりません。')
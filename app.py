import streamlit as st
import pandas as pd
import numpy as np
import json 
import os
from PIL import Image
import requests

st.set_page_config(
    layout='wide',
    page_title='Document Reader Demo',
    page_icon= 'FPT_logo_2010.svg.png'
)

if __name__ == '__main__':

    st.title('Document Reader Demo')



@st.cache
def get_data():
    url = 'https://api.fpt.ai/vision/idr/vnm'
    headers = {
        'api-key': 'g93aEayepguSZpPtLjtscKE4oJuScmgf'
    }
    with open(img.name,"wb") as f:
        f.write((img).getbuffer())
    files = {'image': open(img.name, 'rb').read()}
    response = requests.post(url, files=files, headers=headers)
    content = response.json()
    if content['errorCode'] != 0:
        data = content['errorMessage']
    else:
        data = content['data']
    return data
@st.cache
def load_csv():
    return pd.read_csv('test_data.csv', index_col='Unnamed: 0')



col2, col3 = st.columns(2)

option = st.sidebar.selectbox(
    "Choose type of document",
    ("CCCD", "CMND")
)
   

with col2:
   instructions = "Upload your files below"
   st.subheader(instructions)
   img = st.file_uploader('Upload file')
   if img:
        st.image(img) 

with col3:
    st.subheader(f'Result of {option}')
    if img:
        data = get_data()
        try:
            df = pd.json_normalize(data)
            prob_columns = []
            for column in df.columns:
                if "prob" in column:
                    prob_columns.append(column)
            non_prob_col = df.drop(columns = prob_columns)
            dic = non_prob_col.to_dict()
            df_final = pd.DataFrame.from_dict(dic, orient='index')
            st.dataframe(df_final, use_container_width =True, height=df_final.size*40)
        except:
            st.error(data)
    
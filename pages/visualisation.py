import streamlit as st
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

data=open('engdata.bin','rb')
attentionData=data.read().decode("UTF-8")

st.set_page_config(page_title="Attention Analysis Dashboard", layout="wide")
st.title("📊 Attention Analysis Dashboard")
st.markdown("""
### Overview
This dashboard visualizes engagement levels using pie and line charts. It helps analyze attention trends dynamically.
""")
col1, col2 = st.columns(2)


primaryColor = "#6A0DAD"
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#E5E5E5"
textColor = "#333333"

threshold = st.slider("Select minimum engagement threshold:", 0, 100, 50)
filtered_data = [d for d in data if d >= threshold]
st.write(f"Filtered data points above {threshold}%: {len(filtered_data)}")

def averageAttention(attentionData):
    count1=0
    count2=0
    for con in attentionData:
        if con=='1':
            count1+=1
        else:
            count2+=1
    totalcount=count1+count2
    return (count1/totalcount)*100



def movingAverage(attentionData):
    count=0
    count1,count2=0,0
    avgList=[]
    for con in attentionData:
        if count>=30:
            avg=(count1/(count1+count2))*100
            avgList.append(avg)
            count=0
            count1=0
            count2=0
        count+=1
        if con=='1':
            count1+=1
        else:
            count2+=1
    return avgList

data=movingAverage(attentionData)
avgattention=averageAttention(attentionData)

def linechart(attentionData):
    feild=range(0,len(data))
    line_chart_data = pd.DataFrame(data)
    st.line_chart(line_chart_data)

def piechart(pie_chart_data):
    labels=["engaged","not attentive"]
    sizes=[pie_chart_data,100-pie_chart_data]
    explode=(0,0.1)
    fig1,ax1=plt.subplots()
    ax1.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)


with col1:
    st.subheader("📈 Engagement Trend")
    linechart(data)

with col2:
    st.subheader("🎯 Attention Distribution")
    piechart(avgattention)
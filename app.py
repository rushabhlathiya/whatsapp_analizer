import streamlit as st
import preprocessing as p
import helper as h
from io import StringIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import pandas as pd
import seaborn as sns



# sideBar
st.sidebar.title("Chat Analizer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    # st.write(string_data)

    df,num_media = p.preproces(string_data)
    

# f =open('../Data chats\WhatsApp Chat with D2D.txt','r',encoding='utf-8')
# data = f.read()
# df = p.preproces(data)


# st.dataframe(df)

# dropdown Box

    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    # user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'Overall')


    selectedUser = st.sidebar.selectbox(
        "How would you like to be contacted?",
        user_list)

    # Button

    if st.sidebar.button("Analize"):
        num_msg,words,media,links = h.fetch_stats(selectedUser,df)  
        col1, col2, col3,col4 = st.columns(4)

        with col1:
        
          st.header("Total Messages")
          st.title(num_msg)

        with col2:
          st.header("Total words")
          st.title(words)


        with col3:
          st.header("Media Shared")
          st.title(num_media)

        
        with col4:
          st.header("Link Shared")
          st.title(links)
          
        # monthly Daily Timeline
        
        mounthly,daily = h.monthly_daily(selectedUser,df)
        st.header('Monthly Timeline')
        st.line_chart(mounthly)
        
        st.header('Daily Counts')
        st.line_chart(daily)
        
        # Busy month Busy Days
        
        st.header('Activity Map')
        col1, col2 = st.columns(2)  
        month,days = h.busy_day_month(selectedUser,df)

        with col1:
            fig,ax = plt.subplots()
            st.header("Most Busy Month")
            ax.bar(month.index,month.values,color = 'purple')
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)
        
        with col2:
            fig,ax = plt.subplots()
            st.header("Most Busy Day")
            ax.bar(days.index,days.values,color = 'orange')
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)
            
        # Weakly heat map

        st.header('Weekly Activity Map')
        hours_count = h.weekly_count(selectedUser,df)
        
        fig,ax = plt.subplots()
        ax = sns.heatmap(hours_count, cmap='coolwarm')
        
        
        st.pyplot(fig)

        # mostB Busy user
        
        if selectedUser == 'Overall':
          x,new_df = h.most_busy(df)
          fig,ax = plt.subplots()
          col1, col2 = st.columns(2)
          
          with col1:
            st.header("Most Busy Users")
            ax.bar(x.index,x.values)
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)
          with col2:
            st.header("Chat Contribution")
            st.dataframe(new_df)

        # WordCloud and wordCount

        st.header('Most words used')
        str = h.word_cloud(selectedUser,df)
        wc = WordCloud(stopwords='english',min_font_size=10,width=500,height=500,background_color='white').generate(str)
        col1, col2 = st.columns(2)
        with col1:
          fig, ax = plt.subplots()
          ax.imshow(wc)
          st.pyplot(fig)
        with col2:
          most_comon_worlds = pd.DataFrame({'words':wc.process_text(str).keys(),'count':wc.process_text(str).values()})
          most_comon_worlds =most_comon_worlds.sort_values(by='count',ascending=False).head(20).reset_index(drop=True)
          fig, ax = plt.subplots(figsize=(10, 10))
          ax.barh(most_comon_worlds['words'],most_comon_worlds['count'])
          ax.legend()
          st.pyplot(fig)
          
        
        # Emoji counter Pie Chart 
          
        st.header('Emoji Analysis')
        col1, col2 = st.columns(2)
        emtemp = h.emoji_extractor(selectedUser,df)
        with col1:
          st.dataframe(emtemp)
        with col2:
          fig, ax = plt.subplots()
          ax.pie(emtemp['count'].head(), labels=emtemp['emoji'].head(),autopct='%.2f%%')
          st.pyplot(fig)
        



        
            



    # total msg
    # total words
    # media shared
    # link shared

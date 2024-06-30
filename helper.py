from urlextract import URLExtract
import pandas as pd
import emoji
extractor = URLExtract()

def fetch_stats(selectedUser, df):
   
   if selectedUser != 'Overall':
      df = df[df['user'] == selectedUser]
   
   num_msg = df.shape[0]
      
   word =[]
   urls =[]
   for line in df['message']:
      word.extend(line.split(" "))  
      urls.extend(extractor.find_urls(line))
      
      
   num_media =df[df['message'] =='<Media omitted>'].shape[0] 
   num_links = len(urls)
   
   return num_msg,len(word),num_media,num_links
   
   
def most_busy(df):
   return df[df['user' ]!= 'group notification']['user'].value_counts().head(),((df[df['user' ]!= 'group notification']['user'].value_counts()/df.shape[0])*100).reset_index().rename(columns={'count': 'percentage'})

def word_cloud(selectedUser,df):
   
   if selectedUser != 'Overall':
     df = df[df['user'] == selectedUser]
   
   str =''
   for line in df['message']:
      
      if (line != '<Media omitted>') & ((extractor.has_urls(line)) ==False):
         str = str + line+" "   
   
   return str

def monthly_daily(selectedUser,df):
   if selectedUser != 'Overall':
      df = df[df['user'] == selectedUser]
   
   df['date'] = pd.to_datetime(df['date'], errors='coerce')
   temp =df.set_index('date')   
   monthly_counts =temp.resample('M').size()
   daily_counts =temp.resample('D').size()

   return monthly_counts,daily_counts

def busy_day_month(selectedUser,df):
   if selectedUser != 'Overall':
      df = df[df['user'] == selectedUser]
   day_name = pd.Series()
   for key,subdf in df.groupby('day_name'):
      day_name[key] = subdf.shape[0]
    
   day_name.sort_values(ascending=False,inplace=True)
   month_names = pd.Series()
   for key,subdf in df.groupby('month'):
       month_names[key] = subdf.shape[0]
    
   month_names.sort_values(ascending=False,inplace=True)
   
   return month_names,day_name

def weekly_count(selectedUser,df):
   if selectedUser != 'Overall':
      df = df[df['user'] == selectedUser]
      
   hours_count = pd.DataFrame()
   for key,subdf in df.groupby('day_name'): 
      data =[]   
      for x in range(1,25):
         data.append(subdf[subdf['hour'] == x].shape[0])
      hours_count[f"{key}"] =data
   hours_count.rename(index=lambda x: f"{x}-{x+1}",inplace= True)
   return hours_count.T
   # return df.pivot_table(index='day_name',columns='hour',values='message',aggfunc='count').fillna(0)


def emoji_extractor(selectedUser,df):
   if selectedUser != 'Overall':
      df = df[df['user'] == selectedUser]
   emo =[]
   for line in df['message']:
      for x in emoji.emoji_list(line):
         if len(x):
               emo.append(x['emoji'])
   # print(emo)        
   emoji_df = pd.DataFrame({'emoji':emo})
   return emoji_df.value_counts().reset_index()
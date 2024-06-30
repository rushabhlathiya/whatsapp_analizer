import re
import pandas as pd
def preproces(data):
    patten ='\d+\/\d+\/\d+,\s\d+:\d+\s-\s'
    msg =re.split(pattern=patten,string= data)[1:]
    date = re.findall(patten,data)
    df = pd.DataFrame({'message': msg,'date':date})
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y, %H:%M - ')
    user =[]
    msg =[]
    for str in df['message']:
        temp =re.split('([\w\W]+?):\s',str)
        # temp = str.split(':')
        # print(temp)
        if len(temp)>1:
            user.append(temp[1])
            msg.append(temp[2])
        else:
            user.append('group notification')
            msg.append(temp[0])
    df['user'] = user
    df['message'] = msg
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['day_name']=df['date'].dt.day_name()
    
    df['message']= df['message'].apply(lambda x: x.strip())
    
    return df
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

st_words =['a',
 'about',
 'above',
 'after',
 'again',
 'against',
 'ain',
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',
 'aren',
 "aren't",
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 'couldn',
 "couldn't",
 'd',
 'did',
 'didn',
 "didn't",
 'do',
 'does',
 'doesn',
 "doesn't",
 'doing',
 'don',
 "don't",
 'down',
 'during',
 'each',
 'few',
 'for',
 'from',
 'further',
 'had',
 'hadn',
 "hadn't",
 'has',
 'hasn',
 "hasn't",
 'have',
 'haven',
 "haven't",
 'having',
 'he',
 "he'd",
 "he'll",
 'her',
 'here',
 'hers',
 'herself',
 "he's",
 'him',
 'himself',
 'his',
 'how',
 'i',
 "i'd",
 'if',
 "i'll",
 "i'm",
 'in',
 'into',
 'is',
 'isn',
 "isn't",
 'it',
 "it'd",
 "it'll",
 "it's",
 'its',
 'itself',
 "i've",
 'just',
 'll',
 'm',
 'ma',
 'me',
 'mightn',
 "mightn't",
 'more',
 'most',
 'mustn',
 "mustn't",
 'my',
 'myself',
 'needn',
 "needn't",
 'no',
 'nor',
 'not',
 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',
 'shan',
 "shan't",
 'she',
 "she'd",
 "she'll",
 "she's",
 'should',
 'shouldn',
 "shouldn't",
 "should've",
 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 "that'll",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 "they'd",
 "they'll",
 "they're",
 "they've",
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 've',
 'very',
 'was',
 'wasn',
 "wasn't",
 'we',
 "we'd",
 "we'll",
 "we're",
 'were',
 'weren',
 "weren't",
 "we've",
 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',
 'won',
 "won't",
 'wouldn',
 "wouldn't",
 'y',
 'you',
 "you'd",
 "you'll",
 'your',
 "you're",
 'yours',
 'yourself',
 'yourselves',
 "you've"]
def preproces(data):
    patten ='\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}.(?:am|pm|AM|PM)\s-\s|\d+\/\d+\/\d+,\s\d+:\d+\s-\s'
    msg=re.split(pattern=patten,string= data)[1:]
    date = re.findall(patten,data)
    df = pd.DataFrame({'message': msg,'date':date})
    df['date'] = df['date'].apply(year_converter)
    if 'pm' in date[2] or 'am' in date[2] :
        df['date'] = pd.to_datetime(df['date'],format='%d/%m/%y, %I:%M\u202f%p - ')
    elif  'AM' in date[2] or 'PM' in date[2]:
        df['date'] = pd.to_datetime(df['date'],format='%m/%d/%y, %I:%M\u202f%p - ')
    else:
        df['date'] = pd.to_datetime(df['date'],format='%d/%m/%y, %H:%M - ')
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
    # Modifation From here
    num_media =df[df['message'] =='<Media omitted>'].shape[0]
    df = df[df['user'] != 'group notification']
    df =df[df['message']!="<Media omitted>"]
    df = df[df['message'] !='This message was deleted']
    df = df[df['message'] !='']
    df['message'] = df['message'].apply(remove_stopwords)
    # To here
    
    return df,num_media

def remove_stopwords(msg):
    nost = []
    t_words = word_tokenize(msg)
    for word in t_words:
        if word not in st_words:
            nost.append(word)
            
    return ' '.join(nost)

def year_converter(str):
    year=re.findall('^\d+\/\d+\/(\d+)',str)
    if len(year[0])==4:
        return (str.replace(year[0],year[0][2:]))
    else:
        return str
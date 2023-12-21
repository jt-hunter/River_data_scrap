import requests 
from bs4 import BeautifulSoup as bsoup
import datetime
import pandas as pd
import re
import numpy as np
import math

littlefalls = '01646500' # DEPENDENT
senecacreek = '01645000' # not used
pointofrocks = '01638500'
edwards_ferry = '01644148' # not used
shepherdstown = '01618000'
pawpaw = '01610000' # not used
hancock = '01613000'
springfield = '01608500'
moorfield = '01608070' # not used

# list to hold variables
gage_list = [littlefalls, pointofrocks, shepherdstown, hancock, springfield]

def get_date_time():
    d = dict() # build dict
    
    d['today'] = str(datetime.datetime.now().date()) # get today date
    d['earlier_day'] = str(datetime.datetime.now().date() - datetime.timedelta(days=2)) # get today date
    
    
    d['time_now'] = str(datetime.datetime.now().time())[:-3] # get time, remove unused digits
    
    return d 

def clean_HTML_data(html_data):
    location_of_data_start_in_html = re.search('10s', html_data) # find location of start of data
    location_of_data_start_in_html = location_of_data_start_in_html.span()
    html_data = html_data[(location_of_data_start_in_html[1]+2):] # add 2 to skip some slashes
    html_data = html_data[2:]
    html_data = html_data.replace('\\t' , ',')
    html_data = html_data.split('\\n')
    html_data = [sub.split(',') for sub in html_data]
    html_data = html_data[:-1]
    return html_data

def get_current_gage_heights(gage): # for gage in gage_list loop here
    date_time = get_date_time()
    url = 'https://waterservices.usgs.gov/nwis/iv/?sites=' + gage +\
        '&parameterCd=00065&startDT=' + date_time.get('earlier_day') + 'T' + date_time.get('time_now') + '-05:00' +\
        '&endDT=' + date_time.get('today') + 'T' + date_time.get('time_now') + '-05:00&siteStatus=all&format=rdb'                
    req = requests.get(url)
    if req.status_code == 200: # if webpage request is good...
        datahtml = str(req.content)
        if re.search('No sites found', datahtml): # if no gage or parameter found...
            print('No parameter found')
            df_func = pd.DataFrame()
        else:
            datahtml = clean_HTML_data(datahtml) # clean HTML function
            df_func = pd.DataFrame(datahtml, columns=['USGS','ID','Date','Tz', gage,'P']) # name columns
            df_func = df_func.drop(columns=['USGS','ID','Tz','P']) # drop unwanted variables
    else:
        print('request not good')
        
    return df_func

def create_df(gage_list):
    
    df = pd.DataFrame()
    df = get_current_gage_heights(gage_list[0]) # put only date/time values for little falls
    df = df.drop(df.columns[1], axis=1) # removes data and leave just Dates to merge onto
    
    for gage in gage_list: 
        temp_df = get_current_gage_heights(gage) # get gage heights function
    if temp_df.empty:
        pass
    else:
        df = df.merge(temp_df, how='outer', left_on='Date', right_on='Date')
    return df


df = pd.DataFrame()
df = get_current_gage_heights(gage_list[0])
df = df.drop(df.columns[1], axis=1) # removes data and leave just Dates to merge onto


#Loop to cycle through every listed gage and parameter measurement
for gage in gage_list: 
    print('Trying to merge '+ gage)
    temp_df = get_current_gage_heights(gage)
    if temp_df.empty:
        pass
    else:
        df = df.merge(temp_df, how='outer', left_on='Date', right_on='Date')
      
    
def reduce_to_needed_obs(df, shift):
    # shift needs positive value loop to retrieve data farther back in past
    
    last_obs = -1
    data_list = [] # empty ist of list data will go into
    time_of_obs = df['Date'].values[(last_obs) - shift]
    
    # Springfield gage
    data_list.append(df['01608500'].values[(last_obs) - shift]) # 17hrs
    data_list.append(df['01608500'].values[(last_obs) - shift])
    data_list.append(df['01608500'].values[(last_obs) - shift])
    data_list.append(df['01608500'].values[(last_obs) - shift])
    
    # Hancock gage
    data_list.append(df['01613000'].values[(last_obs) - shift])
    
    # Shepardstown gage
    data_list.append(df['01618000'].values[(last_obs) - shift])
    
    # Point of Rocks gage
    data_list.append(df['01638500'].values[(last_obs) - shift])
    
    
    return data_list, time_of_obs

def loop_to_get_full_obs(df):
    shift = 0
    
    # move observations back until all are not NaN
    while any(pd.isnull(reduce_to_needed_obs(df, shift)[0])) == True:
              shift += 1
    
    return reduce_to_needed_obs(df, shift)

def turn_obs_into_needed_np_array(input_obs_tuple):
# for creating np array for use in model predict
    
    predict_data_lol = input_obs_tuple[0]
    
    predict_input_17hr = np.array([predict_data_lol[0], predict_data_lol[1], predict_data_lol[2], predict_data_lol[3]])
    predict_input_15hr = np.array([predict_data_lol[0], predict_data_lol[4]])
    predict_input_8hr = np.array([predict_data_lol[0], predict_data_lol[4], predict_data_lol[5]])
    predict_input_4hr = np.array([predict_data_lol[0], predict_data_lol[4], predict_data_lol[5], predict_data_lol[6]])
    
    return predict_input_17hr, predict_input_15hr, predict_input_8hr, predict_input_4hr


obs = loop_to_get_full_obs(df)
prediction_inputs = turn_obs_into_needed_np_array(obs)



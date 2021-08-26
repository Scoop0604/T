from selenium.webdriver import  Chrome
from selenium.webdriver.common.keys import Keys
import requests
import re
import pandas as pd
def trans(input_df):
    input_df['C_floor'] = input_df.floor.astype('str').str[1:3]
    C_floor_list = ['低层','中层','高层']
    trans_list = ['low','middle','high']
    n = 0
    for floortype in C_floor_list:
        get_index = input_df[input_df.C_floor == floortype].index.values
        input_df.loc[get_index, 'C_floor'] = trans_list[n]
        n = n+1
    return input_df.C_floor

pd.set_option('display.max_columns',None)

chrome = Chrome(executable_path=r'C:\Users\miracle\AppData\Local\Google\Chrome\Application\chromedriver.exe')

# Xpaths that list the different zone option buttons
xpath_1 = ['longgang','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[1]/a']
xpath_2 = ['longhua','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[2]/a']
xpath_3 = ['baoan','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[3]/a']
xpath_4 = ['nanshan','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[4]/a']
xpath_5 = ['futian','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[5]/a']
xpath_6 = ['luohu','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[6]/a']
xpath_7 = ['pingshan','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[7]/a']
xpath_8 = ['guangming','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[8]/a']
xpath_9 = ['yantian','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[9]/a']
xpath_10 = ['dapengxinqu','//*[@id="@(Model.clickid)@(viewSifo.pageType==1?"]/ul/li[10]/a']

list_xpath = [xpath_1,xpath_2,xpath_3,xpath_4,xpath_5,xpath_6,xpath_7,xpath_8,xpath_9,xpath_10]

url = 'https://sz.esf.fang.com/'

response = chrome.get(url)

df_all = pd.DataFrame()

for xpath in list_xpath:
    ele1 = chrome.find_element_by_xpath(xpath[1])
    ele1.send_keys(Keys.ENTER)
    #Crawl data

    num_temp = []
    num = []
    df = pd.DataFrame()
    if xpath[0] == 'pingshan':
        p = int(re.search(r'\d+',chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[5]/div/span[8]').text).group())
    elif xpath[0] == 'guangming':
        p = int(re.search(r'\d+', chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[5]/div/span[9]').text).group())
    elif xpath[0] == 'dapengxinqu':
        p = int(re.search(r'\d+', chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[5]/div/span[4]').text).group())
    else:
        p = int(re.search(r'\d+',chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[5]/div/span[10]').text).group())

    for page_num in range(1,p+1):

        A_list = chrome.find_elements_by_xpath('//dl[@dataflag="bg"]')
        # print(len(A_list))

        for i in A_list:

            # Extract the data
            info2 = re.search(r'\d+', i.get_attribute('data-bg')).group() \
                    + '|' + i.find_elements_by_xpath('./dd/p')[0].text + '|' \
                    + i.find_elements_by_xpath('./dd/p')[2].text + '|' \
                    + i.find_elements_by_xpath('./dd/p')[1].text + '|' \
                    + i.find_elements_by_xpath('./dd')[1].text

            # Check the data

            # # Check the field
            # info2 = info2.split('|')
            # num_temp.append(len(info2))
            # # Delete unwanted fields
            if re.search(r'(\d+年建.*?)\w', info2) != None:  # Determine if there are any unwanted fields
                info2 = info2.replace(re.search(r'(\d+年建.*?)\w', info2).group(1), '').split('|')
            else:
                continue
            try:
                adtr = info2[7].split('\n')
            except:
                print(page_num,k)
            info2[7] = str('深圳市' + adtr[1] + adtr[0])
            df = pd.concat([df, pd.DataFrame({info2[0]: info2[1:]}).T])
            df = df.drop_duplicates()   # Deleting Deduplication
            num.append(len(info2))

        if page_num ==1:
            ele2 = chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[5]/div/p[1]/a')
            ele2.send_keys(Keys.ENTER)
        elif page_num > 1 and page_num <= p-1:
            ele2 = chrome.find_element_by_xpath('/html/body/div[4]/div[4]/div[4]/div/p[3]/a')
            ele2.send_keys(Keys.ENTER)
        else:
            pass

    # Check whether the fields are neat
    # for i in set(num_temp):
    #     print({i:'Accounted for%s' % round(num_temp.count(i)/len(num_temp),2)})
    # print('-'*50)

    print(len(num))
    print(num.count(num[0]) == len(num))  # Checking data length
    # print(info_num)

    # 2. Data cleaning
    df.columns = ['roomnum-hall', 'area', 'floor', 'direction', 'owner', 'other','address', 'price']
    print(df.head())
    print(df.shape[0])  
    print(df.describe(include='all').T)  

    '''
    After viewing the crawled data, it is found that the data in one column has multiple information. To facilitate data analysis, the data is split.
    '''
    # # Added housing area information
    df['district'] = xpath[0]
    df['roomnum'] = df['roomnum-hall'].astype('str').str[0:1]
    df['hall'] = df['roomnum-hall'].astype('str').str[2:3]
    del df['roomnum-hall']

    df['AREA'] = df['area'].apply(lambda x: x.replace('㎡', ''))
    del df['area']

    # # The floor data column holds only numeric values
    df['C_floor'] = trans(df)
    df['floor_num'] = df['floor'].astype('str').apply(lambda x: re.findall(r'\d+', x)[0])
    del df['floor']

    # # Get information on proximity to the school
    df = df.fillna('None')
    df['school'] = df['other'].apply(lambda x: 0 if re.search(r'优质教育', x) == None else 1)

    # #Get information on proximity to the subway
    # df['subway'] = df['other'].astype('str').apply(lambda x: 0 if re.search(r'距\d+号线', x) == None else 1)
    df['subway'] = df['other'].astype('str').apply(lambda x: re.search(r'\d+米', x).group() if re.search(r'\d+米', x) != None else ['no_subway'])
    df['subway'] = df['subway'].astype('str').apply(lambda x: x.replace('米', '') if re.search(r'\d+米', x) != None else 'no_subway')
    # # Deal with the price
    df['per_price_1'] = df['price'].astype('str').apply(lambda x: int(re.match(r'\d+', x.split('\n')[2])[0]) / 10000 if x != 'None' else None)
    # df['per_price_2'] = df['other'].astype('str').apply(lambda x: int(re.match(r'\d+', x.split('\n')[1])[0]) / 10000 if re.match(r'\d+',x.split('\n')[0]) != None else None)
    # df['per_price_3'] = df['owner'].astype('str').apply(lambda x: int(re.match(r'\d+', x.split('\n')[1])[0]) / 10000 if re.match(r'\d+',x.split('\n')[0]) != None else None)
    df['per_price'] = df['per_price_1'].fillna(0)
    # # Remove unwanted columns
    del df['other']
    del df['direction']
    del df['owner']
    del df['price']
    del df['per_price_1']
    # del df['per_price_2']
    # del df['per_price_3']
    print(df.head())


    # # 8) 合并不同区的数据
    df_all = pd.concat([df_all,df])
    df_all.to_excel(r'D:\case\new-case' + r'\szfj_' + xpath[0] + r'.xls')
    print('total %s data' % xpath[0])
    print('-' * 50)
    print('=' * 50)

# 查看所有爬取到的信息的数据数情况(即行数)
import os
os.chdir(r'D:\case\new-case')
num_all = 0
for i in os.listdir():
    locals()[i.split('.')[0]] = pd.read_excel(r'D:\case\new-case' +'\\'+ i)
    locals()[i.split('.')[0]] = locals()[i.split('.')[0]].drop_duplicates()
    print('%s表共计%d条数据'%(i.split('.')[0],locals()[i.split('.')[0]].shape[0]))
    num_all += locals()[i.split('.')[0]].shape[0]
    print('-'*50)
print('totoal %d' % num_all)


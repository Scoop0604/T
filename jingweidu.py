import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import json
import sys
import time
# from xpinyin import Pinyin
#
def getlnglat(address):
    """
    Get the latitude and longitude of the house
    """
    url = 'https://api.map.baidu.com/geocoding/v3/'
    # The output is in JSON format
    output = 'json'
    ak = '515ohDbmHDxW2j6syNc2Ob6HQHbGXpVD'
    add = quote(str(address))  # Sometimes you get a KeyError in quote, so you have to convert the inside of quote to a string  
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    # Build baidu map URL

    # The following piece of code is designed to prevent errors caused by too many requests  


    maxNum = 5
    for tries in range(maxNum):
        try:
            req = urlopen(uri, timeout = 30)  #  To prevent blocking
        except:
            if tries < (maxNum - 1):
                # time.sleep(10)
                continue
            else:
                print("Has tried %d times, all failed!", maxNum)
                break

    res = req.read().decode()
    temp = json.loads(res)
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat, lng
#
#
if __name__ == "__main__":
    dt = pd.read_excel(r"D:\case\new-case\szfj_dapengxinqu.xls")
    dt_lat = []
    dt_lag = []
    n = 0
 
    for add in dt.address:
        lat, lag = getlnglat(add)
        print(lat,lag)
        dt_lat.append(lat)
        dt_lag.append(lag)
        n = n+1
        p = n/16427*100
        print(str(p)+'%')
    dt['lat'] = dt_lat
    dt['lag'] = dt_lag
    print(dt)
    dt.to_excel(r'D:\case\new-case\firstdata.xls')

        # try:

        # print("address：{0}|longitude:{1}|latitude:{2}.".format(add, lng, lat))
        # except Error as e:
        #     print(e)




import math

import pandas as pd
from urllib.request import urlopen, quote
import json

def getlnglat(address):
    """
    Get latitude and longitude
    """
    url = 'https://api.map.baidu.com/geocoding/v3/'
    # The output is in JSON format
    output = 'json'
    ak = '515ohDbmHDxW2j6syNc2Ob6HQHbGXpVD'
    add = quote(str(address))  #Sometimes you get a KeyError in quote, so you have to convert the inside of quote to a string  
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    # Build baidu map URL

    # The following piece of code is designed to prevent errors caused by too many requests  

    maxNum = 5
    for tries in range(maxNum):
        try:
            req = urlopen(uri, timeout = 30)  # To prevent blocking
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



if __name__ == "__main__":
    dt = pd.read_excel(r"D:\case\new-case\firstdata.xls")

    CBDadd = ['深圳市罗湖区蔡屋围', '深圳福田cbd', '深圳南山商业文化中心区']
    n = 1
    for add in CBDadd:
        lat, lag = getlnglat(add)
        print(lat, lag)
        dt['cbdlat' + str(n)] = lat
        dt['cbdlag' + str(n)] = lag
        dt['cbdlat' + str(n)] = dt.lat.sub(dt['cbdlat' + str(n)])
        dt['cbdlag' + str(n)] = dt.lag.sub(dt['cbdlag' + str(n)])
        dt['cbdlat' + str(n)] = dt['cbdlat' + str(n)].apply(lambda x : x**2)
        dt['cbdlag' + str(n)] = dt['cbdlag' + str(n)].apply(lambda x : x**2)
        dt['distance'+str(n)] = dt['cbdlat' + str(n)] + dt['cbdlag' + str(n)]
        dt['distance'+str(n)] = dt['distance'+str(n)].apply(lambda x : math.sqrt(x))
        del dt['cbdlat' + str(n)]
        del dt['cbdlag' + str(n)]
        n = n+1
    dt['distance'] = dt[["distance1","distance2","distance3"]].mean(axis=1)
    dt = dt.drop(["distance1","distance2","distance3"],axis=1)
    print(dt)
    dt.to_excel(r'D:\case\new-case\firstdata.xls')


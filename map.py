import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

df1 =  pd.read_excel('data.xlsx')
df1



Shenzhen= gpd.read_file('Shenzhen.shp')

Shenzhen.plot()
#Shenzhen.head()

#select the data
df_geo = df.loc[:,['lag','lat','price.1']]
print(df_geo)

#Creat geodataframe
gdf = gpd.GeoDataFrame(df_geo, 
      geometry=gpd.points_from_xy(df_geo['lag'], df_geo['lat'], crs='epsg:4326'))
# print(gdf)
ax = Shenzhen.plot(color = 'white', edgecolor = 'black', figsize = (20,16))
gdf.plot(column = 'price.1', cmap='viridis', ax=ax, scheme='quantiles', k=15, legend = True)#,markersize=1
plt.show()
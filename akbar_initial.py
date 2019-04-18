#!/usr/bin/env python
# coding: utf-8

# In[23]:


from pprint import pprint
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon


# In[24]:


neighbourhoods = gpd.read_file('neighbourhoods.geojson')
print(neighbourhoods.head())


# In[25]:


neighbourhoods.neighbourhood_group.notna().sum()

neighbourhoods.drop('neighbourhood_group', axis=1, inplace =True)

neighbourhoods.head()


# In[26]:


print(neighbourhoods.crs)


# In[27]:


neighbourhoods_3857 = neighbourhoods.to_crs(epsg=3857)


# In[28]:


neighbourhoods_3857.head()


# In[29]:


neighbourhoods['area_kms'] = neighbourhoods_3857.geometry.area / 10**6


# In[30]:


neighbourhoods.head()


# In[31]:


neighbourhoods['center'] = neighbourhoods.geometry.centroid


# In[32]:


neighbourhoods.head()


# In[33]:


neighbourhoods.shape


# In[34]:


chicago_listings_sum = pd.read_csv('listings_summary.csv')


# In[37]:


chicago_listings_sum.drop('neighbourhood_group', axis=1, inplace=True)


# In[38]:


combined_gdf = gpd.GeoDataFrame(pd.merge(chicago_listings_sum,neighbourhoods,on='neighbourhood'),crs = neighbourhoods.crs)


# In[48]:


f, ax = plt.subplots(figsize=(12, 12))
combined_gdf.plot(ax=ax,column = 'neighbourhood',color='grey',edgecolor='white', legend = True, legend_kwds = {'title':'Neighbourhoods', 'loc':'lower center','bbox_to_anchor':(0.5, -0.6),'ncol':4}, axes = ax)
#ax.scatter(chicago_listings_sum.longitude[0:15], chicago_listings_sum.latitude[0:15], alpha = 0.3)
plt.scatter(chicago_listings_sum.longitude, chicago_listings_sum.latitude, alpha=0.3, color='red')
plt.title('Neighbourhoods of Chicago', size = 15)
plt.show()


# In[40]:


chicago = (41.881832, -87.623177)
fmap = folium.Map(location=chicago, zoom_start=15, zoom_control=True)
folium.GeoJson(neighbourhoods[neighbourhoods.neighbourhood == 'Lincoln Park'].geometry).add_to(fmap)
LP_series = gpd.GeoDataFrame(neighbourhoods[neighbourhoods.neighbourhood == 'Lincoln Park'])
LP_series.reset_index(inplace=True)
LP_coord = LP_series.center[0]
LP_rev_coord = [LP_coord.y, LP_coord.x]
lp_marker = folium.Marker(location=LP_rev_coord, popup='Lincoln Park')
lp_marker.add_to(fmap)
chicago_marker = folium.Marker(location=chicago, popup='<strong>'+'Chicago'+'</strong>')
chicago_marker.add_to(fmap)
display(fmap)


# In[41]:


plt.scatter(chicago_listings_sum.longitude.values, chicago_listings_sum.latitude.values)
plt.show()


# In[18]:


chicago_listings_sum.longitude


# In[ ]:





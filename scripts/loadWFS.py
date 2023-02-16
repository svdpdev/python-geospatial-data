# -*- coding: utf-8 -*-
"""

@author: Sander van der Plas
"""
import json
import geopandas as gpd
from owslib.wfs import WebFeatureService

class loadWFS:
    def __init__(self, wfsUrl, xmin, ymin, xmax, ymax):
        self.wfsUrl = wfsUrl
        self.wfs = WebFeatureService(url=self.wfsUrl, version='2.0.0')
        self.layer = list(self.wfs.contents)[0]
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    
    def get_features(self):
        startindex = 0
        max_features = 40000
        features = []
        while True:
            if startindex >= max_features:
                break
            response = self.wfs.getfeature(typename=self.layer, bbox=(self.xmin, self.ymin, self.xmax, self.ymax), outputFormat='json', startindex=startindex)
            data = json.loads(response.read())
            new_features = data['features']
            features.extend(new_features)
            if len(new_features) < 1000 or startindex + 1000 >= max_features:
                break
            startindex += 1000
        data['features'] = features
        return data
    
    
    def create_gdf(self):
        data = self.get_features()
        WFS = gpd.GeoDataFrame.from_features(data['features'])
        return WFS

if __name__ == "__main__":
    wfsUrl = 'https://service.pdok.nl/lv/bag/wfs/v2_0?request=GetCapabilities&service=WFS'
    xmin, ymin, xmax, ymax = 129979, 453904, 137537, 458517



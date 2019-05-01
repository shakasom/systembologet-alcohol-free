
import xml.etree.ElementTree as ET

import pandas as pd 
import numpy as np 

import geopandas as gpd 
from geopandas.tools import geocode
import geopy.geocoders
from geopy.geocoders import GoogleV3, Nominatim

from sklearn.preprocessing import MultiLabelBinarizer



def read_xml(xml_file):

    """Create a dataframe from xml file"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    butik = []
    artikel = []
    for node in root.iter('Butik'):
        butik.append(node.attrib.get('ButikNr'))
        artikel.append([artikel_elem.text for artikel_elem in node.getchildren()])

    d = {'butik': butik, 'artikels': artikel}
    df = pd.DataFrame(d)
    mlb = MultiLabelBinarizer()
    df_1Hot = df.join(pd.DataFrame(mlb.fit_transform(df.pop('artikels')),
                          columns=mlb.classes_,
                          index=df.index))
    return df_1Hot


def preprocess_alcohol(df):
    """ Filter out the alchohol free products from the all products and return a 
        list of strings for all alchohol free products"""
    alcohol_free = df[df['Varugrupp'] == 'Alkoholfritt']
    alcohol_free_list = list(alcohol_free['nr'])
    return list(map(str, alcohol_free_list))

def preprocess_availabe_products(df):
    """return only available products in Butiks that are also alcoholfree"""
    available_artikels = list(set(alcohol_free_list_str).difference(set(non_avaliable_artikels)))
    return df[available_artikels]
    


    
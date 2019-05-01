
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
    

def preprocess_availabe_products(df, available, non_availabe):
    """return only available products in Butiks that are also alcoholfree"""
    available_artikels = list(set(available).difference(set(non_availabe)))
    return df[available_artikels]

def calculate_alcoholfree_total(df, filtered):
    """calculate/sum number of products for each shop"""
    total = filtered.sum(axis=1)
    filtered.loc[:, 'total'] = total
    filtered.is_copy = None
    return pd.concat([df['butik'], filtered['total']], axis=1)


def merge_df(butiks, filtered_total):
    """ fill butik Nr and merge it with filtered"""
    butiks['Nr'] = butiks['Nr'].str.zfill(4)
    return pd.merge(butiks, filtered_total, left_on='Nr', right_on='butik')


def create_address_col(df):
    """ Concatenate Address, Postcode, City, and Country for geocoding """
    df['ADDRESS'] = df['Address1'].astype(str) + ',' + \
                    df['Address3'] + ',' + \
                    df['Address4'] + ',' + \
                    df['Address5'] + ',' + ' Sweden'   
    return df

def group_df_total(df, feature):
    """ Create dataframe from groupby total butik stocks and other features """
    grouped = df.groupby(feature)['total'].sum()
    return pd.DataFrame({feature: grouped.index, 'sum_total':grouped.values})



    
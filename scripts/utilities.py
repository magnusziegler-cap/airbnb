import pandas as pd
import numpy as np
import gzip
import shutil
import os
import geojson

def restructure_data():
    """ Renames the downloaded summary data and unzips the calendar, listings, and reviews data
    """
    data_path = '../data/'

    # rename the summary-packages with "_summary" postfix
    os.rename((data_path+'reviews.csv'), (data_path+'reviews_summary.csv'))
    os.rename((data_path+'listings.csv'), (data_path+'listings_summary.csv'))

    # unzip packages
    in_names = ["calendar.csv.gz", "listings.csv.gz", "reviews.csv.gz"]
    out_names = ["calendar.csv", "listings.csv", "reviews.csv"]

    for in_name, out_name in zip(in_names, out_names):
        with gzip.open(data_path + in_name, 'rb') as f_in:
            with open(data_path + out_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def load_data():
    """Loads all data

    Returns:
        _type_: dataframes:
        calendar
        listings
        listings_summary
        neighbourhoods
        reviews
        reviews_summary
        _type_: geojson feature_collection
        gj_neighbourhoods

    """
    data_path = '../data/'
    df_calendar = pd.read_csv(filepath_or_buffer=data_path+'calendar.csv')
    df_listings = pd.read_csv(filepath_or_buffer=data_path+'listings.csv')
    df_listings_summary = pd.read_csv(filepath_or_buffer=data_path+'listings_summary.csv')
    df_neighbourhoods = pd.read_csv(filepath_or_buffer=data_path+'neighbourhoods.csv')
    df_reviews = pd.read_csv(filepath_or_buffer=data_path+'reviews.csv')
    df_reviews_summary = pd.read_csv(filepath_or_buffer=data_path+'reviews_summary.csv')

    with open(data_path+'neighbourhoods.geojson', 'rb') as f_in:
        gj_neighbourhoods = geojson.load(f_in) 
    return df_calendar, df_listings, df_listings_summary, df_neighbourhoods, gj_neighbourhoods, df_reviews, df_reviews_summary
import os
import shutil
import gzip

import geojson
import pandas as pd

from typing import Union

import datetime


# Globals
DATA_PATH = '../data'

FILE_LIST = {
    'calendar':'calendar.csv',
    'calendar_gzip':'calendar.csv.gz',
    'listings':'listings.csv',
    'listings_summary':'listings_summary.csv',
    'listings_gzip':'listings.csv.gz',
    'reviews':'reviews.csv',
    'reviews_summary':'reviews_summary.csv',
    'reviews_gzip':'reviews.csv.gz',
    'neighbourhoods':'neighbourhoods.csv',
    'neighbourhoods_geojson':'neighbourhoods.geojson',
}

def create_backup(data_path=None) -> None:
    """ Creates a secondary or backup copy of the original data before any restructuring takes place
    """

    if data_path is None:
        data_path = DATA_PATH

    backup_path = os.path.join(data_path,'backup')
    os.mkdir(backup_path)

    for file_name in FILE_LIST.values():
        shutil.copy(
            src=os.path.join(data_path, file_name),
            dst=os.path.join(backup_path, file_name)
            )


def restructure_data(data_path=None) -> None:
    """ Renames the downloaded summary data and unzips the calendar, listings, and reviews data
    """
    if data_path is None:
        data_path = DATA_PATH

    # rename the summary-packages with "_summary" postfix
    os.rename(
        src=os.path.join(data_path,'reviews.csv'),
        dst=os.path.join(data_path,'reviews_summary.csv'))
    os.rename(
        src=os.path.join(data_path,'listings.csv'),
        dst=os.path.join(data_path,'listings_summary.csv'))

    # unzip packages
    in_names = ["calendar.csv.gz", "listings.csv.gz", "reviews.csv.gz"]
    out_names = ["calendar.csv", "listings.csv", "reviews.csv"]

    for in_name, out_name in zip(in_names, out_names):
        with gzip.open(os.path.join(data_path,in_name), 'rb') as f_in:
            with open(os.path.join(data_path,out_name), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def load_data(data_path=None):
    """Loads all data

    Returns:
        pd.DataFrame:
        calendar
        listings
        listings_summary
        neighbourhoods
        reviews
        reviews_summary

        geojson:
        feature_collection:gj_neighbourhoods
    """

    if data_path is None:
        data_path = DATA_PATH

    df_calendar = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'calendar.csv'))
    df_listings = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'listings.csv'))
    df_listings_summary = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'listings_summary.csv'))
    df_neighbourhoods = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'neighbourhoods.csv'))
    df_reviews = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'reviews.csv'))
    df_reviews_summary = pd.read_csv(filepath_or_buffer=os.path.join(data_path,'reviews_summary.csv'))

    with open(os.path.join(data_path,'neighbourhoods.geojson'), 'rb') as f_in:
        gj_neighbourhoods = geojson.load(f_in)
    return df_calendar, df_listings, df_listings_summary, df_neighbourhoods, gj_neighbourhoods, df_reviews, df_reviews_summary

def clean_listings(df_listings:pd.DataFrame)->pd.DataFrame:
    """ Clean up the listings dataframe.
    Performs the following:

    Args:
        df_listings (pd.DataFrame): listings dataframe

    Returns:
        pd.DataFrame: cleaned listings dataframe
    """
    df_listings_cleaned = df_listings
    df_listings_cleaned = df_listings_cleaned.replace(to_replace={'t':1, 'f':0}) #binarize t/f

    # bathroom mappings
    bathroom_mappings = parse_bathrooms(dataframe=df_listings["bathrooms_text"])
    df_listings_cleaned["bathrooms"] = df_listings_cleaned["bathrooms"].replace(to_replace=bathroom_mappings)

    #price to float
    df_listings_cleaned["price"] = df_listings_cleaned["price"].apply(_price_to_float)

    #cleaning in the "reviews" areas:
    df_listings_cleaned["reviews_per_month"] = df_listings_cleaned["reviews_per_month"].replace(to_replace="nan", value=0.0)

    #reviews features
    df_listings_cleaned["review_age"] = df_listings_cleaned["last_review"].apply(lambda x:_age_days(x))

    #licenses
    df_listings_cleaned = df_listings_cleaned.drop(columns="license")

    return df_listings_cleaned

def parse_bathrooms(dataframe:Union[pd.DataFrame,pd.Series], verbose=False)->dict:
    """Converts bathroom text descriptions to floats,
    and returns a dict that can be used in mapping

    Args:
        df (pd.DataFrame): listings dataframe
        verbose (bool, optional): prints descriptions and their inferred values. Defaults to False.

    Returns:
        dict: mapping between bathroom descriptions and numbers
    """
    bathroom_descriptions = dataframe.unique()
    
    bathrooms = {}
    bathrooms.update({'nan':float(0)}) #specifically add nan to the mapping dict

    for description in bathroom_descriptions:
        try:
            words = description.split(' ')
            numbers=[]
            for word in words:
                try:
                    numbers.append(float(word))
                except ValueError:
                    pass
            
            if not numbers: #if its empty bathrooms = 0
                bathroom_number = float(0)
            else:
                bathroom_number = numbers[0]
            bathrooms.update({description:bathroom_number})

            if verbose:
                print(f"Text description:'{description}' has {bathroom_number} baths \n")

        except AttributeError:
            pass

    return bathrooms

def _age_days(input_date, date_format="%Y-%m-%d") -> int:
    """calculate age in days (from today) from format

    Args:
        x (_type_): _description_

    Returns:
        int: number of days delta, -1 if date is not in past or date was NaN
    """
    try:
        age = datetime.datetime.today() - datetime.datetime.strptime(input_date, date_format)
        age = age.days
    except TypeError:
        age = -1
    return age

def _price_to_float(input_string:str, currency:str="$") -> float:
    """utility to convert the price string to a float
    drops the currency symbol(default dollar-sign), spaces, and comma.
    Args:
        input_string (str): string representing the price

    Returns:
        float: price
    """
    input_string = input_string.replace(currency,'').replace(' ','').replace(',','')

    return float(input_string)



import os
import zipfile
from datetime import date, timedelta
from io import BytesIO, StringIO

import httpx
import pandas as pd
import app

from CONSTANTS import *

ISO_2_TO_ISO_3_URL = "https://raw.githubusercontent.com/ilyabo/aiddata/master/data/static/data/countries-iso2-iso3.csv"
POPULATION_URL = (
    "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv"
)


@app.cache.memoize(timeout=app.TIMEOUT)
def load_latest_data(start_date=date.today(), go_back=10):
    counter = 0

    while counter < go_back:
        start_date -= timedelta(days=counter)
        url = get_url(start_date)
        r = httpx.get(url)

        if r.status_code == 200:
            df = pd.read_excel(BytesIO(r.content)).sort_values(
                [COUNTRY_TEXT, DATE]
            )
            df.loc[df[ISO2] == "UK", ISO2] = "GB"
            df_iso3 = load_iso3_codes()
            df_population = load_population()
            df = df.merge(df_iso3, left_on=ISO2, right_on="iso2")
            df = df.merge(df_population, on="iso3")
            return start_date, df.to_json(date_format="iso", orient="split")

        counter += 1

    raise ValueError("Not able to find data")


def dataframe():
    date, df = load_latest_data()
    return date, pd.read_json(df, orient="split")


def get_start_date():
    start_date, _ = dataframe()
    return start_date


def get_total_deaths():
    _, df = dataframe()
    return df[CASES].sum()


def get_new_deaths():
    _, df = dataframe()
    return df[df[DATE].max() == df[DATE]][DEATHS].sum()


def get_total_incidents():
    _, df = dataframe()
    return df[CASES].sum()


def get_new_incidents():
    _, df = dataframe()
    return df[df[DATE].max() == df[DATE]][CASES].sum()


def get_country_options():
    _, df = dataframe()
    return [
        {"value": row["iso3"], "label": row[COUNTRY_TEXT]}
        for _, row in df.groupby([COUNTRY_TEXT, "iso3"]).first().reset_index().iterrows()
    ]


def get_url(date):
    date_str = date.strftime("%Y-%m-%d")
    return f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{date_str}.xlsx"


def load_iso3_codes():
    if os.path.exists("data/iso2_to_3.parquet"):
        return pd.read_parquet("data/iso2_to_3.parquet")
    else:
        if not os.path.exists("data"):
            os.mkdir("data")
        df = pd.read_csv(ISO_2_TO_ISO_3_URL, usecols=["iso3", "iso2"]).dropna(how="all")
        df.to_parquet("data/iso2_to_3.parquet")
        return df


def load_population():
    if os.path.exists("data/population.parquet"):
        return pd.read_parquet("data/population.parquet")
    else:
        if not os.path.exists("data"):
            os.mkdir("data")
        r = httpx.get(POPULATION_URL)
        zipfile_ = zipfile.ZipFile(BytesIO(r.content))

        FILE_TO_EXTRACT = [i for i in zipfile_.namelist() if i.startswith("API_SP.POP.TOTL_DS2_en_csv")][0]

        df = pd.read_csv(
            BytesIO(zipfile_.read(FILE_TO_EXTRACT)),
            skiprows=3,
            usecols=["Country Code", "2018"],
        ).rename(columns={"Country Code": "iso3", "2018": "population_2018"})
        df.to_parquet("data/population.parquet")
        return df

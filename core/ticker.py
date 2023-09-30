import logging

from requests import Session
from pandas import DataFrame
from datetime import datetime, timedelta

from yfinance import download as yf_download

def download_ticker_data(
                    stock_name: str, 
                    time_delta : timedelta, 
                    session: Session)->DataFrame:
    '''
    Downloads the ticker data for the 
    provided time range and returns the DataFrame.
        params:
            stock_name : Ticker name
            time_delta : datetime.timedelta object

        returns -> DataFrame 
    '''
    start_date = datetime.strftime(datetime.now() - time_delta, "%Y-%m-%d")
    end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    logging.info(f"Fetching data for [{stock_name}] for time range [{start_date} to {end_date}]")
    data : DataFrame = yf_download(
        stock_name,
        start=start_date,
        end=end_date,
        session=session
        )
    return data
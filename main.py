import requests
import logging
import os
import tempfile
from typing import Any
from pandas import DataFrame
from datetime import datetime, timedelta
from yfinance import download as y_download
from json import load as j_load

def create_temp_openssl_config():
    '''
    Creates openssl config file to enable
    UnsafeLegacyRenegotiation option.
    '''
    global open_ssl_config_path
    config_content = """
    openssl_conf = openssl_init

    [openssl_init]
    ssl_conf = ssl_sect

    [ssl_sect]
    system_default = system_default_sect

    [system_default_sect]
    Options = UnsafeLegacyRenegotiation
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='wt', suffix='.cnf') as temp_file:
            temp_file.write(config_content)
    except Exception as e:
        logging.error(f"Error while creating openssl config file : [{e}]")
    else:
        open_ssl_config_path = temp_file.name
        logging.info(f"Setting OPENSSL_CONF->[{open_ssl_config_path}]")
        os.environ["OPENSSL_CONF"] = open_ssl_config_path

def initialize(ssl_verfiy:bool=False)->None:
    '''
    Setups basic stuff like logging and if
    ssl_verify is set to false then:
    Disable SSL warnings, setup global
    session that doesn't verify SSL and setups
    openssl_config
    '''
    setup_logging()
    global session
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    if not ssl_verfiy:
        logging.warn("YOUR HAD BEEN WARNED!! Initializing NON SSL HTTP request session.")
        create_temp_openssl_config()
        session.verify = False

def terminate()->None:
    # Ensure the temp file is cleaned up when the script ends
    if open_ssl_config_path:
        os.remove(open_ssl_config_path)

def setup_logging()-> None:
    '''
    Just a logging setup
    '''
    global logger
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized!")

def load_portfolio(path:str)->Any:
    '''
    Loads the portfolio json file
        param : path

        returns -> python portfolio object
    '''
    try:
        with open(path, 'r') as j:
            portfolio = j_load(j)
    except Exception as e:
        logging.error(f"Issue while loading the portfolio file : [{e}]")
        raise Exception(e)
    else:
        logging.info(f"Portfolio file loaded from path [{path}]")
        return portfolio

def download_ticker_data(stock_name: str, time_delta : timedelta)->DataFrame:
    '''
    Downloads the ticker data for the 
    provided time range and returns the dataframe.
        params:
            stock_name : Ticker name
            time_delta : datetime.timedelta object

        returns -> DataFrame 
    '''
    start_date = datetime.strftime(datetime.now() - time_delta, "%Y-%m-%d")
    end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    logging.info(f"Fetching data for [{stock_name}] for time range [{start_date} to {end_date}]")
    data : DataFrame = y_download(
        stock_name,
        start=start_date,
        end=end_date,
        session=session
        )
    return data

if __name__ == '__main__':
    initialize()
    data = download_ticker_data('INFY', timedelta(days=10))
    print(data)
from os import environ
from datetime import timedelta

from core.ticker import download_ticker_data

from utils.logging import setup_logging
from utils.sessions import get_session, terminate_session

def initialize(ssl_verify:bool=False)->None:
    '''
    Basic setup for:
        - logging
        - http session
    '''
    setup_logging()
    global session
    session = get_session(ssl_verify)

if __name__ == '__main__':
    initialize()
    data = download_ticker_data(
                    stock_name='INFY', 
                    time_delta=timedelta(days=100), 
                    session=session
                    )
    print(data)
    terminate_session()
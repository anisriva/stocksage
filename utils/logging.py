import logging
def setup_logging()-> None:
    '''
    Just a logging setup
    '''
    global logger
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized!")
import os
import logging
import tempfile
import requests
from requests.sessions import Session

def get_session(ssl_verify=False)->Session:
    '''
    If ssl_verify is set to false then:
     - Disable SSL warnings
     - setup openssl_config
    ''' 
    global session
    # disable_warnings(InsecureRequestWarning)
    # requests.packages.urllib3.disable_warnings()
    session = Session()
    if not ssl_verify:
        logging.warn("YOUR HAD BEEN WARNED!! Initializing NON SSL HTTP request session.")
        create_temp_openssl_config()
        session.verify = False
    return session

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
        logging.info(f"Setting OPENSSL_CONF=[{open_ssl_config_path}]")
        os.environ["OPENSSL_CONF"] = open_ssl_config_path

def terminate_session()->None:
    '''
    Cleans up the temp opensslconfig
    and closes the session.
    '''
    if open_ssl_config_path:
        logging.warn(f"Removing the config file : [{open_ssl_config_path}]")
        os.remove(open_ssl_config_path)
    if session:
        logging.warn(f"Closing the HTTP session.")
        session.close()
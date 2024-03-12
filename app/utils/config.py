import configparser
import os
from dotenv import load_dotenv

config_parser = configparser.ConfigParser()
config_file_path = 'config.ini'
dotenv_file_path = '.env'

def loadConfig():
    config_data = {}  # Dictionary to store configuration data
    
    # Check if config.ini exists and load its content
    if os.path.exists(config_file_path):
        try:
            config_parser.read(config_file_path)
            for section in config_parser.sections():
                for key, value in config_parser.items(section):
                    key = key.upper() # Convert key to uppercase
                    config_data[key] = value
        except configparser.Error as e:
            print(f"Error reading configuration file: {e}")
    
    return config_data


def loadEnv():
    config_data = {}  # Dictionary to store configuration data
    
    # Check if .env exists and load its content
    if os.path.exists(dotenv_file_path):
        try:
            load_dotenv(dotenv_file_path)
            for key, value in os.environ.items():
                key = key.upper() # Convert key to uppercase
                config_data[key] = value
        except Exception as e:
            print(f"Error reading .env file: {e}")
    
    return config_data
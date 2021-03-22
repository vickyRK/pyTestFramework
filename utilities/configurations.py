import configparser
import pyodbc


def getConfig():
    config = configparser.ConfigParser()
    config.read('PycharmProjects\\pythonProject\\utilities\\properties.ini')
    return config


server_name = getConfig()['SQL']['server']
db_name = getConfig()['SQL']['database']


def getConnection():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER='+server_name+';'
                                'DATABASE='+db_name+';'
                                'Trusted_Connection=yes;')
        print("Connection successful")
        return conn
    except pyodbc.Error as e:
        print(e)







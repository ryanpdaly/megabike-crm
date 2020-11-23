# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 20:33:20 2020

@author: ryand

Goal: Create the Database Connection Pool for our Megabike CRM
"""

import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

import settings.config
import utilities.util as util

try:
    Credentials = util.read_json('settings/config_database.json')
    
    connection_pool = mysql.pooling.MySQLConnectionPool(pool_name='CRM_pool',
                                                        pool_size=5,
                                                        pool_reset_session=True,
                                                        host = Credentials.get('host'),
                                                        user = Credentials.get('user'),
                                                        passwd = Credentials.get('passwd'),
                                                        database = Credentials.get('database'))
    print("Printing connection pool properties:")
    print("Connection Pool Name - ", connection_pool.pool_name)
    print("Connection Pool Size - ", connection_pool.pool_size,"\n")
        
except Error as e:
    print("Error while connecting to MySQL using Connection pool ", e)

def open_connection():
    connection_object = connection_pool.get_connection()
    
    if connection_object.is_connected():
        db_Info = connection_object.get_server_info()
        print("Connected to MySQL database using connection pool on MySQL Server version on ",db_Info,"\n")
        
    return connection_object

def close_connection(connection_object, cursor):
    #closing database connection
    if(connection_object.is_connected()):
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")
        
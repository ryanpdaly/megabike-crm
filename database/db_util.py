# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:05 2020

@author: ryand

Goal: Create the Database Utilties for our Megabike-CRM Tool
"""

import mysql.connector as mysql
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

try:
	credentials = util.read_json('C:/Python/Megabike_CRM/settins/mysql_credentials.json')

	connection_pool = mysql.pooling.MySQLConnectionPool(**credentials)
    print("Printing connection pool properties:")
    print("Connection Pool Name - ", connection_pool.pool_name)
    print("Connection Pool Size - ", connection_pool.pool_size,"\n")

except Error as e:
	print("Error while connection to MySQL using connection pool: " e)

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
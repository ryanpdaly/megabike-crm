# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:05 2020

@author: ryand

Goal: Create the Database Utilties for our Megabike-CRM Tool
"""

import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

import settings.config
import utilities.util

import database.db_connection_pool as db_pool

class ConnectionPool(mysql.pooling.MySQLConnectionPool):
    def __init__(self, *args, **kwargs):
        mysql.pooling.MySQLConnectionPool.__init__(self, *args, **kwargs)

        try:
            self.Credentials = util.read_json('settings/mysql_credentials.json')
            self.connection_pool = mysql.pooling.MySQLConnectionPool(pool_name='CRM_pool',
                                                                    pool_size=5,
                                                                    pool_reset_session=True,
                                                                    host=self.Credentials.get('host'),
                                                                    user=self.Credentials.get('user'),
                                                                    passwd=self.Credentials.get('passwd'),
                                                                    database=self.Credentials.get('database'))
            print('Printing connection pool properties:')
            print('Connection Pool Name - ', self.connection_pool.pool_name)
            print('Connection Pool Size - ', self.connection_pool.pool_size)
        except Error as error:
            print('Error while connection to MySQL using connection pool ', error)

    def open_connection():
        connection_object = self.connection_pool.get_connection()

        if connection_object.is_connected():
            db_Info = connection_object.get_server_info()
            print('Connected to MySQL Database using connection pool on ',db_Info,'\n')

    def close_connection(connection_object, cursor):
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print('MySQL connection closed')

def check_existence(table, column, criteria):
    command = 'SELECT EXISTS (SELECT * FROM %s WHERE %s = "%s");' %(table, column, criteria)
    check = commit_query(command)
    return(check[0][0])

def commit_entry(sql_command, values):
    connection_object = db_pool.open_connection()
    cursor = connection_object.cursor()
    cursor.execute(sql_command, values)
    connection_object.commit()
    db_pool.close_connection(connection_object, cursor)
    
def commit_query(query):
    connection_object = db_pool.open_connection()
    cursor = connection_object.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db_pool.close_connection(connection_object, cursor)
    return(result)

def execute_script(file):
    temp = open(file, 'r')
    sql_file = temp.read()
    temp.close()
    
    sql_commands = filter(None, sql_file.split(';'))
    
    for command in sql_commands:
        try:
            mysql.cursor.execute(command)
        except mysql.Error as e:
            print('Error while executing:' + command)
            print('Error code:', str(e))
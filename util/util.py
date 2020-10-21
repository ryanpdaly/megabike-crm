# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 07:28:55 2020

@author: ryand
"""

import csv
import json

def configure_list(file):
    with open(file, mode='r') as infile:
        reader = csv.reader(infile)
        i=0
        temp_dict = {}
        for rows in reader:
            temp_dict[rows[0]] = i
            i=i+1.0
            
    return temp_dict

def read_json(file):
    with open(file, 'r') as read_file:
        data = json.load(read_file)
    return(data)

def replace_special(string):
    cleaned=string.translate(str.maketrans({'Ä':'Ae', 'ä':'ae', 'Ö':'Oe',
                                                   'ö':'oe', 'Ü':'Ue', 'ü':'ue',
                                                   'ß':'ss'}))
    return(cleaned)

def write_json(data, file):
    with open(file, 'w') as write_file:
            json.dump(data, write_file)
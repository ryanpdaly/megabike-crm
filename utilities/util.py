# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 07:28:55 2020

@author: ryand
"""

import csv
import json

import tkinter as tk
import tkcalendar

class DateEntry(tkcalendar.DateEntry):
    def get_date(self):
        if not self.get():
            return None
        self._validate_date()
        return self.parse_date(self.get())

class Error(tk.Toplevel):
    def __init__(self, parent, cause):
        tk.Toplevel.__init__(self)

        if cause == 'empty_input':
            err_label=tk.Label(self, text='Bitte alle Eingabefelder ausfüllen',
                font=config.Settings.headerfont)
            err_label.pack()

        print('The error function works')
        self.mainloop()

def check_inputs(INPUTS, DATES):
    test=True
    for input_ in INPUTS:
        if len(input_.get())==False:
            return(False)
    for date in DATES:
        if date.get_date() ==None:
            return(False)
    return(test)

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

def reset_inputs(INPUTS, DATES):
    for input_ in INPUTS:
        input_.delete(0, tk.END)
    for date in DATES:
        date.delete(0, tk.END)

def write_json(data, file):
    with open(file, 'w') as write_file:
            json.dump(data, write_file)
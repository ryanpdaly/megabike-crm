# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 06:38:13 2020

@author: ryand
"""

import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

import utilities.util as util
import database.db_util as db_util

class Settings():
    # Create font objects!
    titlefont=('Bahnschrift', 14, 'bold')
    headerfont=('Bahnschrift', 12, 'bold')
    subheaderfont=('Bahnschrift', 10, 'bold')
    labelfont=('Bahnschrift', 10)
    dateformat='YYYY-MM-DD'

    # Database Settings
    host='localhost'
    user='root'
    passwd='$TOREthatDATA666'
    database='megabikecrm'

    # Warranty Settings
    faellig_gelb=4
    faellig_rot=7

settings = Settings()

class Gesamt(tk.Toplevel):
    #titlefont=tkFont.Font(root, family='Bahnschrift', size=14, weight='bold')
    def __init__(self, parent):
        tk.Toplevel.__init__(self)

        self.file = 'settings/config_gesamt.json'

        self.title('Megabike-CRM: Gesamteinstellung')

        self.inputFrame=tk.Frame(self)
        self.inputFrame.grid(row=0, column=0)

        self.controlFrame=tk.Frame(self)
        self.controlFrame.grid(row=1, column=0)

        DATEFORMATS=('YYYY-MM-DD', 'DD.MM.YY', 'DD.MM.YYYY')

        #LABELS =('TEXT', COLUMN, ROW)
        LABELS=(('Title Font:',0,0),
                ('Header Font:',0,1),
                ('Subheader Font:',0,2),
                ('Label Font:',0,3),
                ('Date Format:',0,4))

        for label in LABELS:
            temp_label=tk.Label(self.inputFrame, text=label[0])
            temp_label.grid(column=label[1], row=label[2], padx=2, pady=5)

        self.input_titlefont=tk.Entry(self.inputFrame)
        self.input_titlefont.grid(row=0, column=1, padx=5, pady=2)
        
        self.input_headerfont=tk.Entry(self.inputFrame)
        self.input_headerfont.grid(row=1, column=1, padx=5, pady=2)

        self.input_subheaderfont=tk.Entry(self.inputFrame)
        self.input_subheaderfont.grid(row=2, column=1, padx=5, pady=2)

        self.input_labelfont = tk.Entry(self.inputFrame)
        self.input_labelfont.grid(row=3, column=1, padx=5, pady=2)        

        self.input_dateformat=ttk.Combobox(self.inputFrame, value=DATEFORMATS)
        self.input_dateformat.grid(row=4, column=1, padx=4, pady=2)

        self.SETTINGS=util.read_json(self.file)
        self.input_titlefont.insert(0, settings.titlefont)
        self.input_headerfont.insert(0, self.SETTINGS.get('headerfont'))
        self.input_subheaderfont.insert(0, self.SETTINGS.get('subheaderfont'))
        self.input_labelfont.insert(0, self.SETTINGS.get('labelfont'))

    def read_settings(self):
        pass

    def save_changes(self):
        pass

class MenuRekla(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.file = 'settings/config_rekla.json'
        
        self.title('Megabike-CRM: Reklamationseinstellung')
        
        # Inputs go here
        self.inputFrame = tk.Frame(self)
        self.inputFrame.grid(row=0, column=0)
        
        self.label_faellig1 = tk.Label(self.inputFrame, text='Fällig Gelb:')
        self.label_faellig1.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        self.input_faellig1 = tk.Entry(self.inputFrame)
        self.input_faellig1.grid(row=0, column=1, padx=5, pady=2)
        
        self.label_faellig2 = tk.Label(self.inputFrame, text='Fällig Rot:')
        self.label_faellig2.grid(row=1, column=0, padx=2, pady=2, sticky='w')
        self.input_faellig2 = tk.Entry(self.inputFrame)
        self.input_faellig2.grid(row=1, column=1, padx=5, pady=2)
        
        # Controls go here
        self.controlFrame = tk.Frame(self)
        self.controlFrame.grid(row=1, column=0)        

        self.button_save = tk.Button(self.controlFrame, text='Speichern', command=lambda: self.save_changes())
        self.button_save.grid(row=0, column=0, padx=2, pady=2, columnspan=2)

        try:
            self.SETTINGS = util.read_json(self.file)
            self.input_faellig1.insert(0, self.SETTINGS.get('faellig_gelb'))
            self.input_faellig2.insert(0, self.SETTINGS.get('faellig_rot'))
        except:
            print("This didn't work for some reason")

    def save_changes(self):
        settings = {'faellig1' : input_faellig1.get(),
                    'faellig2' : input_faellig2.get(),
                    'labelfont' : input_labelfont.get()}
        util.write_json(settings, file)

class MenuDatabase(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.file = 'settings/config_database.json'
    
        self.title('MegabikeCRM: MySQL Server Credentials')

        self.inputFrame = tk.Frame(self)
        self.inputFrame.grid(row=0, column=0)
        
        self.controlFrame = tk.Frame(self)
        self.controlFrame.grid(row=1, column=0)
        
        self.label_host = tk.Label(self.inputFrame, text='Host:')
        self.label_host.grid(row=1, column=0, padx=2, pady=2, sticky='w')
        
        self.label_user = tk.Label(self.inputFrame, text='User:')
        self.label_user.grid(row=2, column=0, padx=2, pady=2, sticky='w')
        
        self.label_passwd = tk.Label(self.inputFrame, text='Password:')
        self.label_passwd.grid(row=3, column=0, padx=2, pady=2, sticky='w')
        
        self.label_database = tk.Label(self.inputFrame, text='Database:')
        self.label_database.grid(row=4, column=0, padx=2, pady=2, sticky='w')
        
        self.input_host = tk.Entry(self.inputFrame)
        self.input_host.grid(row=1, column=1, padx=5, pady=2)
        
        self.input_user = tk.Entry(self.inputFrame)
        self.input_user.grid(row=2, column=1, padx=5, pady=2)
        
        self.input_passwd = tk.Entry(self.inputFrame)
        self.input_passwd.grid(row=3, column=1, padx=5, pady=2)
        
        self.input_database = tk.Entry(self.inputFrame)
        self.input_database.grid(row=4, column=1, padx=5, pady=2)
        
        self.button_save = tk.Button(self.controlFrame, text='Speichern', 
                                command=lambda: save_changes())
        self.button_save.grid(row=5, column=0, padx=2, pady=2, columnspan=2)
        
        try:
            CREDENTIALS = util.read_json(self.file)
            self.input_host.insert(0, CREDENTIALS.get('host'))
            self.input_user.insert(0, CREDENTIALS.get('user'))
            self.input_passwd.insert(0, CREDENTIALS.get('passwd'))
            self.input_database.insert(0, CREDENTIALS.get('database'))
        except:
            pass
    
    def save_changes(self):
        data = {'host' : input_host.get(),
                'user' : input_user.get(),
                'passwd' : input_passwd.get(),
                'database' : input_database.get()}
        util.write_json(data, file)
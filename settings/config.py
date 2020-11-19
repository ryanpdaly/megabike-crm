# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 06:38:13 2020

@author: ryand
"""

import json
import tkinter as tk

import utilities.util as util
import database.db_util as db_util

class SettingsMain(tk.Frame):
    def __init__():
    
        selectFrame = tk.Frame(root)
        selectFrame.pack()
        
        button_server = tk.Button(selectFrame, text='SQL Server Einstellungen',
                              command=lambda: mysql_credentials())
        button_gui = tk.Button(selectFrame, text='GUI Einstellungen',
                               command=lambda: gui_config())
        
        button_server.grid(row=0, column=0, padx=5, pady=5)
        button_gui.grid(row=1, column=0, padx=5, pady=5)

class SettingsGUI(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)

        file = ''

        self.title('Megabike-CRM: Gesamteinstellung')

        self.label_labelfont = tk.Label(inputFrame, text='Label Font:')
        self.label_labelfont.grid(row=2, column=0, padx=2, pady=2, sticky='w')
        self.input_labelfont = tk.Entry(inputFrame)
        self.input_labelfont.grid(row=2, column=1, padx=5, pady=2)        

class SettingsRekla(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.file = 'settings/GUI_config.json'
        
        self.title('Megabike-CRM: Reklamationseinstellung')
        
        self.inputFrame = tk.Frame(self)
        self.inputFrame.grid(row=0, column=0)
        
        self.controlFrame = tk.Frame(self)
        self.controlFrame.grid(row=1, column=0)
        
        self.label_faellig1 = tk.Label(self.inputFrame, text='Fällig Gelb:')
        self.label_faellig1.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        self.input_faellig1 = tk.Entry(self.inputFrame)
        self.input_faellig1.grid(row=0, column=1, padx=5, pady=2)
        
        self.label_faellig2 = tk.Label(self.inputFrame, text='Fällig Rot:')
        self.label_faellig2.grid(row=1, column=0, padx=2, pady=2, sticky='w')
        self.input_faellig2 = tk.Entry(self.inputFrame)
        self.input_faellig2.grid(row=1, column=1, padx=5, pady=2)
        
        self.button_save = tk.Button(self.controlFrame, text='Speichern', command=lambda: self.save_changes())
        self.button_save.grid(row=0, column=0, padx=2, pady=2, columnspan=2)

        try:
            self.SETTINGS = util.read_json(self.file)
            self.input_faellig1.insert(0, self.SETTINGS.get('faellig1'))
            self.input_faellig2.insert(0, self.SETTINGS.get('faellig2'))
        except:
            print("This didn't work for some reason")

    def save_changes(self):
        settings = {'faellig1' : input_faellig1.get(),
                    'faellig2' : input_faellig2.get(),
                    'labelfont' : input_labelfont.get()}
        util.write_json(settings, file)

class SettingsDatabase(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.file = 'settings/mysql_credentials.json'
    
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
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 06:38:13 2020

@author: ryand
"""

import json
import tkinter as tk

import utilities.util as util
import database.db_util as db_util

def main():
    root = tk.Tk()
    
    selectFrame = tk.Frame(root)
    selectFrame.pack()
    
    button_server = tk.Button(selectFrame, text='SQL Server Einstellungen',
                          command=lambda: mysql_credentials())
    button_gui = tk.Button(selectFrame, text='GUI Einstellungen',
                           command=lambda: gui_config())
    
    button_server.grid(row=0, column=0, padx=5, pady=5)
    button_gui.grid(row=1, column=0, padx=5, pady=5)
    
    root.mainloop()

def gui_config():
    
    file = 'settings/GUI_config.json'
    
    def read_values():
        settings = {'faellig1' : input_faellig1.get(),
                    'faellig2' : input_faellig2.get(),
                    'labelfont' : input_labelfont.get()}
        util.write_json(settings, file)
    
    root=tk.Tk()
    root.title('MegabikeCRM: GUI Configuration')
    
    inputFrame = tk.Frame(root)
    inputFrame.grid(row=0, column=0)
    
    controlFrame = tk.Frame(root)
    controlFrame.grid(row=1, column=0)
    
    label_faellig1 = tk.Label(inputFrame, text='Fällig Gelb:')
    label_faellig1.grid(row=0, column=0, padx=2, pady=2, sticky='w')
    input_faellig1 = tk.Entry(inputFrame)
    input_faellig1.grid(row=0, column=1, padx=5, pady=2)
    
    label_faellig2 = tk.Label(inputFrame, text='Fällig Rot:')
    label_faellig2.grid(row=1, column=0, padx=2, pady=2, sticky='w')
    input_faellig2 = tk.Entry(inputFrame)
    input_faellig2.grid(row=1, column=1, padx=5, pady=2)
    
    
    label_labelfont = tk.Label(inputFrame, text='Label Font:')
    label_labelfont.grid(row=2, column=0, padx=2, pady=2, sticky='w')
    input_labelfont = tk.Entry(inputFrame)
    input_labelfont.grid(row=2, column=1, padx=5, pady=2)    
    
    button_save = tk.Button(controlFrame, text='Speichern', command=read_values)
    button_save.grid(row=0, column=0, padx=2, pady=2, columnspan=2)
    
    try:
        Settings = util.read_json(file)
        input_faellig1.insert(0, Settings.get('faellig1'))
        input_faellig2.insert(0, Settings.get('faellig2'))
    except:
        pass
    
def mysql_credentials():
    
    file = 'settings/mysql_credentials.json'
    
    def read_inputs():
        data = {'host' : input_host.get(),
                'user' : input_user.get(),
                'passwd' : input_passwd.get(),
                'database' : input_database.get()}
        util.write_json(data, file)
    
    root=tk.Tk()
    root.title('MegabikeCRM: MySQL Server Credentials')

    inputFrame = tk.Frame(root)
    inputFrame.grid(row=0, column=0)
    
    controlFrame = tk.Frame(root)
    controlFrame.grid(row=1, column=0)
    
    label_host = tk.Label(inputFrame, text='Host:')
    label_host.grid(row=1, column=0, padx=2, pady=2, sticky='w')
    
    label_user = tk.Label(inputFrame, text='User:')
    label_user.grid(row=2, column=0, padx=2, pady=2, sticky='w')
    
    label_passwd = tk.Label(inputFrame, text='Password:')
    label_passwd.grid(row=3, column=0, padx=2, pady=2, sticky='w')
    
    label_database = tk.Label(inputFrame, text='Database:')
    label_database.grid(row=4, column=0, padx=2, pady=2, sticky='w')
    
    input_host = tk.Entry(inputFrame)
    input_host.grid(row=1, column=1, padx=5, pady=2)
    
    input_user = tk.Entry(inputFrame)
    input_user.grid(row=2, column=1, padx=5, pady=2)
    
    input_passwd = tk.Entry(inputFrame)
    input_passwd.grid(row=3, column=1, padx=5, pady=2)
    
    input_database = tk.Entry(inputFrame)
    input_database.grid(row=4, column=1, padx=5, pady=2)
    
    button_save = tk.Button(controlFrame, text='Speichern', 
                            command=lambda: read_inputs)
    button_save.grid(row=5, column=0, padx=2, pady=2, columnspan=2)
    
    try:
        Credentials = util.read_json(file)
        input_host.insert(0, Credentials.get('host'))
        input_user.insert(0, Credentials.get('user'))
        input_passwd.insert(0, Credentials.get('passwd'))
        input_database.insert(0, Credentials.get('database'))
    except:
        pass
    
    root.mainloop()
        

if __name__ == '__main__':
    #mysql_credentials()
    main()
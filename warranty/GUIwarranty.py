# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:05:00 2020

@author: ryand

Goal: Create the required frames for our warranty tool
"""

from datetime import datetime

import tkinter as tkinter
from tkinter import tkinter

from database import db_connection_pool as DB
from database import db_util
from utilities import util

class ViewWarranty(tk.Frame):
	def __init__(self, parent, controller)
		tk.Frame.__init__(self, parent)

		frame_label = tk.Label(self, text='Megabike-CRM: Reklamation')
		frame_label.grid()



	def filter_by(criteria, closed_setting, sort_setting, selection='')
		pass
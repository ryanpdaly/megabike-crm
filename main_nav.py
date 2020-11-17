# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:35:00 2020

@author: ryand

Goal: Create a main navigation screen for our Megabike-CRM tool
"""

import tkinter as tk
from tkinter import ttk

from datetime import datetime

import database.db_util
import warranty.GUIwarranty as rekla

LARGE_FONT = ('Verdana', 12)

class MainNav(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)

		container.pack(side='top', fill='both', expand=True)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		container.title=('Megabike-CRM')

		self.frames = {}

		WINDOWS_MAIN = (NavFrame, rekla.ViewWarranty)

		for window in WINDOWS_MAIN:
		
			frame = window(container, self)
			self.frames[window] = frame

			frame.grid(row=0, column=0, sticky='nsew')

		self.show_frame(NavFrame)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


	def new_window(self, cont):
		pass

class NavFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		frame_label = tk.Label(self, text='Megabike-CRM: Nav Screen', font=LARGE_FONT)
		frame_label.grid(column=0, row=0, columnspan=4, pady=10)

		contact_button = tk.Button(self, text='Kundenkontakt',
										command='',
										height=5, width=20)
		contact_button.grid(column=0, row=1, padx=5, pady=5)

		insurance_button = tk.Button(self, text='Versicherunsbereich',
									command='',
									height=5, width=20)
		insurance_button.grid(column=1, row=1, padx=5, pady=5)

		warranty_button = tk.Button(self, text='Reklamationsbereich',
									command = lambda: controller.show_frame(rekla.ViewWarranty),
									height=5, width=20)
		warranty_button.grid(column=2, row=1, padx=5, pady=5)

app = MainNav()
app.title('Megabike CRM')
app.mainloop()
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:35:00 2020

@author: ryand

Goal: Create a main navigation screen for our Megabike-CRM tool
"""

import tkinter as tk
from tkinter import ttk

from datetime import datetime

import warranty.GUIwarranty as rekla
import insurance.GUIinsurance as vers
import settings.config as config

class MainNav(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.menuBar=MenuBar(self)

		container = tk.Frame(self)
		container.pack(side='bottom', fill='both', expand=True)
		container.title=('Megabike-CRM')

		self.frames = {}

		self.WINDOWS_MAIN = (NavFrame, rekla.ViewWarranty, vers.SearchInsurance, vers.InputInsurance)

		for window in self.WINDOWS_MAIN:
			frame = window(container, self)
			self.frames[window] = frame
			frame.grid(row=0, column=0, sticky='nsew')

		self.show_frame(NavFrame)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class NavFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.columnconfigure((1,2), weight=1)
		self.rowconfigure((1), weight=1)

		frame_label = tk.Label(self, text='Megabike-CRM: Nav Screen', font=config.settings.titlefont)
		frame_label.grid(column=0, row=0, columnspan=4, pady=10)

		#contact_button = tk.Button(self, text='Kundenkontakt', font=config.settings.headerfont,
		#								command='')
		#contact_button.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW)

		insurance_button = tk.Button(self, text='Versicherungsbereich', font=config.settings.headerfont,
									command=lambda: controller.show_frame(vers.SearchInsurance))
		insurance_button.grid(column=1, row=1, padx=5, pady=5, sticky=tk.NSEW)

		warranty_button = tk.Button(self, text='Reklamationsbereich', font=config.settings.headerfont,
									command = lambda: controller.show_frame(rekla.ViewWarranty))
		warranty_button.grid(column=2, row=1, padx=5, pady=5, sticky=tk.NSEW)

class MenuBar(tk.Menu):
	def __init__(self, parent):
		tk.Menu.__init__(self, parent)

		self.add_command(label='Main', command=lambda: parent.show_frame(NavFrame))
		self.add_separator()
		self.add_command(label='Versicherung suchen',  command=lambda: parent.show_frame(vers.SearchInsurance))
		self.add_command(label='Versicherug eingeben', command=lambda: parent.show_frame(vers.InputInsurance))
		self.add_separator()
		self.add_command(label='Reklamation', command=lambda: parent.show_frame(rekla.ViewWarranty))

		'''
		self.jump_to = tk.Menu(self, tearoff=1)
		self.jump_to.add_command(label='Navigation', command=lambda: parent.show_frame(NavFrame))
		#self.jump_to.add_command(label='Telefonnotiz', command='')
		#self.jump_to.add_command(label='Kundenkontakt', command='')
		self.jump_to.add_command(label='Versicherungsinfo', command=lambda: parent.show_frame(vers.SearchInsurance))
		self.jump_to.add_command(label='Reklamation', command=lambda: parent.show_frame(rekla.ViewWarranty))
		self.add_cascade(label='Jump To', menu=self.jump_to)

		self.add_separator()

		self.settings = tk.Menu(self, tearoff=0)
		self.settings.add_command(label='Gesamt', command=lambda: config.Gesamt(self))
		self.settings.add_command(label='Reklamation', command=lambda: config.MenuRekla(self))
		self.settings.add_command(label='Versicherung', command='')
		self.settings.add_command(label='Database', command=lambda: config.MenuDatabase(self))
		#self.add_cascade(label='Settings', menu=self.settings)
		'''

app = MainNav()
app.title('Megabike-CRM')
app.config(menu=MenuBar(app))
app.mainloop()
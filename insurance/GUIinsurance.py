# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:17:30

@author: ryand

Goal: Create the required classes and methods for our Insurance GUI
"""

from datetime import datetime

import tkinter as tk
from tkinter import ttk

import utilities.autoscroll as autoscroll

class SearchInsurance(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.frame_label=tk.Label(self, text='Megabike-CRM: Versicherung')
		self.frame_label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.controlFrame.grid(column=0, row=1, pady=2)

		self.button_rahmennr=tk.Button(self.controlFrame, text='Nach Rahmennummer', width=18)
		self.button_rahmennr.grid(column=0, row=0, padx=5, pady=2)
		self.input_rahmennr=tk.Entry(self.controlFrame)
		self.input_rahmennr.grid(column=0, row=1, padx=5, pady=2)

		self.button_policenr=tk.Button(self.controlFrame, text='Nach Policenummer', width=18)
		self.button_policenr.grid(column=1, row=0, padx=5, pady=2)
		self.input_policenr=tk.Entry(self.controlFrame)
		self.input_policenr.grid(column=1, row=1, padx=5, pady=2)

		self.button_kdnr=tk.Button(self.controlFrame, text='Nach Kundennr', width=18,
			command='')
		self.button_kdnr.grid(column=5, row=0, padx=5, pady=2)
		self.input_kdnr=tk.Entry(self.controlFrame)
		self.input_kdnr.grid(column=5, row=1, padx=5, pady=2)

		self.input_insurance=tk.Button(self.controlFrame, text='Input Insurance Info', width=15, height=5,
			command=lambda: controller.show_frame(InputInsurance))
		self.input_insurance.grid(column=6, row=0, rowspan=2, padx=5, pady=2)

		self.viewFrame=autoscroll.ScrollableFrame(self, relief=tk.RAISED, height=200, width=600)
		self.viewFrame.grid(column=0, row=2, pady=2)

		for i in range(50):
			tk.Label(self.viewFrame.frame, text=i).grid(row=i, column=0)

class InputInsurance(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.frame_label=tk.Label(self, text='Megabike-CRM: Versicherung eintragen')
		self.frame_label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.controlFrame.grid(column=0, row=1)

		self.inputFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.inputFrame.grid(column=0, row=2)

		self.COMPANIES = (Assona,
							Businessbike,
							BikeleasingService,
							ENRA,
							EuroRad,
							JobRad,
							MeinDienstrad)

		self.anbieter = tk.StringVar()
		self.anbieter.set('Businessbike')

		for index, company in enumerate(self.COMPANIES):
			radio=tk.Radiobutton(self.controlFrame, text=company.__name__, width=15, 
				variable=self.anbieter, value=company, indicatoron=0,
				command=lambda frame=company: self.show_frame(frame))
			radio.grid(column=index, row=1, padx=3, pady=2)

		self.save=tk.Button(self.controlFrame, text='Speichern', height=3, width=30,
			command='')
		self.save.grid(column=(len(self.COMPANIES)//2)-2, row=0, columnspan=2, pady=5)

		self.reset=tk.Button(self.controlFrame, text='Reset', height=3, width=30,
			command='')
		self.reset.grid(column=(len(self.COMPANIES)//2)+1, row=0, columnspan=2, pady=5)

		self.frames = {}

		FRAME_INSURANCE = (Assona, Businessbike, BikeleasingService, ENRA, EuroRad, JobRad, MeinDienstrad)

		for F in FRAME_INSURANCE:
			frame = F(self.inputFrame)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky=tk.NSEW)

		self.show_frame(Businessbike)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def save_inputs(self):
		pass

class Assona(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table = 'assona'

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Vertragsnummer:',0,1),
					('Fahrrad:',0,2),
					('Rahmennummer:',0,3))

		for label in LABELS:
			temp_label=tk.Label(self, text=label[0])
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5)

		self.input_kdnr=tk.Entry(self)
		self.input_kdnr.grid(column=1, row=0)

		self.input_vertragsnr=tk.Entry(self)
		self.input_vertragsnr.grid(column=1, row=1)

		self.input_bike=tk.Entry(self)
		self.input_bike.grid(column=1, row=2)

		self.input_rahmennr=tk.Entry(self)
		self.input_rahmennr.grid(column=1, row=3)

class Businessbike(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table='businessbike'

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Leasingnutzer:',0,1),
					('Fahrrad:',0,2),
					('Rahmennummer:',0,3),
					('Leasinglaufzeit:',0,4),
					('Policenummer:',0,5),
					('Service-Paket:',0,6))

		for label in LABELS:
			temp_label=tk.Label(self, text=label[0])
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5)

		self.input_kdnr=tk.Entry(self)
		self.input_kdnr.grid(column=1, row=0, columnspan=3, padx=2, pady=5)

		self.input_nutzer=tk.Entry(self)
		self.input_nutzer.grid(column=1, row=1, columnspan=3, padx=2, pady=5)

		self.input_bike=tk.Entry(self)
		self.input_bike.grid(column=1, row=2, columnspan=3, padx=2, pady=5)

		self.input_rahmennr=tk.Entry(self)
		self.input_rahmennr.grid(column=1, row=3, columnspan=3, padx=2, pady=5)

		self.input_beginn=tk.Entry(self, width=8)
		self.input_beginn.grid(column=1, row=4, padx=0, pady=5)
		self.label_bis=tk.Label(self, text='bis')
		self.label_bis.grid(column=2, row=4, padx=2, pady=5)
		self.input_ende=tk.Entry(self, width=8)
		self.input_ende.grid(column=3, row=4, padx=0, pady=5)

		self.input_policenr=tk.Entry(self)
		self.input_policenr.grid(column=1, row=5, columnspan=3, padx=2, pady=5)

		self.input_paket=tk.Entry(self)
		self.input_paket.grid(column=1, row=6, columnspan=3, padx=2, pady=5)

class BikeleasingService(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table = 'bikeleasing_service'

		self.Label=tk.Label(self, text='BikeleasingService')
		self.Label.grid(column=0, row=0)

class ENRA(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table='enra'

		self.Label=tk.Label(self, text='ENRA')
		self.Label.grid(column=0, row=0)

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Nutzer:',0,1),
					('Fahrrad:',0,2),
					('Rahmennummer:',0,3),
					('Beginn:',0,4),
					('Policenummer:',0,5))

		for label in LABELS:
			temp_label=tk.Label(self, text=label[0])
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5)

		self.input_kdnr=tk.Entry(self)
		self.input_kdnr.grid(column=1, row=0, padx=2, pady=5)

		self.input_nutzer=tk.Entry(self)
		self.input_nutzer.grid(column=1, row=1, padx=2, pady=5)

		self.input_bike=tk.Entry(self)
		self.input_bike.grid(column=1, row=2, padx=2, pady=5)

		self.input_rahmennr=tk.Entry(self)
		self.input_rahmennr.grid(column=1, row=3, padx=2, pady=5)

		self.input_beginn=tk.Entry(self)
		self.input_beginn.grid(column=1, row=4, padx=2, pady=5)

		self.input_policenr=tk.Entry(self)
		self.input_policenr.grid(column=1, row=5, padx=2, pady=5)

class EuroRad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table='eurorad'

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Vertragsnummer:',0,1),
					('Rahmennummer:',0,2))

		for label in LABELS:
			temp_label=tk.Label(self, text=label[0])
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5)

		self.input_kdnr=tk.Entry(self)
		self.input_kdnr.grid(column=1, row=0)

		self.input_vertragsnr=tk.Entry(self)
		self.input_vertragsnr.grid(column=1, row=1)

		self.input_rahmennr=tk.Entry(self)
		self.input_rahmennr.grid(column=1, row=2)

class JobRad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table = 'jobrad'

		self.Label=tk.Label(self, text='JobRad')
		self.Label.grid(column=0, row=0)

class MeinDienstrad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.table = 'mein_dienstrad'

		self.Label=tk.Label(self, text='MeinDienstrad')
		self.Label.grid(column=0, row=0)
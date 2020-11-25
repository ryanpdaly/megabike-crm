# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:17:30

@author: ryand

Goal: Create the required classes and methods for our Insurance GUI
"""

from datetime import date

import tkcalendar as tkcal
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import utilities.util as util
import utilities.autoscroll as autoscroll
import settings.config as config
import database.db_util as db_util

class SearchInsurance(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)

		self.frame_label=tk.Label(self, text='Megabike-CRM: Versicherung Suche',
			font=config.Settings.titlefont)
		self.frame_label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.controlFrame.grid(column=0, row=1, pady=2)

		self.button_kdnr=tk.Button(self.controlFrame, text='Nach Kundennr', 
			font=config.Settings.subheaderfont, width=18,
			command=lambda: self.search_versicherung('kdnr', self.input_kdnr))
		self.button_kdnr.grid(column=1, row=0, padx=5, pady=2)
		self.input_kdnr=tk.Entry(self.controlFrame, font=config.Settings.subheaderfont,)
		self.input_kdnr.grid(column=1, row=1, padx=5, pady=2)		

		self.button_rahmennr=tk.Button(self.controlFrame, text='Nach Rahmennummer', 
			font=config.Settings.subheaderfont, width=18,
			command=lambda: self.search_versicherung('rahmennr', self.input_rahmennr))
		self.button_rahmennr.grid(column=2, row=0, padx=5, pady=2)
		self.input_rahmennr=tk.Entry(self.controlFrame, font=config.Settings.subheaderfont)
		self.input_rahmennr.grid(column=2, row=1, padx=5, pady=2)


		VERSICHERUNGEN = ('Assona', 'Bikeleasing', 'Businessbike', 'ENRA', 'EuroRad')
		self.button_insurance=tk.Button(self.controlFrame, text='Nach Versicherung',
			font=config.Settings.subheaderfont, width=18,
			command=lambda:self.search_versicherung('versicherung', self.input_insurance))
		self.button_insurance.grid(column=3, row=0, padx=5, pady=2)
		self.input_insurance=ttk.Combobox(self.controlFrame, font=config.Settings.subheaderfont,
				width=15, values=VERSICHERUNGEN)
		self.input_insurance.grid(column=3, row=1, padx=5, pady=2)
		'''
		self.input_insurance=tk.Entry(self.controlFrame, font=config.Settings.subheaderfont,)
		self.input_insurance.grid(column=3, row=1, padx=5, pady=2)
		'''
		self.button_insurance_erfassen=tk.Button(self.controlFrame, text='Input Insurance Info', 
			font=config.Settings.subheaderfont, width=20, height=5,
			command=lambda: controller.show_frame(InputInsurance))
		self.button_insurance_erfassen.grid(column=4, row=0, rowspan=2, padx=5, pady=2)

		self.viewFrame=autoscroll.ScrollableFrame(self, relief=tk.RAISED, bd=3, height=200, width=700)
		self.viewFrame.grid(column=0, row=2, pady=2)

		self.policeFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.policeFrame.grid(column=0, row=3, pady=2)

	def clean_inputs(self):
		if self.criteria == 'kdnr':
			self.input_rahmennr.delete(0, tk.END)
			self.input_insurance.delete(0, tk.END)
		elif self.criteria == 'rahmennr':
			self.input_kdnr.delete(0, tk.END)
			self.input_insurance.delete(0, tk.END)
		elif self.criteria == 'versicherung':
			self.input_kdnr.delete(0, tk.END)
			self.input_rahmennr.delete(0, tk.END)

	def display_results(self):
		#LABELS=(TEXT, COLUMN, ROW)
		LABELS = (('Kundennummer:',0,0),
					('Fahrrad:',1,0),
					('Rahmennummer:',2,0),
					('Versicherung:',3,0))

		for label in LABELS:
			temp_label = tk.Label(self.viewFrame.frame, text=label[0],
					font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=8, pady=2)

		for index, result in enumerate(self.result):
			num=0
			index += 2
			for subindex, value in enumerate(result):
				lookup_label=tk.Label(self.viewFrame.frame, text=value, 
					font=config.settings.labelfont)
				lookup_label.grid(column=num, row=index, padx=8, pady=5)
				num+=1
			view_result=tk.Button(self.viewFrame.frame, text='Anzeigen',
				font=config.Settings.labelfont, width=15,
				command=lambda info=result: self.show_police(info))
			view_result.grid(column=num+1, row=index, padx=8, pady=5)

	def go_back(self, parent, controller):
		pass

	def search_versicherung(self, criteria, selection):
		self.criteria=criteria
		self.selection=selection
		self.viewFrame.clear_canvas()
		self.query_vers_all()
		self.clean_inputs()
		self.display_results()

	def query_vers_all(self):
		#self.criteria=criteria
		self.query = 'SELECT * FROM vers_all \
			WHERE (%s = "%s") ORDER by kdnr DESC' % (self.criteria, self.selection.get())
		self.result=db_util.commit_query(self.query)

	def show_police(self, info):
		for child in self.policeFrame.winfo_children():
			child.destroy()

		ANBIETER = {'assona':Assona,
					'bikeleasing':BikeleasingService,
					'businessbike':Businessbike,
					'enra':ENRA,
					'eurorad':EuroRad}

		vers_in = ANBIETER.get(info[3])

		title=tk.Label(self.policeFrame, text=vers_in.__name__, font=config.Settings.headerfont)
		title.grid(column=0, row=0)

		displayFrame=vers_in(self.policeFrame)
		displayFrame.kdnr=info[0]
		displayFrame.fahrrad=info[1]
		displayFrame.rahmennr=info[2]
		displayFrame.versicherung=info[3]

		displayFrame.query_vertrag()
		displayFrame.fill_inputs()
		displayFrame.grid(column=0, row=1)

class InputInsurance(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)

		self.frame_label=tk.Label(self, text='Megabike-CRM: Versicherung Eingabe',
			font=config.Settings.titlefont)
		self.frame_label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.controlFrame.grid(column=0, row=1, padx=5, pady=20)

		self.inputFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.inputFrame.grid(column=0, row=2)

		self.COMPANIES = (Assona,
							BikeleasingService,
							Businessbike,
							ENRA,
							EuroRad)		


		self.anbieter = tk.StringVar()
		self.anbieter.set('Businessbike')	

		for index, company in enumerate(self.COMPANIES):
			radio=tk.Radiobutton(self.controlFrame, text=company.__name__, 
				font=config.Settings.subheaderfont, width=20, height=2, 
				variable=self.anbieter, value=company, indicatoron=0,
				command=lambda frame=company: self.show_frame(frame))
			radio.grid(column=index, row=1, padx=10, pady=10)

		self.nav_insurance(self.inputFrame)

	def nav_insurance(self, frame_in):
		self.frames = {}

		for F in self.COMPANIES:
			frame = F(frame_in)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky=tk.NSEW)

		self.show_frame(Businessbike)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def go_back(self, parent, controller):
		pass

class Assona(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0, sticky=tk.EW)
		self.inputFrame.columnconfigure((0,1), weight=1)

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Fahrrad:',0,1),
					('Rahmennummer:',0,2),
					('Vertragsnummer:',0,3),
					('Beginn:',0,4))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kdnr.grid(column=1, row=0)

		self.input_bike=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_bike.grid(column=1, row=1)

		self.input_rahmennr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_rahmennr.grid(column=1, row=2)

		self.input_vertragsnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_vertragsnr.grid(column=1, row=3)

		self.input_beginn=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyyy', 
			locale='de_DE', font=config.Settings.labelfont)
		self.input_beginn.delete(0, tk.END)
		self.input_beginn.grid(column=1, row=4)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)
		
		self.button_reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont,
			command=lambda: self.reset_inputs())
		self.button_reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.button_save=tk.Button(self.controlFrame, text='Speichern', font=config.Settings.headerfont,
			command=lambda: self.save())
		self.button_save.grid(column=1, row=0, padx=5, sticky=tk.EW)

		self.INPUTS = (self.input_kdnr, self.input_bike, self.input_rahmennr, self.input_vertragsnr)
		self.DATES = (self.input_beginn,)

	def fill_inputs(self):
		to_destroy=(self.input_kdnr, self.input_bike, self.input_rahmennr, 
			self.input_vertragsnr, self.input_beginn, self.button_reset, self.button_save)
		for widget in to_destroy:
			widget.destroy()

		#LABELS=VARIABLE, COLUMN, ROW
		LABELS=((self.kdnr,1,0),
				(self.fahrrad,1,1),
				(self.rahmennr,1,2),
				(self.vertragsnr,1,3),
				(self.beginn.strftime('%d.%m.%Y'),1,4))

		for label in LABELS:
			self.temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.labelfont)
			self.temp_label.grid(column=label[1], row=label[2])

	def query_vertrag(self):
		query = 'SELECT vertragsnr, beginn FROM vers_assona WHERE (rahmennr="%s")' % (self.rahmennr)
		result=db_util.commit_query(query)
		
		self.vertragsnr=result[0][0]
		self.beginn=result[0][1]

	def reset_inputs(self):
		for input_ in self.INPUTS:
			input_.delete(0, tk.END)
		for date in self.DATES:
			date.delete(0, tk.END)

	def save(self):
		all_command="INSERT INTO vers_all (kdnr, fahrrad, rahmennr, versicherung) \
			VALUES (%s, %s, %s, 'assona')"
		all_values=(self.input_kdnr.get(), self.input_bike.get(), self.input_rahmennr.get())

		anbieter_command="INSERT INTO vers_assona (vertragsnr, rahmennr, beginn) \
			VALUES (%s, %s, %s)"
		anbieter_values=(self.input_vertragsnr.get(), self.input_rahmennr.get(),
			self.input_beginn.get_date())

		if util.check_inputs(self.INPUTS, self.DATES):
			try:
				db_util.commit_entry(all_command, all_values)
				db_util.commit_entry(anbieter_command, anbieter_values)
				self.reset_inputs()
			except:
				print("Failed to save Assona")
		else:
			err_window=messagebox.showerror(title='Eingabefeld leer', message='Alle Felder sind erforderlich!')

class BikeleasingService(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0, sticky=tk.EW)
		self.inputFrame.columnconfigure((0,1), weight=1)

		#LABELS=('TEXT',COLUMN,ROW)
		LABELS=(('Kundennummer:',0,0),
				('Fahrrad:',0,1),
				('Rahmennummer:',0,2),
				('Nutzer-ID:',0,3),
				('Service-Paket:',0,4),
				('Leasingbank:',0,5),
				('Leasingbeginn:',0,6))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kdnr.grid(column=1, row=0)

		self.input_bike=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_bike.grid(column=1, row=1)

		self.input_rahmennr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_rahmennr.grid(column=1,row=2)

		self.input_nutzerid=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_nutzerid.grid(column=1, row=3)

		self.input_paket=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_paket.grid(column=1, row=4)

		self.input_bank=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_bank.grid(column=1, row=5)

		self.input_beginn=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyyy', 
			locale='de_DE', font=config.Settings.labelfont)
		self.input_beginn.delete(0, tk.END)
		self.input_beginn.grid(column=1, row=6)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)

		self.button_reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont,
			command=lambda: self.reset_inputs())
		self.button_reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.button_save=tk.Button(self.controlFrame, text='Speichern', 
			command=lambda: self.save(), font=config.Settings.headerfont)
		self.button_save.grid(column=1, row=0, padx=5, sticky=tk.EW)		

		self.INPUTS = (self.input_kdnr, self.input_bike, self.input_rahmennr, self.input_nutzerid, 
			self.input_paket, self.input_bank)
		self.DATES = (self.input_beginn,)

	def fill_inputs(self):
		to_destroy=(self.input_kdnr, self.input_bike, self.input_rahmennr, self.input_nutzerid, 
			self.input_paket, self.input_bank, self.input_beginn, self.button_reset, self.button_save)
		for widget in to_destroy:
			widget.destroy()

		#LABELS=VARIABLE, COLUMN, ROW
		LABELS=((self.kdnr,1,0),
				(self.fahrrad,1,1),
				(self.rahmennr,1,2),
				(self.nutzerid,1,3),
				(self.paket,1,4),
				(self.bank,1,5),
				(self.beginn.strftime('%d.%m.%Y'),1,6))

		for label in LABELS:
			self.temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.labelfont)
			self.temp_label.grid(column=label[1], row=label[2])

	def query_vertrag(self):
		query='SELECT paket, nutzer_id, leasingbank, beginn FROM vers_bikeleasing \
			WHERE (rahmennr="%s")' % self.rahmennr
		result=db_util.commit_query(query)

		self.paket=result[0][0]
		self.nutzerid=result[0][1]
		self.bank=result[0][2]
		self.beginn=result[0][3]

	def reset_inputs(self):
		for input_ in self.INPUTS:
			input_.delete(0, tk.END)
		for date in self.DATES:
			date.delete(0, tk.END)

	def save(self):
		all_command="INSERT INTO vers_all (kdnr, fahrrad, rahmennr, versicherung) \
			VALUES (%s, %s, %s, 'bikeleasing')"
		all_values=(self.input_kdnr.get(), self.input_bike.get(), self.input_rahmennr.get())

		anbieter_command="INSERT INTO vers_bikeleasing (rahmennr, nutzer_id, paket, \
			leasingbank, beginn) VALUES (%s, %s, %s, %s, %s)"
		anbieter_values=(self.input_rahmennr.get(), self.input_nutzerid.get(),
			self.input_paket.get(), self.input_bank.get(), 
			self.input_beginn.get_date())

		if util.check_inputs(self.INPUTS, self.DATES):
			try:
				db_util.commit_entry(all_command, all_values)
				db_util.commit_entry(anbieter_command, anbieter_values)
				self.reset_inputs()
			except:
				print("Failed to save Bikeleasing Service Info")
		else:
			err_window=messagebox.showerror(title='Eingabefeld leer', message='Alle Felder sind erforderlich!')

class Businessbike(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0, sticky=tk.EW)
		self.inputFrame.columnconfigure((0,1), weight=1)

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Leasingnutzer:',0,1),
					('Fahrrad:',0,2),
					('Rahmennummer:',0,3),
					('Leasinglaufzeit:',0,4),
					('Policenummer:',0,5),
					('Service-Paket:',0,6))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_kdnr.grid(column=1, row=0, columnspan=3, padx=2, pady=5)

		self.input_nutzer=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_nutzer.grid(column=1, row=1, columnspan=3, padx=2, pady=5)

		self.input_bike=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_bike.grid(column=1, row=2, columnspan=3, padx=2, pady=5)

		self.input_rahmennr=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_rahmennr.grid(column=1, row=3, columnspan=3, padx=2, pady=5)

		self.input_beginn=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyyy', locale='de_DE',
			font=config.Settings.labelfont, width=8)
		self.input_beginn.delete(0, tk.END)
		self.input_beginn.grid(column=1, row=4, padx=0, pady=5)
		self.label_bis=tk.Label(self.inputFrame, text='bis', font=config.Settings.labelfont)
		self.label_bis.grid(column=2, row=4, padx=2, pady=5)
		self.input_ende=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyy', locale='de_DE',
			font=config.Settings.labelfont, width=8)
		self.input_ende.delete(0, tk.END)
		self.input_ende.grid(column=3, row=4, padx=0, pady=5)

		self.input_policenr=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_policenr.grid(column=1, row=5, columnspan=3, padx=2, pady=5)

		self.input_paket=tk.Entry(self.inputFrame, font=config.Settings.labelfont, width=25)
		self.input_paket.grid(column=1, row=6, columnspan=3, padx=2, pady=5)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, columnspan=2, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)
		
		self.button_reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont,
			command=lambda: self.reset_inputs())
		self.button_reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.button_save=tk.Button(self.controlFrame, text='Speichern', 
			command=lambda: self.save(), font=config.Settings.headerfont)
		self.button_save.grid(column=1, row=0, padx=5, sticky=tk.EW)

		self.INPUTS = (self.input_kdnr, self.input_nutzer, self.input_bike, self.input_rahmennr, 
			self.input_policenr, self.input_paket)
		self.DATES = (self.input_beginn, self.input_ende)		

	def fill_inputs(self):
		to_destroy=(self.input_kdnr, self.input_nutzer, self.input_bike, self.input_rahmennr, 
			self.input_beginn, self.input_ende, self.input_policenr, self.input_paket,
			self.button_reset, self.button_save)
		for widget in to_destroy:
			widget.destroy()

		#LABELS=VARIABLE, COLUMN, ROW, COLUMNSPAN
		LABELS=((self.kdnr,1,0,3),
				(self.nutzer,1,1,3),
				(self.fahrrad,1,2,3),
				(self.rahmennr,1,3,3),
				(self.beginn.strftime('%d.%m.%Y'),1,4,1),
				(self.ende.strftime('%d.%m.%Y'),3,4,1),
				(self.policenr,1,5,3),
				(self.paket,1,6,3))

		for label in LABELS:
			self.temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.labelfont)
			self.temp_label.grid(column=label[1], row=label[2], columnspan=label[3])

	def query_vertrag(self):
		query='SELECT policenr, paket, nutzer, beginn, ende FROM vers_businessbike \
			WHERE (rahmennr="%s")' % self.rahmennr
		result=db_util.commit_query(query)

		self.policenr=result[0][0]
		self.paket=result[0][1]
		self.nutzer=result[0][2]
		self.beginn=result[0][3]
		self.ende=result[0][4]

	def reset_inputs(self):
		for input_ in self.INPUTS:
			input_.delete(0, tk.END)
		for date in self.DATES:
			date.delete(0, tk.END)

	def save(self):
		all_command="INSERT INTO vers_all (kdnr, fahrrad, rahmennr, versicherung) \
			VALUES (%s, %s, %s, 'businessbike')"
		all_values=(self.input_kdnr.get(), self.input_bike.get(), self.input_rahmennr.get())

		anbieter_command="INSERT INTO vers_businessbike (rahmennr, policenr, paket, \
			nutzer, beginn, ende) VALUES (%s, %s, %s, %s, %s, %s)"
		anbieter_values=(self.input_rahmennr.get(), self.input_policenr.get(),
			self.input_paket.get(), self.input_nutzer.get(), 
			self.input_beginn.get_date(), self.input_ende.get_date())

		if util.check_inputs(self.INPUTS, self.DATES):
			try:
				db_util.commit_entry(all_command, all_values)
				db_util.commit_entry(anbieter_command, anbieter_values)
				self.reset_inputs()
			except Error as e:
				err_window=messagebox.showerror(title='Error', message='Businessbike Versicherungsinfo könnte nicht gespeichert werden.')
		else:
			err_window=messagebox.showerror(title='Eingabefeld leer', message='Alle Felder sind erforderlich!')

class ENRA(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0, sticky=tk.EW)
		self.inputFrame.columnconfigure((0,1), weight=1)

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Nutzer:',0,1),
					('Fahrrad:',0,2),
					('Rahmennummer:',0,3),
					('Beginn:',0,4),
					('Policenummer:',0,5))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kdnr.grid(column=1, row=0, padx=2, pady=5)

		self.input_nutzer=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_nutzer.grid(column=1, row=1, padx=2, pady=5)

		self.input_bike=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_bike.grid(column=1, row=2, padx=2, pady=5)

		self.input_rahmennr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_rahmennr.grid(column=1, row=3, padx=2, pady=5)

		self.input_beginn=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyyy', 
			locale='de_DE', font=config.Settings.labelfont)
		self.input_beginn.delete(0, tk.END)
		self.input_beginn.grid(column=1, row=4, padx=2, pady=5)

		self.input_policenr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_policenr.grid(column=1, row=5, padx=2, pady=5)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)

		self.button_reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont,
			command=lambda:self.reset_inputs())
		self.button_reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.button_save=tk.Button(self.controlFrame, text='Speichern', 
			command=lambda: self.save(), font=config.Settings.headerfont)
		self.button_save.grid(column=1, row=0, padx=5, sticky=tk.EW)

		self.INPUTS = (self.input_kdnr, self.input_nutzer, self.input_bike, self.input_rahmennr,
			self.input_policenr)
		self.DATES = (self.input_beginn,)		

	def fill_inputs(self):
		to_destroy=(self.input_kdnr, self.input_nutzer, self.input_bike,
			self.input_rahmennr, self.input_beginn, self.input_policenr, 
			self.button_reset, self.button_save)

		for widget in to_destroy:
			widget.destroy()

		#LABELS=(VARIABLE, COLUMN, ROW)
		LABELS=((self.kdnr,1,0),
				(self.nutzer,1,1),
				(self.fahrrad,1,2),
				(self.rahmennr,1,3),
				(self.beginn.strftime('%d.%m.%Y'),1,4),
				(self.policenr,1,5))

		for label in LABELS:
			self.temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.labelfont)
			self.temp_label.grid(column=label[1], row=label[2])

	def query_vertrag(self):
		query='SELECT policenr, nutzer, beginn FROM vers_enra \
			WHERE (rahmennr="%s")' % self.rahmennr
		result=db_util.commit_query(query)

		self.policenr=result[0][0]
		self.nutzer=result[0][1]
		self.beginn=result[0][2]

	def reset_inputs(self):
		for input_ in self.INPUTS:
			input_.delete(0, tk.END)
		for date in self.DATES:
			date.delete(0, tk.END)

	def save(self):
		all_command="INSERT INTO vers_all (kdnr, fahrrad, rahmennr, versicherung) \
			VALUES (%s, %s, %s, 'enra')"
		all_values=(self.input_kdnr.get(), self.input_bike.get(), self.input_rahmennr.get())

		anbieter_command="INSERT INTO vers_enra (rahmennr, policenr, nutzer, beginn) \
		VALUES (%s, %s, %s, %s)"
		anbieter_values=(self.input_rahmennr.get(), self.input_policenr.get(),
			self.input_nutzer.get(), self.input_beginn.get_date())

		if util.check_inputs(self.INPUTS, self.DATES):
			try:
				db_util.commit_entry(all_command, all_values)
				db_util.commit_entry(anbieter_command, anbieter_values)
				self.reset_inputs()
			except:
				print("Failed to save ENRA Versicherungsinfo")
		else:
			err_window=messagebox.showerror(title='Eingabefeld leer', message='Alle Felder sind erforderlich!')

class EuroRad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0, sticky=tk.EW)
		self.inputFrame.columnconfigure((0,1), weight=1)

		#LABELS = ((LABEL TEXT, COLUMN, ROW))
		LABELS = (('Kundennummer:',0,0),
					('Fahrrad:',0,1),
					('Rahmennummer:',0,2),
					('Vertragsnummer:',0,3),
					('Leasingbeginn:',0,4))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], padx=2, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kdnr.grid(column=1, row=0)

		self.input_fahrrad=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_fahrrad.grid(column=1, row=1)

		self.input_rahmennr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_rahmennr.grid(column=1, row=2)

		self.input_vertragsnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_vertragsnr.grid(column=1, row=3)

		self.input_beginn=util.DateEntry(self.inputFrame, date_pattern='dd.mm.yyyy', 
			locale='de_DE', font=config.Settings.labelfont)
		self.input_beginn.delete(0, tk.END)
		self.input_beginn.grid(column=1, row=4)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)

		self.button_reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont,
			command=lambda: self.reset_inputs())
		self.button_reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.button_save=tk.Button(self.controlFrame, text='Speichern', 
			command=lambda: self.save(), font=config.Settings.headerfont)
		self.button_save.grid(column=1, row=0, padx=5, sticky=tk.EW)

		self.INPUTS = (self.input_kdnr, self.input_fahrrad, self.input_rahmennr, self.input_vertragsnr)
		self.DATES = (self.input_beginn,)		

	def fill_inputs(self):
		to_destroy=(self.input_kdnr, self.input_fahrrad, self.input_rahmennr, 
			self.input_vertragsnr, self.input_beginn, self.button_reset,
			self.button_save)
		for widget in to_destroy:
			widget.destroy()

		#LABELS=(VARIABLE, COLUMN, ROW)
		LABELS=((self.kdnr,1,0),
				(self.fahrrad,1,1),
				(self.rahmennr,1,2),
				(self.vertragsnr,1,3),
				(self.beginn.strftime('%d.%m.%Y'),1,4))

		for label in LABELS:
			self.temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.labelfont)
			self.temp_label.grid(column=label[1], row=label[2])

	def query_vertrag(self):
		query='SELECT vertragsnr, beginn FROM vers_eurorad WHERE (rahmennr="%s")' %self.rahmennr
		result=db_util.commit_query(query)

		self.vertragsnr=result[0][0]
		self.beginn=result[0][1]

	def reset_inputs(self):
		for input_ in self.INPUTS:
			input_.delete(0, tk.END)
		for date in self.DATES:
			date.delete(0, tk.END)

	def save(self):
		all_command="INSERT INTO vers_all (kdnr, fahrrad, rahmennr, versicherung) \
			VALUES (%s, %s, %s, 'eurorad')"
		all_values=(self.input_kdnr.get(), self.input_fahrrad.get(), self.input_rahmennr.get())

		anbieter_command="INSERT INTO vers_eurorad (rahmennr, vertragsnr, beginn) \
		VALUES (%s, %s, %s)"
		anbieter_values=(self.input_rahmennr.get(), self.input_vertragsnr.get(),
			self.input_beginn.get_date())

		if util.check_inputs(self.INPUTS, self.DATES):
			try:
				db_util.commit_entry(all_command, all_values)
				db_util.commit_entry(anbieter_command, anbieter_values)
				self.reset_inputs()
			except:
				print("Failed to save EuroRad Versicherungsinfo")
		else:
			err_window=messagebox.showerror(title='Eingabefeld leer', message='Alle Felder sind erforderlich!')

class JobRad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0)
		self.inputFrame.columnconfigure((0,1), weight=1)

		self.Label=tk.Label(self, text='JobRad')
		self.Label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)

		self.reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont)
		self.reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.save=tk.Button(self.controlFrame, text='Speichern', font=config.Settings.headerfont)
		self.save.grid(column=1, row=0, padx=5, sticky=tk.EW)

	def save(self):
		pass

class MeinDienstrad(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.inputFrame=tk.Frame(self)
		self.inputFrame.grid(column=0, row=0)
		self.inputFrame.columnconfigure((0,1), weight=1)

		self.Label=tk.Label(self, text='MeinDienstrad')
		self.Label.grid(column=0, row=0)

		self.controlFrame=tk.Frame(self)
		self.controlFrame.grid(column=0, row=1, sticky=tk.S+tk.EW)
		self.controlFrame.columnconfigure((0,1), weight=1)

		self.reset=tk.Button(self.controlFrame, text='Reset', font=config.Settings.headerfont)
		self.reset.grid(column=0, row=0, padx=5, sticky=tk.EW)
		
		self.save=tk.Button(self.controlFrame, text='Speichern', font=config.Settings.headerfont)
		self.save.grid(column=1, row=0, padx=5, sticky=tk.EW)

	def save(self):
		pass
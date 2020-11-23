# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:05:00 2020

@author: ryand

Goal: Create the required frames for our warranty tool
"""

from datetime import date
from datetime import datetime

import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal

import utilities.util as util
import database.db_util as db_util
import settings.config as config
import utilities.autoscroll as autoscroll

status_dict = util.configure_list('settings/list_status.csv')
mitarbeiter_dict = util.configure_list('settings/list_mitarbeiter.csv')
hersteller_dict = util.configure_list('settings/list_hersteller.csv')

class ViewWarranty(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.frame_label = tk.Label(self, text='Megabike-CRM: Reklamation', font=config.Settings.titlefont)
		self.frame_label.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)

		# Controls
		self.controlFrame=tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.controlFrame.grid(column=0, row=1, pady=1, padx=2)

		self.filter_faellig=tk.Button(self.controlFrame, text='Alle Fällige', 
			font=config.settings.headerfont, width=13, 
			command=lambda: self.filter_by('Faellig'))
		self.filter_faellig.grid(column=0, row=0, padx=5, pady=5, rowspan=3, sticky=tk.NS)

		self.filter_all=tk.Button(self.controlFrame, text='Alle', 
			font=config.settings.headerfont, width=13, 
			command=lambda: self.filter_by('All'))
		self.filter_all.grid(column=1, row=0, padx=5, pady=5, rowspan=3, sticky=tk.NS)

		self.filter_status=tk.Button(self.controlFrame, text='Nach Status', 
			font=config.settings.subheaderfont, width=15,
			command=lambda: self.filter_by('stand', self.input_status))
		self.filter_status.grid(column=2, row=0, padx=5, pady=5)
		self.input_status=ttk.Combobox(self.controlFrame, 
			font=config.settings.subheaderfont, width=15,
			value=list(status_dict.keys()))
		self.input_status.current(0)
		self.input_status.grid(column=2, row=1, padx=5, pady=5)

		self.filter_mitarbeiter=tk.Button(self.controlFrame, text='Nach Mitarbeiter', 
			font=config.settings.subheaderfont, width=15, 
			command=lambda: self.filter_by('ansprechpartner', self.input_mitarbeiter))
		self.filter_mitarbeiter.grid(column=3, row=0, padx=5, pady=5)
		self.input_mitarbeiter=ttk.Combobox(self.controlFrame, 
			font=config.settings.subheaderfont, width=15,
			value=list(mitarbeiter_dict.keys()))
		self.input_mitarbeiter.current(0)
		self.input_mitarbeiter.grid(column=3, row=1, padx=5, pady=5)

		self.filter_hersteller=tk.Button(self.controlFrame, text='Nach Hersteller', 
			font=config.settings.subheaderfont, width=15, 
			command=lambda: self.filter_by('hersteller', self.input_hersteller))
		self.filter_hersteller.grid(column=4, row=0, padx=5, pady=5)
		self.input_hersteller=ttk.Combobox(self.controlFrame, 
			font=config.settings.subheaderfont, width=15,
			value=list(hersteller_dict.keys()))
		self.input_hersteller.current(0)
		self.input_hersteller.grid(column=4, row=1, padx=5, pady=5)

		self.filter_kunde=tk.Button(self.controlFrame, text='Nach Kunde', 
			font=config.settings.subheaderfont, width=15,
			command=lambda: self.filter_by('kunde', self.input_kunde))
		self.filter_kunde.grid(column=5, row=0, padx=5, pady=5)
		self.input_kunde=tk.Entry(self.controlFrame, font=config.settings.subheaderfont, 
			width=15)
		self.input_kunde.grid(column=5, row=1, padx=5, pady=5)

		self.setting_closed = tk.IntVar(value=0)
		self.display_closed=tk.Checkbutton(self.controlFrame, text='Geschlossen anzeigen',
			font=config.settings.subheaderfont, variable=self.setting_closed)
		self.display_closed.grid(column=2, row=2, padx=5, pady=5)

		self.setting_sort = tk.StringVar(value='ASC')
		self.label_sort=tk.Label(self.controlFrame, text='Sortierung', 
			font=('Bahnschrift 10 bold underline'))
		self.sort_asc=tk.Radiobutton(self.controlFrame, text='Aufsteigend', 
			font=config.Settings.labelfont,
			variable=self.setting_sort, value='ASC')
		self.sort_desc=tk.Radiobutton(self.controlFrame, text='Absteigend',
			font=config.Settings.labelfont,
			variable=self.setting_sort, value='DESC')
		self.label_sort.grid(column=6, row=0, sticky='we')
		self.sort_asc.grid(column=6, row=1, sticky='w')
		self.sort_desc.grid(column=6, row=2, sticky='w')

		self.navFrame = tk.Frame(self, relief=tk.GROOVE, bd=2)
		self.navFrame.grid(column=1, row=1, padx=2, pady=5, sticky=tk.E)

		self.create_button=tk.Button(self.navFrame, text='Rekla Erstellen', height=5,
			font=config.Settings.subheaderfont,
			width=15, command=self.create_warranty)
		self.create_button.grid(column=0, row=0, padx=5, pady=5)

		self.viewFrame = autoscroll.ScrollableFrame(self, relief=tk.RAISED, borderwidth=3, height=450, width=1050)
		self.viewFrame.grid(column=0, row=3, padx=2, pady=5, columnspan=8, sticky='NSEW')

		self.filter_by('Faellig')

	def filter_by(self, criteria, selection=''):
		# This needs to clear view before running and printing new query
		# Split this into seperate functions at some point
			# set_query
			# run_query
			# display_query

		self.viewFrame.clear_canvas()

		self.query = ''

		self.criteria=criteria
		self.selection=selection

		if self.setting_closed.get() == 0:
			if criteria == 'All':
				self.closed_query = 'WHERE stand != "Abgeschlossen"'
			else:
				self.closed_query = 'AND stand != "Abgeschlossen"'
		else:
			self.closed_query = ''

		if criteria == 'All':
			self.query = 'SELECT * FROM rekla_vw \
				%s ORDER BY auftrag %s' %(self.closed_query, self.setting_sort.get())
		elif criteria =='Faellig':
			self.query = 'SELECT * FROM rekla_vw \
						WHERE (datum < NOW() - INTERVAL 1 WEEK %s) \
						ORDER BY auftrag %s' %(self.closed_query, self.setting_sort.get())
		else:
			self.query = 'SELECT * FROM rekla_vw \
			WHERE (%s = "%s" %s) ORDER by auftrag %s' % (criteria, selection.get(),
				self.closed_query, self.setting_sort.get())

		self.result = db_util.commit_query(self.query)

		if not self.result:
			no_result = tk.Label(self.viewFrame.frame,
        		text='Keine Ergebnisse . . . . ', font=('Helvetica',24))
			no_result.grid()

		else:
			self.label_filter = tk.Label(self.viewFrame.frame,
        		text='Aktuelle Filter: %s' %criteria, font=config.Settings.headerfont)
			self.label_filter.grid(column=0, row=0, padx=5, pady=3, columnspan=10,
				sticky='ew')

			# LABELS = ('TEXT', COLUMN, ROW)
			LABELS = (('Auftrag', 0,1),
						('Status', 1,1),
						('Annahme',2,1),
						('Ansprechpartner',3,1),
						('Kunde',4,1),
						('Kundennr',5,1),
						('Hersteller',6,1),
						('Gemeldet',7,1),
						('Vorgangsnr',8,1),
						('Update',9,1))

			for label in LABELS:
				temp_label = tk.Label(self.viewFrame.frame, text=label[0],
					font=config.Settings.subheaderfont)
				temp_label.grid(column=label[1], row=label[2], padx=8, pady=2)

			for index, result in enumerate(self.result):
				num =0
				index += 2
				rep_id = result[0]
				stand = result[1]

				update_delta = datetime.now() - result[9]

				edit_button = tk.Button(self.viewFrame.frame, text=rep_id, 
					font=config.settings.labelfont, width=10, 
					command=lambda auftrag=rep_id: EditWarranty(self, auftrag))
				edit_button.grid(row=index, column=num, pady=5)

				if stand=='Abgeschlossen':
					edit_button.configure(bg='grey25')
				else:
					if update_delta.days >= 7:
						edit_button.configure(bg='red')
					elif update_delta.days >= 4 and update_delta.days<7:
						edit_button.configure(bg='yellow')

				for subindex, value in enumerate(result):
					# TODO: Refine query such that I don't need this BS continue block.
					if subindex==0 or subindex==9:
						continue
					lookup_label = tk.Label(self.viewFrame.frame,
						text=value, font=config.Settings.labelfont)
					lookup_label.grid(row=index, column=num+1, padx=8, pady=5)
					num += 1
				view_status=tk.Button(self.viewFrame.frame, text='Status ändern', 
					font=config.settings.labelfont, width=15,
					command=lambda auftrag=rep_id: UpdateStatus(self, auftrag))
				view_status.grid(row=index, column=num+1, padx=2, pady=5)

	def create_warranty(self):
		self.app = EditWarranty(self)

	def refresh_view(self):
		self.filter_by(self.criteria, self.selection)

	def go_back(self, parent, controller):
		pass

class EditWarranty(tk.Toplevel):
	def __init__(self, parent, *auftrag):
		tk.Toplevel.__init__(self)
		self.parent=parent

		self.title('Megabike-CRM: Reklamation erstellen')

		self.controlFrame=tk.Frame(self, relief=tk.RAISED, bd=2)
		self.controlFrame.grid(row=0, column=0, sticky=tk.NSEW)

		self.controlFrame.columnconfigure((0,1), weight=1)

		# Controls go here
		self.clear=tk.Button(self.controlFrame, text='Reset', 
			font=config.Settings.headerfont, width=20,
			command=self.clear_fields)
		self.clear.grid(column=0, row=0, padx=10, pady=5, sticky=tk.EW)		

		self.submit=tk.Button(self.controlFrame, text='Speichern', 
			font=config.Settings.headerfont, width=20,
			command=self.create_rekla)
		self.submit.grid(column=1, row=0, padx=10, pady=5, sticky=tk.EW)

		self.inputFrame=tk.Frame(self, relief=tk.RAISED, bd=2)
		self.inputFrame.grid(column=0, row=1)

		#LABELS=(TEXT, COLUMN, ROW)
		LABELS=(('Mitarbeiter:',0,0),
				('Auftrag:',0,1),
				('Kunde:',0,2),
				('Kundennummer:',0,3),
				('Angenommen am:',0,4),
				('Ansprechpartner:',0,5),
				('Hersteller:',0,6),
				('Status:',0,7),
				('Gemeldet am:',0,8),
				('Vorgangsnummer:',0,9),
				('Anmerkung:',0,10))

		for label in LABELS:
			temp_label=tk.Label(self.inputFrame, text=label[0], font=config.Settings.subheaderfont)
			temp_label.grid(column=label[1], row=label[2], sticky=tk.W)
		'''
		self.bool_anmerkung=tk.IntVar()
		self.radio_anmerkung=tk.Checkbutton(self.inputFrame, text='Anmerkung', 
						variable=self.bool_anmerkung)
		self.radio_anmerkung.grid(column=0, row=10)
		'''

		self.input_mitarbeiter=ttk.Combobox(self.inputFrame, font=config.Settings.labelfont,
			value=list(mitarbeiter_dict.keys()))
		self.input_mitarbeiter.current(0)
		self.input_mitarbeiter.grid(column=1, row=0, padx=10, pady=5, sticky=tk.W)

		self.input_auftrag=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_auftrag.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)

		self.input_kunde=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kunde.grid(column=1, row=2, padx=10, pady=5, sticky=tk.W)

		self.input_kdnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont)
		self.input_kdnr.grid(column=1, row=3, padx=10, pady=5, sticky=tk.W)

		self.input_angenommen=tkcal.DateEntry(self.inputFrame, font=config.Settings.labelfont,
			date_pattern='dd.mm.yyyy', locale='de_DE')
		self.input_angenommen.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W)

		self.input_ansprechpartner=ttk.Combobox(self.inputFrame, font=config.Settings.labelfont,
			value=list(mitarbeiter_dict.keys()))
		self.input_ansprechpartner.current(0)
		self.input_ansprechpartner.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)

		self.input_hersteller=ttk.Combobox(self.inputFrame, font=config.Settings.labelfont,
			value=list(hersteller_dict.keys()))
		self.input_hersteller.current(0)
		self.input_hersteller.grid(column=1, row=6, padx=10, pady=5, sticky=tk.W)

		self.input_status=ttk.Combobox(self.inputFrame, font=config.Settings.labelfont,
			value=list(status_dict.keys()))
		self.input_status.current(0)
		self.input_status.grid(column=1, row=7, padx=10, pady=5, sticky=tk.W)

		self.input_gemeldet=tkcal.DateEntry(self.inputFrame, font=config.Settings.labelfont,
			date_pattern='dd.mm.yyyy', locale='de_DE')
		self.input_gemeldet.grid(column=1, row=8, padx=10, pady=5, sticky=tk.W)

		self.input_vorgangsnr=tk.Entry(self.inputFrame, font=config.Settings.labelfont,)
		self.input_vorgangsnr.grid(column=1, row=9, padx=10, pady=5, sticky=tk.W)

		self.input_anmerkung=tk.Text(self.inputFrame, font=config.Settings.labelfont,
			height=7, width=50)
		self.input_anmerkung.grid(column=1, row=10, padx=10, pady=5, sticky=tk.NW)

		if auftrag:
			self.auftrag = auftrag[0]
			self.fill_info(self.auftrag)

	def fill_info(self, auftrag):
		query_info= 'SELECT * FROM rekla_vw WHERE auftrag=%s ORDER BY auftrag ASC' % self.auftrag
		query_status= 'SELECT * FROM rekla_status WHERE auftrag=%s ORDER BY auftrag ASC' % self.auftrag
		result_info=db_util.commit_query(query_info)
		result_info=result_info[0]
		result_status=db_util.commit_query(query_status)

		self.title('Megabike-CRM: Reklamation %s' % self.auftrag)

		self.input_auftrag.destroy()
		self.submit.destroy()
		self.input_angenommen.selection_clear()
		self.input_gemeldet.selection_clear()

		self.submit=tk.Button(self.controlFrame, text='Speichern', 
			font=config.Settings.headerfont, width=20,
			command=self.edit_rekla)
		self.submit.grid(column=1, row=0, padx=10, pady=5, sticky=tk.EW)		

		self.setting_close=tk.IntVar()
		self.check_close=tk.Checkbutton(self.controlFrame, text='Close after save',
			font=config.Settings.subheaderfont, variable=self.setting_close)
		self.check_close.grid(row=1, column=1, padx=2, pady=1, sticky=tk.EW)

		self.current_auftrag=tk.Label(self.inputFrame, text=self.auftrag, font=config.Settings.subheaderfont)
		self.current_auftrag.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)

		current_ansprechpartner=int(mitarbeiter_dict.get(result_info[3]))
		self.input_ansprechpartner.current(current_ansprechpartner)

		current_hersteller=int(hersteller_dict.get(result_info[6]))
		self.input_hersteller.current(current_hersteller)

		current_status=int(status_dict.get(result_info[1]))
		self.input_status.current(current_status)

		self.input_kunde.insert(0, result_info[4])
		self.input_kdnr.insert(0, result_info[5])
		self.input_angenommen.set_date(result_info[2])
		self.input_gemeldet.set_date(result_info[7])
		self.input_vorgangsnr.insert(0, result_info[8])

		# Figure out a way to auto resize the canvas?
		self.commentsFrame=autoscroll.ScrollableFrame(self, relief=tk.RAISED, borderwidth=10, height=200, width=750)
		self.commentsFrame.grid(column=0, row=2, pady=10)

		self.label_date=tk.Label(self.commentsFrame.frame, 
			text='Datum', font=config.Settings.labelfont)
		self.label_date.grid(column=0, row=0, padx=5, pady=3)

		self.label_mitarbeiter=tk.Label(self.commentsFrame.frame, 
			text='Mitarbeiter', font=config.Settings.labelfont)
		self.label_mitarbeiter.grid(column=1, row=0, padx=5, pady=3)

		self.label_status=tk.Label(self.commentsFrame.frame,
			text='Status', font=config.Settings.labelfont)
		self.label_status.grid(column=2, row=0, padx=5, pady=3)

		self.label_comment=tk.Label(self.commentsFrame.frame,
			text='Anmerkung', font=config.Settings.labelfont)
		self.label_comment.grid(column=3, row=0, padx=5, pady=3)

		# The view order needs to be reversed, should display newest up top
		num=len(result_status)
		for i, x in enumerate(result_status):
			date=tk.Label(self.commentsFrame.frame, text=x[5], 
				font=config.Settings.labelfont)
			date.grid(column=0, row=num, padx=5, pady=3)
			mitarbeiter=tk.Label(self.commentsFrame.frame, text=x[1],
				font=config.Settings.labelfont)
			mitarbeiter.grid(column=1, row=num, padx=5, pady=3)
			status=tk.Label(self.commentsFrame.frame, text=x[3],
				font=config.Settings.labelfont)
			status.grid(column=2, row=num, padx=5, pady=3)
			anmerkung=tk.Text(self.commentsFrame.frame, wrap=tk.WORD, 
				font=config.Settings.labelfont, width=50, height=5)
			anmerkung.insert(tk.END, x[4])
			anmerkung.grid(column=3, row=num, padx=5, pady=3)
			num-=1

	def clear_fields(self):
		self.input_mitarbeiter.current(0)
		self.input_kunde.delete(0, tk.END)
		self.input_kdnr.delete(0, tk.END)
		self.input_angenommen.delete(0, tk.END)
		self.input_ansprechpartner.current(0)
		self.input_hersteller.current(0)
		self.input_status.current(0)
		self.input_gemeldet.delete(0, tk.END)
		self.input_vorgangsnr.delete(0, tk.END)
		self.input_anmerkung.delete(1.0, tk.END)
		
		if self.auftrag:
			self.fill_info(self.auftrag)
		else:
			self.input_auftrag.delete(0, tk.END)

	def create_rekla(self):
		info_command="INSERT INTO rekla (auftrag, angenommen, ansprechpartner, \
			kunde, kd_nr, hersteller, gemeldet, vorgangsnr) \
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		info_values=(self.input_auftrag.get(), self.input_angenommen.get_date(),
					self.input_ansprechpartner.get(), self.input_kunde.get(),
					self.input_kdnr.get(), self.input_hersteller.get(), 
					self.input_gemeldet.get_date(), self.input_vorgangsnr.get())

		status_command="INSERT INTO rekla_status (mitarbeiter, auftrag, stand,\
			anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
		status_values=(self.input_mitarbeiter.get(), self.input_auftrag.get(), 
			self.input_status.get(), self.input_anmerkung.get(1.0, tk.END))

		if db_util.check_existence('rekla', 'auftrag', self.input_auftrag.get()) == 0:
			db_util.commit_entry(info_command, info_values)
			db_util.commit_entry(status_command, status_values)
			self.destroy()
			self.parent.refresh_view()
		else:
			print("Something went wrong, man")

	def edit_rekla(self):
		info_command="UPDATE rekla SET angenommen=%s, ansprechpartner=%s, \
			kunde=%s, kd_nr=%s, hersteller=%s, gemeldet=%s, vorgangsnr=%s \
			WHERE auftrag=%s" 
		info_values=(self.input_angenommen.get(),
			self.input_ansprechpartner.get(), self.input_kunde.get(),
			self.input_kdnr.get(), self.input_hersteller.get(), 
			self.input_gemeldet.get(), self.input_vorgangsnr.get(), self.auftrag)

		status_command="INSERT INTO rekla_status (mitarbeiter, auftrag, stand,\
			anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
		status_values=(self.input_mitarbeiter.get(), self.auftrag,
			self.input_status.get(), self.input_anmerkung.get(1.0, tk.END))

		db_util.commit_entry(info_command, info_values)
		db_util.commit_entry(status_command, status_values)

		self.parent.refresh_view()

		if self.setting_close.get()==1:
			self.destroy()
		else:
			self.refresh_frame()

	def refresh_frame(self):
		self.destroy()
		self.__init__(self.parent, self.auftrag)

class UpdateStatus(tk.Toplevel):
	def __init__(self, parent, auftrag):
		tk.Toplevel.__init__(self)
		self.parent=parent
		self.auftrag = auftrag

		self.status_list=self.fill_info()

		end_status = len(self.status_list)-1
		self.current_status = self.status_list[end_status][3]

		self.title('Megabike CRM: Rekla %s Status' % self.auftrag)

		self.controlFrame=tk.Frame(self, relief=tk.RAISED, bd=2)
		self.controlFrame.grid(row=0, column=1, sticky=tk.N, padx=2, pady=5)

		self.inputFrame=tk.Frame(self, relief=tk.RAISED, bd=2)
		self.inputFrame.grid(row=0, column=0, sticky=tk.N, padx=2, pady=5)

		self.setting_close=tk.IntVar()

		self.check_close=tk.Checkbutton(self.controlFrame, text='Close after save',
			variable=self.setting_close)
		self.check_close.grid(row=0, column=0, padx=2, pady=1, sticky=tk.NW)

		self.save_new=tk.Button(self.controlFrame, text='Speichern', width=20, height=2,
			command=self.commit_update)
		self.save_new.grid(row=1, column=0, padx=2, pady=3, sticky=tk.NW)

		self.update_mitarbeiter=ttk.Combobox(self.controlFrame, width=20,
			values=list(mitarbeiter_dict.keys()))
		self.update_mitarbeiter.current(0)
		self.update_mitarbeiter.grid(row=2, column=0, padx=2, pady=3, sticky=tk.NW)

		self.label_auftrag = tk.Label(self.inputFrame, text=self.auftrag)
		self.label_auftrag.grid(row=0, column=0, padx=2, pady=3, sticky=tk.NW)

		self.old_status = tk.Label(self.inputFrame, text=self.current_status)
		self.old_status.grid(row=1, column=0, padx=2, pady=3,  sticky=tk.NW)

		self.new_status=ttk.Combobox(self.inputFrame, values=list(status_dict.keys()))
		self.new_status.current(int(status_dict.get(self.current_status)))
		self.new_status.grid(row=2, column=0, padx=2, pady=3, sticky=tk.NW)

		self.new_comment=tk.Text(self.inputFrame, height=5, width=60)
		self.new_comment.grid(row=0, column=1, rowspan=3, columnspan=8, padx=2, pady=5)

		self.commentsFrame=autoscroll.ScrollableFrame(self, relief=tk.RAISED, height=200, width=750)
		self.commentsFrame.grid(column=0, row=2, columnspan=4)
		
		num=len(self.status_list)
		for i, x in enumerate(self.status_list):
			i+=2
			date=tk.Label(self.commentsFrame.frame, text=x[5])
			date.grid(column=0, row=num, padx=5, pady=3)

			mitarbeiter=tk.Label(self.commentsFrame.frame, text=x[1])
			mitarbeiter.grid(column=1, row=num, padx=5, pady=3)

			status=tk.Label(self.commentsFrame.frame, text=x[3])
			status.grid(column=2, row=num, padx=5, pady=3)

			anmerkung=tk.Text(self.commentsFrame.frame, wrap=tk.WORD,
				width=53, height=5)
			anmerkung.insert(tk.END, x[4])
			anmerkung.grid(column=3, row=num, padx=5, pady=3)
			num-=1

	def fill_info(self):
		query_status= 'SELECT * FROM rekla_status WHERE auftrag=%s ORDER BY auftrag DESC' % self.auftrag
		result_status=db_util.commit_query(query_status)

		return(result_status)

	def commit_update(self):
		status_command="INSERT INTO rekla_status (mitarbeiter, auftrag, stand,\
			anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
		status_values=(self.update_mitarbeiter.get(), self.auftrag,
			self.new_status.get(), self.new_comment.get(1.0, tk.END))

		db_util.commit_entry(status_command, status_values)

		print(self.setting_close)
		print(self.setting_close.get())
		self.parent.refresh_view()
		if self.setting_close.get()==1:
			self.destroy()
		else:
			self.refresh_frame()

	def refresh_frame(self):
		self.destroy()
		self.__init__(self.parent, self.auftrag)
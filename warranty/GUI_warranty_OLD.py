# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 20:56:25 2020

@author: ryand

Goal: Create a ticket writer for warranty claims for our Megabike CRM
"""

from datetime import datetime

import tkinter as tk
from tkinter import ttk

import config
import db_connection_pool as db_connect
import db_util
import util


def main():
    
    label_font = 'Helvetica 8 bold'
    
    def filter_by(criteria, closed_setting, setting_sort, selection=''):
        subView = create_view()
        query = ''
        
        setting_sort = setting_sort.get()
        
        if closed_setting.get() == 0:
            if criteria =='All':
                closed_query = 'WHERE stand != "Abgeschlossen"'
            else:
                closed_query = 'AND stand != "Abgeschlossen"'
        else:
            closed_query = ''
        
        if criteria == 'All':
            query = 'SELECT * FROM rekla_vw \
                %s ORDER BY auftrag %s' % (closed_query, setting_sort)
        elif criteria == 'Faellig':
            query = 'SELECT * FROM rekla_vw \
                        WHERE (datum < NOW() - INTERVAL 1 WEEK %s) \
                        ORDER BY auftrag %s' % (closed_query, setting_sort)
        else:
            query = 'SELECT * FROM rekla_vw \
                        WHERE (%s = "%s" %s) ORDER by auftrag %s' % (criteria, selection.get(),
                        closed_query, setting_sort)
            
        result = db_util.commit_query(query)
        
        if not result:
            no_result = tk.Label(subView, text = 'Keine Ergebnisse. . . .', 
                                 font=('Helvetica', 24))
            no_result.pack()
        else:
            label_filter = tk.Label(subView, text='Aktuelle Filter: %s' % criteria,
                                    font='Helvetica 12 bold')
            label_filter.grid(column=0, row=0, padx=5, pady=3, columnspan=10, sticky='ew')
            
            label_filter = tk.Label(subView, text='Auftrag', font=label_font)
            label_filter.grid(column=0, row=1, padx=5, pady=3)
            
            label_status = tk.Label(subView, text='Status', font=label_font)
            label_status.grid(column=1, row=1, padx=5, pady=3)
            
            label_angenommen = tk.Label(subView, text='Angenommen', font=label_font)
            label_angenommen.grid(column=2, row=1, padx=5, pady=3)
            
            label_ansprechpartner = tk.Label(subView, text='Ansprechpartner', font=label_font)
            label_ansprechpartner.grid(column=3, row=1, padx=5, pady=3)
            
            label_kunde = tk.Label(subView, text='Kunde', font=label_font)
            label_kunde.grid(column=4, row=1, padx=5, pady=3)
            
            label_kdnr = tk.Label(subView, text='Kd Nr', font=label_font)
            label_kdnr.grid(column=5, row=1, padx=5, pady=3)
            
            label_hersteller = tk.Label(subView, text='Hersteller', font=label_font)
            label_hersteller.grid(column=6, row=1, padx=5, pady=3)
            
            label_gemeldet = tk.Label(subView, text='Gemeldet', font=label_font)
            label_gemeldet.grid(column=7, row=1, padx=5, pady=3)
            
            label_vorgangsnr = tk.Label(subView, text='Vorgangsnr', font=label_font)
            label_vorgangsnr.grid(column=8, row=1, padx=5, pady=3)
            
            label_update = tk.Label(subView, text='Update Status', font=label_font)
            label_update.grid(column=9, row=1, padx=5, pady=3)
            
            for i, x in enumerate(result):
                num = 0
                i += 2
                rep_id = x[0]
                stand = x[1]
                
                update_delta = datetime.now() - x[9]
                
                edit_button = tk.Button(subView, text=rep_id, width=10, 
                                        command=lambda auftrag=x[0]: update_rekla(edit_mode=True, rep_id=auftrag))
                edit_button.grid(row=i, column=num, pady=5)
                
                if stand == 'Abgeschlossen':
                    edit_button.configure(bg='grey25')
                else:
                    if update_delta.days >= 7:
                        edit_button.configure(bg='red')
                    elif update_delta.days >=4 and update_delta.days<7:
                        edit_button.configure(bg='yellow')
                
                for idx, val in enumerate(x):
                    if idx==0 or idx==9: #Don't need to print idx == 9 after testing?
                        continue
                    lookup_label = tk.Label(subView, text=val)
                    lookup_label.grid(row=i, column=num+1, padx=5, pady=5)
                    num += 1
                view_status = tk.Button(subView, text='Stand ändern', width=20,
                                          command=lambda rep_id=x[0]: update_status(rep_id))
                view_status.grid(row=i, column=num+1, padx=2, pady=5)
                
            subView.bind("<Configure>", lambda event, canvas=viewCanvas: configure_frame(canvas))
        
    def create_view():
        for child in viewCanvas.winfo_children():
            child.destroy()
        
        subView = tk.Frame(viewCanvas)
        subView.pack(fill=tk.BOTH, expand=1)
        
        viewCanvas.configure(yscrollcommand=viewScroll.set)
        viewCanvas.create_window((0,0), window=subView, anchorB='nw')
        
        return subView
    
    root = tk.Tk()
    root.title("Megabike CRM: Reklamation")
    
    root.wm_iconbitmap('settings/icon.ico')
    
    controlFrame = tk.Frame(root, relief=tk.GROOVE, bd=2)
    controlFrame.grid(column=0, row=1, pady=2, padx=1)
    
    # Create our frame for search results along with required canvas and scrollbar
    viewFrame=tk.Frame(root, relief=tk.RAISED, bd=2, padx=1, pady=2)
    viewFrame.grid(column=0, row=3, pady=10, columnspan=8, sticky='nw')
    viewFrame.grid_rowconfigure(0, weight=1)
    viewFrame.grid_columnconfigure(0, weight=1)
    viewCanvas = tk.Canvas(viewFrame, height=450, width=980)
    viewCanvas.grid(row=0, column=0, sticky='news')
    viewScroll = tk.Scrollbar(viewFrame, orient='vertical', 
                              command=viewCanvas.yview)
    viewScroll.grid(row=0, column=1, sticky='ns')
    viewCanvas.configure(yscrollcommand=viewScroll.set)

    # Inputs
    
    filter_faellig = tk.Button(controlFrame, text='Alle Fällige Reklas', height=3, width=15,
                        command=lambda: filter_by('Faellig', closed_setting, setting_sort))
    filter_faellig.grid(column=0, row=0, padx=5, pady=5, rowspan=2)
    
    filter_offen = tk.Button(controlFrame, text='Alle Reklas', height=3, width=15,
                      command=lambda: filter_by('All', closed_setting, setting_sort))
    filter_offen.grid(column=1, row=0, padx=5, pady=5, rowspan=2)
     
    '''
    label_threshold1 = tk.Label(controlFrame, text='Fällig gelb')
    label_threshold1.grid(column=0, row=2)
    input_threshold1 = tk.Entry(controlFrame, width=5)
    input_threshold1.grid(column=0, row=3)
    
    label_threshold2 = tk.Label(controlFrame, text='Fällig rot')
    label_threshold2.grid(column=1, row=2)
    input_threshold2 = tk.Entry(controlFrame, width=5)
    input_threshold2.grid(column=1, row=3)
    '''
    
    filter_status = tk.Button(controlFrame, text='Nach Status', width=15,
                            command=lambda: filter_by('stand', closed_setting, 
                                                      setting_sort, input_status))
    filter_status.grid(column=2, row=0, padx=5, pady=5)
    
    input_status = ttk.Combobox(controlFrame, width=15,
                              value=list(status_dict.keys()))
    input_status.current(0)
    input_status.grid(column=2, row=1, padx=5, pady=5)
    
    filter_mitarbeiter = tk.Button(controlFrame, text='Nach Mitarbeiter', width=15,
                                 command=lambda: filter_by('ansprechpartner', closed_setting, 
                                                           setting_sort, input_mitarbeiter))
    filter_mitarbeiter.grid(column=3, row=0, padx=5, pady=5)
    
    input_mitarbeiter = ttk.Combobox(controlFrame, width=15, 
                               value=list(mitarbeiter_dict.keys()))
    input_mitarbeiter.current(0)
    input_mitarbeiter.grid(column=3, row=1, padx=5, pady=5)
    
    filter_hersteller = tk.Button(controlFrame, text='Nach Hersteller', width=15,
                                command=lambda: filter_by('hersteller', closed_setting, 
                                                          setting_sort, input_hersteller))
    filter_hersteller.grid(column=4, row=0, padx=5, pady=5)
    
    input_hersteller = ttk.Combobox(controlFrame, width=15,
                              value=list(hersteller_dict.keys()))
    input_hersteller.current(0)
    input_hersteller.grid(column=4, row=1, padx=5, pady=5)
    
    filter_kunde = tk.Button(controlFrame, text='Nach Kunde', width=15,
                               command=lambda: filter_by('kunde', closed_setting, 
                                                         setting_sort, input_kunde))
    filter_kunde.grid(column=5, row=0, padx=5, pady=5)
    
    input_kunde = tk.Entry(controlFrame, width=15)
    input_kunde.grid(column=5, row=1, padx=5, pady=5)
    
    closed_setting = tk.IntVar()    
    display_closed = tk.Checkbutton(controlFrame, text='Geschlossen anzeigen', variable=closed_setting)
    display_closed.grid(column=2, row=2, padx=5, pady=5)
    
    label_sort=tk.Label(controlFrame, text='Sortierung', font='Helvetica 10 bold underline')
    setting_sort = tk.StringVar()
    setting_sort.set('ASC')
    sort_asc = tk.Radiobutton(controlFrame, text='Aufsteigend', variable=setting_sort,
                              value='ASC')
    sort_desc = tk.Radiobutton(controlFrame, text='Absteigend', variable=setting_sort,
                               value='DESC')
    label_sort.grid(column=6, row=0, sticky='we')
    sort_asc.grid(column=6, row=1, sticky='w')
    sort_desc.grid(column=6, row=2, sticky='w')
    
    button_settings = tk.Button(controlFrame, text='Einstellungen',
                                command = lambda: config.mysql_credentials())
    button_settings.grid(column=5, row=2)
    
    
    # Navigation
    
    navFrame = tk.Frame(master=root, relief=tk.GROOVE, bd=2)
    navFrame.grid(column=1, row=1, padx=5, pady=5, sticky=tk.E)
    
    create_button = tk.Button(navFrame, text='Rekla Erstellen', height=5,
                                    width=15, command=lambda: update_rekla())
    create_button.grid(column=0, row=0, padx=5, pady=5)
    

    
    filter_by('Faellig', closed_setting, setting_sort)
    root.mainloop()
    


def update_rekla(edit_mode=False, rep_id=''):
    
    def clear_fields():
        input_mitarbeiter.delete(0, tk.END)
        input_auftrag.delete(0, tk.END)
        input_kunde.delete(0, tk.END)
        input_kdnr.delete(0, tk.END)
        input_angenommen.delete(0, tk.END)
        input_ansprechpartner.current(0)
        input_hersteller.current(0)
        input_status.current(0)
        input_gemeldet.delete(0, tk.END)
        input_vorgangsnr.delete(0, tk.END)
        input_anmerkung.delete(1.0, tk.END)
        
    def reset_fields():
        if edit_mode == False:
            clear_fields()
        else:
            pass
    
    erstellen = tk.Tk()
    
    controlFrame = tk.Frame(master=erstellen, relief=tk.RAISED, bd=2)
    controlFrame.grid(row=0, column=0)
    
    inputFrame = tk.Frame(erstellen, relief=tk.RAISED, bd=2)
    inputFrame.grid(column=0, row=1)
    
    # Inputs
    label_mitarbeiter = tk.Label(inputFrame, text='Mitarbeiter:')
    label_mitarbeiter.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
    label_filter = tk.Label(inputFrame, text='Auftrag:')
    label_filter.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
    label_kunde = tk.Label(inputFrame, text='Kunde:')
    label_kunde.grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)
    label_kdnr = tk.Label(inputFrame, text='Kundennummer:')
    label_kdnr.grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)
    label_angenommen = tk.Label(inputFrame, text='Angenommen am:')
    label_angenommen.grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
    label_ansprechpartner = tk.Label(inputFrame, text='Ansprechpartner:')
    label_ansprechpartner.grid(column=0, row=5, sticky=tk.W, padx=10, pady=5)
    label_hersteller = tk.Label(inputFrame, text='Hersteller:')
    label_hersteller.grid(column=0, row=6, sticky=tk.W, padx=10, pady=5)
    label_status = tk.Label(inputFrame, text='Status:')
    label_status.grid(column=0, row=7, sticky=tk.W, padx=10, pady=5)
    label_gemeldet = tk.Label(inputFrame, text='Gemeldet am:')
    label_gemeldet.grid(column=0, row=8, sticky=tk.W, padx=10, pady=5)
    label_vorgangsnr = tk.Label(inputFrame, text='Vorgangsnummer:')
    label_vorgangsnr.grid(column=0, row=9, sticky=tk.W, padx=10, pady=5)
    label_anmerkung = tk.Label(inputFrame, text='Anmerkung:')
    label_anmerkung.grid(column=0, row=10, sticky=tk.W, padx=10, pady=5)
    
    input_mitarbeiter = ttk.Combobox(inputFrame, value=list(mitarbeiter_dict.keys()))
    input_mitarbeiter.current(0)
    input_mitarbeiter.grid(column=1, row=0, padx=10, pady=5, sticky=tk.W)

    input_kunde = tk.Entry(inputFrame)
    input_kunde.grid(column=1, row=2, padx=10, pady=5, sticky=tk.W)
    
    input_kdnr = tk.Entry(inputFrame)
    input_kdnr.grid(column=1, row=3, padx=10, pady=5, sticky=tk.W)

    input_angenommen = tk.Entry(inputFrame)
    input_angenommen.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W)
    
    input_ansprechpartner = ttk.Combobox(inputFrame, value=list(mitarbeiter_dict.keys()))
    input_ansprechpartner.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)
    
    input_hersteller = ttk.Combobox(inputFrame, value=list(hersteller_dict.keys()))
    input_hersteller.grid(column=1, row=6, padx=10, pady=5, sticky=tk.W)
    
    input_status = ttk.Combobox(inputFrame, value=list(status_dict.keys()))
    input_status.grid(column=1, row=7, padx=10, pady=5, sticky=tk.W)
    
    input_gemeldet = tk.Entry(inputFrame)
    input_gemeldet.grid(column=1, row=8, padx=10, pady=5, sticky=tk.W)
    
    input_vorgangsnr = tk.Entry(inputFrame)
    input_vorgangsnr.grid(column=1, row=9, padx=10, pady=5, sticky=tk.W)

    input_anmerkung = tk.Text(inputFrame, height=7, width=50)
    input_anmerkung.grid(column=1, row=10, padx=10, pady=5, sticky=tk.NW)
    
    if edit_mode == False:
        erstellen.title('Megabike CRM: Rekla erstellen')
        
        input_auftrag = tk.Entry(inputFrame)
        input_auftrag.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)
        
        input_ansprechpartner.current(0)
        input_hersteller.current(0)
        input_status.current(0)
        
        def read_inputs():
            rekla_command = "INSERT INTO rekla (auftrag, angenommen, ansprechpartner, \
                            kunde, kd_nr, hersteller, gemeldet, vorgangsnr) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            
            rekla_values = (input_auftrag.get(), input_angenommen.get(), 
                      input_ansprechpartner.get(), input_kunde.get(),
                      input_kdnr.get(), input_hersteller.get(), input_gemeldet.get(), 
                      input_vorgangsnr.get())
            
            status_command = "INSERT INTO rekla_status (mitarbeiter, auftrag, stand,\
                            anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
            status_values = (input_mitarbeiter.get(), input_auftrag.get(), input_status.get(), 
                      input_anmerkung.get(1.0, tk.END))
            
            if db_util.check_existence('rekla', 'auftrag', input_auftrag.get()) == 0:
                db_util.commit_entry(rekla_command, rekla_values) 
                db_util.commit_entry(status_command, status_values)
                erstellen.destroy()
                
            else:
                error('A001')
            
    else:
        erstellen.title('Megabike CRM: Rekla bearbeiten')
        
        # Inputs 
        result = read_values(rep_id)
        status = result[1]
        result = result[0]
        
        # I don't like that these are essentially hard coded to our current table layout
        current_ansprechpartner = int(mitarbeiter_dict.get(result[0][3]))
        current_hersteller = int(hersteller_dict.get(result[0][6]))
        current_status= int(status_dict.get(result[0][1]))
        
        label_auftrag = tk.Label(inputFrame, text=result[0][0])
        label_auftrag.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)
        
        input_ansprechpartner.current(current_ansprechpartner)
        input_hersteller.current(current_hersteller-1)
        input_status.current(current_status)
        
        input_kunde.insert(0, result[0][4])
        input_kdnr.insert(0, result[0][5])
        input_angenommen.insert(0, result[0][2])
        input_gemeldet.insert(0, result[0][7])
        input_vorgangsnr.insert(0, result[0][8])
        
        # Create frame, canvas, and scrollbar for status/comment data
        commentsFrame = tk.Frame(inputFrame, relief=tk.RAISED, bd=2, padx=5, pady=5)  
        commentsFrame.grid(row=11, column=0, columnspan=4)
        commentsFrame.grid_rowconfigure(0, weight=1)
        commentsFrame.grid_columnconfigure(0, weight=1)
        commentsCanvas = tk.Canvas(commentsFrame, height=275, width=760)
        commentsCanvas.grid(row=0, column=0, sticky='news')
        commentsView = tk.Frame(commentsCanvas)
        commentsView.grid(row=0, column=0)
        commentsScroll = tk.Scrollbar(commentsFrame, orient='vertical',
                                      command=commentsCanvas.yview)
        commentsScroll.grid(row=0, column=1, sticky='ns')
        commentsCanvas.configure(yscrollcommand=commentsScroll.set)
        commentsCanvas.create_window((0,0), window=commentsView, anchor='nw')
        commentsView.bind("<Configure>", lambda event, canvas=commentsCanvas:configure_frame(canvas))
    
        # Populate our scrollable frame with comments
        num=1
        for i, x in enumerate(status):
            i += 2
            date = tk.Label(commentsView, text=x[5])
            date.grid(column=0, row=num, padx=5, pady=3)
            
            mitarbeiter = tk.Label(commentsView, text=x[1])
            mitarbeiter.grid(column=1, row=num, padx=5, pady=3)
            
            status = tk.Label(commentsView, text=x[3])
            status.grid(column=2, row=num, padx=5, pady=3)
            
            anmerkung = tk.Text(commentsView, wrap=tk.WORD, width=55, height=5)
            anmerkung.insert(tk.END, x[4])
            anmerkung.grid(column=3, row=num, padx=5, pady=3)
            
            num += 1
        
        def read_inputs():    
            rekla_command = "UPDATE rekla SET angenommen = %s,\
                ansprechpartner = %s, kunde = %s, kd_nr = %s, hersteller = %s,\
                gemeldet = %s, vorgangsnr = %s WHERE auftrag = %s"
            
            rekla_values = (input_angenommen.get(), input_mitarbeiter.get(), 
                      input_kunde.get(), input_kdnr.get(), input_hersteller.get(), 
                      input_gemeldet.get(), input_vorgangsnr.get(), label_auftrag.cget('text'))
            
            status_command = "INSERT INTO rekla_status (mitarbeiter, auftrag, \
                 stand, anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
    
            status_values = (input_mitarbeiter.get(), label_auftrag.cget('text'),
                                input_status.get(), input_anmerkung.get(1.0, tk.END))
            
            # I don't like that our null mitarbeiter is essentially hardcoded here
            if input_mitarbeiter.get() != 'Mitarbeiter . . . . ':
                db_util.commit_entry(rekla_command, rekla_values)
                db_util.commit_entry(status_command, status_values)
            else:
                error('M001')
        
    submit_button = tk.Button(controlFrame, text='Speichern', command=read_inputs)
    submit_button.grid(column=0, row=0, padx=10, pady=5)
    
    # We probably don't want to clear all of our fields when editing a rekla ticket
    clear_fields_button = tk.Button(controlFrame, text='Reset', command=clear_fields)
    clear_fields_button.grid(column=1, row=0, padx=10, pady=5)

    erstellen.mainloop()

def update_status(rep_id):
    
    def read_inputs():
        status_command = "INSERT INTO rekla_status (mitarbeiter, auftrag, \
            stand, anmerkung, datum) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"

        status_values = (update_mitarbeiter.get(), rep_id,
                            new_status.get(), new_comment.get(1.0, tk.END))
      
        db_util.commit_entry(status_command, status_values)
    
    values = read_values(rep_id)
    status = values[1]
    values = values[0]
    
    current_status= int(status_dict.get(values[0][1]))
    
    commentWindow = tk.Tk()
    
    commentWindow.title('Megabike CRM: Rekla %s Status' % rep_id)
    #commentWindow.geometry('800x400')
    
    controlFrame = tk.Frame(commentWindow, relief=tk.RAISED, bd=2)
    controlFrame.grid(row=0, column=1, sticky=tk.N, padx=2, pady=5)
    
    inputFrame = tk.Frame(commentWindow, relief=tk.RAISED, bd=2)
    inputFrame.grid(row=0, column=0, sticky=tk.N, padx=2, pady=5)
    
    save_new = tk.Button(controlFrame, text='Speichern', width=20, height=3,
                         command=update_status)
    save_new.grid(row=0, column=0, padx=2, pady=5, sticky=tk.NW)
    
    update_mitarbeiter = ttk.Combobox(controlFrame, width=20,
                              values=list(mitarbeiter_dict.keys()))
    update_mitarbeiter.current(0)
    update_mitarbeiter.grid(row=1, column=0, padx=2, pady=3, sticky=tk.NW)
    
    new_comment = tk.Text(inputFrame, height=5, width=60)
    new_comment.grid(row=0, column=2, rowspan=2, columnspan=8, padx=2, pady=5)
    
    old_status = tk.Label(inputFrame, text=status[0][3], font='Helvetica 10 bold')
    old_status.grid(row=0, column=1, padx=2, pady=5, sticky=tk.NW)
    
    new_status = ttk.Combobox(inputFrame, values=list(status_dict.keys()))
    new_status.current(current_status)
    new_status.grid(row=1, column=1, padx=2, pady=5, sticky=tk.NW)
    
    
    # Create frame, canvas, and scrollbar for our status/comment data
    commentsFrame = tk.Frame(commentWindow, relief=tk.RAISED, bd=2, padx=5, pady=5)
    commentsFrame.grid(row=2, column=0, columnspan=4)
    commentsFrame.grid_rowconfigure(0, weight=1)
    commentsFrame.grid_columnconfigure(0, weight=1)
    commentsCanvas = tk.Canvas(commentsFrame, height=275, width=800)
    commentsCanvas.grid(row=0, column=0, sticky='news')
    commentsView = tk.Frame(commentsCanvas)
    commentsView.grid(row=0, column=0)
    commentsScroll = tk.Scrollbar(commentsFrame, orient='vertical',
                                  command=commentsCanvas.yview)
    commentsScroll.grid(row=0, column=1, sticky='ns')
    commentsCanvas.configure(yscrollcommand=commentsScroll.set)
    commentsCanvas.create_window((0,0), window=commentsView, anchor='nw')
    commentsView.bind("<Configure>", lambda event, canvas=commentsCanvas: configure_frame(canvas))
    
    label_date = tk.Label(commentsView, text='Datum', font='Helvetica 10 bold')
    label_date.grid(column=0, row=0, padx=5, pady=3)
    
    label_mitarbeiter = tk.Label(commentsView, text='Mitarbeiter', font='Helvetica 10 bold')
    label_mitarbeiter.grid(column=1, row=0, padx=5, pady=3)
    
    label_status = tk.Label(commentsView, text='Status', font='Helvetica 10 bold')
    label_status.grid(column=2, row=0, padx=5, pady=3)
    
    label_comment = tk.Label(commentsView, text='Anmerkung', font='Helvetica 10 bold')
    label_comment.grid(column=3, row=0, padx=5, pady=3)
  
    num=1
    for i, x in enumerate(status):
        i += 2
        date = tk.Label(commentsView, text=x[5])
        date.grid(column=0, row=num, padx=5, pady=3)
        
        mitarbeiter = tk.Label(commentsView, text=x[1])
        mitarbeiter.grid(column=1, row=num, padx=5, pady=3)
        
        status = tk.Label(commentsView, text=x[3])
        status.grid(column=2, row=num, padx=5, pady=3)
        
        anmerkung = tk.Text(commentsView, wrap=tk.WORD, width=53, height=5)
        anmerkung.insert(tk.END, x[4])
        anmerkung.grid(column=3, row=num, padx=5, pady=3)
        
        num += 1

def configure_frame(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

def error(err_code):
    err_window = tk.Tk()
    
    errs = {'A001': 'Auftrag bereits eingetragen',
            'M001': 'Kein Mitarbeiter ausgewählt'}
    
    err_message = errs.get(err_code)
    
    err_print = 'Error %s: %s' % (err_code, err_message)
    
    err_label = tk.Label(err_window, text = err_print, font='Helvetica 16 bold')
    err_label.pack(padx=20, pady=20)
    
    err_window.mainloop()


# This function is not very flexible
def read_values(rep_id):
    #Outputs: values[0], status[1]
    connection_object = db_connect.open_connection()
    cursor = connection_object.cursor()
    
    # Could probably combine these three in a loop?
    query = 'SELECT * FROM rekla_vw WHERE auftrag = %s ORDER BY auftrag ASC' % rep_id
    cursor.execute(query)
    values = cursor.fetchall()
    
    query = 'SELECT * FROM rekla_status WHERE auftrag = %s ORDER BY datum DESC' % rep_id
    cursor.execute(query)
    status = cursor.fetchall()
    
    db_connect.close_connection(connection_object, cursor)
    return values, status
    
status_dict = util.configure_list('settings/list_status.csv')
mitarbeiter_dict = util.configure_list('settings/list_mitarbeiter.csv')
hersteller_dict = util.configure_list('settings/list_hersteller.csv')

if __name__  == '__main__':
    main()
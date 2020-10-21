# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:31:00 2020

@author: ryand

Goal: create a frame+canvas containing a scrollbar that hides itself when 
		not needed
"""

import tkinter as tk
from tkinter import ttk

class AutoScrollBar(tk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call('grid', 'remove', self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")

class ScrollableFrame(ttk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		canvas = tk.Canvas(self)
		scrollbar = AutoScrollBar(self, orient="vertical", command=canvas.yview)
		self.scrollable_frame = ttk.Frame(canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
			)

		canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')

		canvas.configure(yscrollcommand=scrollbar.set)

		canvas.grid(row=0, column=0)
		scrollbar.grid(row=0, column=1, sticky=tk.NS)
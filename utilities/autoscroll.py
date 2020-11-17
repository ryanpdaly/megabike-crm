# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:31:00 2020

@author: ryand

Goal: create a frame+canvas containing a scrollbar that hides itself when 
		not needed

Needs: Auto Resize function
		Relief of frame
		No way to pass background width
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
	def __init__(self, container, height, width, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		#self.viewFrame = tk.Tk()
		#self.canvas = tk.Canvas(self, height=450, width=980)
		
		self.height=height
		self.width=width
		
		self.canvas = tk.Canvas(self, height=self.height, width=self.width)
		self.scrollbar = AutoScrollBar(self, orient="vertical", command=self.canvas.yview)
		self.scrollable_frame = ttk.Frame(self.canvas)
		self.bind_frame()

	def bind_frame(self):
		self.scrollable_frame = ttk.Frame(self.canvas)
		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
			)

		self.canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')
		self.canvas.configure(yscrollcommand=self.scrollbar.set)
		self.canvas.grid(row=0, column=0)
		self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

	def clear_canvas(self):
		for child in self.canvas.winfo_children():
			child.destroy()

			self.bind_frame()

	def resize():
		pass

if __name__ == '__main__':
	root = tk.Tk()

	viewFrame = ScrollableFrame()

	for i in range(50):
		ttk.Label(frame.scrollable_frame)
import tkinter as tk
import tkinter.font as tkFont

import utilities.autoscroll as autoscroll

root = tk.Tk()

viewFrame = autoscroll.ScrollableFrame(root, height=600, width=600)
viewFrame.grid()

for index, font in enumerate(tkFont.families()):
	label=tk.Label(viewFrame.frame, text=font, font=(font, 14))
	label.grid(row=index, column=0, sticky=tk.W)

	#label_bold=tk.Label(viewFrame.frame, text=font, font=(font, 14), bold=True)
	#label_bold.grid(row=index, column=1, sticky=tk.W)

root.mainloop()
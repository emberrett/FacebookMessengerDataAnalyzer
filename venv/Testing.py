from tkcalendar import DateEntry
import tkinter as tk
root = tk.Tk()
cal = DateEntry(root, width=12, year=2019, month=6, day=22,
background='darkblue', foreground='white', borderwidth=2)
cal.pack(padx=10, pady=10)
root.mainloop()
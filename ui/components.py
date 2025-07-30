# atodumo_kun_gui/ui/components.py

import tkinter as tk

def create_label_entry_row(parent, label_text, font, label_width=10, entry_width=10):
    frame = tk.Frame(parent)
    label = tk.Label(frame, text=label_text, font=font, width=label_width, anchor="e")
    label.pack(side="left")
    entry = tk.Entry(frame, width=entry_width, font=font)
    entry.pack(side="left")
    frame.pack(pady=2)
    return entry

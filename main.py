import os
from tkinter import filedialog, messagebox
from config import *
import customtkinter as ctk
import tkinter as tk
from pypdf import PdfReader, PdfWriter
from split import *
from merge import *



file_paths = []

# hlavní okno
root = ctk.CTk()
root.geometry("500x420")
root.title("Pdf Tool")
root.resizable(False, False)

tabview = ctk.CTkTabview(master=root,width=380, height=380)
tabview.pack( fill="both", expand=True, padx=10, pady=10)

tab_split = tabview.add('Rozdělit PDF')
tab_merge = tabview.add('Sloučit PDF')

# oblast s výběrem souboru v tab_split
path_frame = ctk.CTkFrame(master=tab_split)
path_frame.pack( fill='x',  pady = (0, 20))
entry_path = ctk.CTkEntry(path_frame, width=300, font=main_font)
entry_path.grid(row=0, column=0, padx = 5)
select_button = ctk.CTkButton(path_frame, text="Vyber soubor", font=main_font, command=lambda :select_file(entry_path, info_label))
select_button.grid(row=0, column=1)

# info o počtu stránek a tlačítko rozdělit v tab_split
info_label = ctk.CTkLabel(tab_split, text="Počet stránek: ", font=main_font)
info_label.pack( anchor="w", padx=10)

split_button = ctk.CTkButton(tab_split, text='Rozdělit a uložit do složky', font=main_font, command=lambda :split_file(entry_path))
split_button.pack( fill='x', padx=10)

# oblast s výběrem stránky a uložení v tab_split
page_frame = ctk.CTkFrame(master=tab_split)
page_frame.pack( fill='x',  pady=(20, 0))
select_page_label = ctk.CTkLabel(page_frame, text='Číslo stránky: ', font=main_font)
select_page_label.grid(row=0, column=0, padx=5)
entry_page_number = ctk.CTkEntry(page_frame, font=main_font, width=50, textvariable=tk.StringVar(value='1'))
entry_page_number.grid(row=0, column=1, padx=5)
extract_button = ctk.CTkButton(tab_split,text='Uložit stránku jako...', font=main_font, command=lambda :extract_page(entry_path, entry_page_number))
extract_button.pack( anchor="w", pady=(5, 0), fill="x")

# tab_merge
info_merge_label = ctk.CTkLabel(tab_merge, text='Vyber PDF soubory ke sloučení (v pořadí, v jakém mají jít za sebou):')
info_merge_label.pack( anchor="w", padx=10)
list_frame = ctk.CTkFrame(master=tab_merge)
list_frame.pack( fill='both', pady=10)

# listbox s posuvníkem
listbox = tk.Listbox(list_frame, font=main_font)
listbox.pack( side='left', fill='both', pady=10, expand=True)
scrollbar = ctk.CTkScrollbar(list_frame, orientation='vertical', command=listbox.yview)
scrollbar.pack( side='right', fill='y')
listbox.configure(yscrollcommand=scrollbar.set)

# oblast s tlačítky
buttons_frame = ctk.CTkFrame(master=tab_merge)
buttons_frame.pack( fill='x', pady=10)
add_button = ctk.CTkButton(buttons_frame, text='Přidat soubory', font=main_font, command=lambda :add_files(listbox, file_paths))
add_button.pack(side='left', padx=3)
remove_button = ctk.CTkButton(buttons_frame, text='Odebrat soubor', font=main_font, command=lambda :remove_file(listbox, file_paths))
remove_button.pack(side='left', padx=3)
up_button = ctk.CTkButton(buttons_frame, text='Nahoru', width=80, font=main_font, command=lambda :move(listbox, -1, file_paths))
up_button.pack(side='left', padx=3)
down_button = ctk.CTkButton(buttons_frame, text='Dolu', width=80, font=main_font, command=lambda :move(listbox, 1, file_paths))
down_button.pack(side='left', padx=3)

merge_button = ctk.CTkButton(tab_merge, text='Sloučit a uložit jako...', font=main_font, command=lambda :merge_files(listbox, file_paths))
merge_button.pack(fill='x', padx=3)






root.mainloop()
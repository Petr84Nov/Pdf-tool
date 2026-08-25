import os
from tkinter import filedialog, messagebox
from config import *
import customtkinter as ctk
import tkinter as tk
from pypdf import PdfReader, PdfWriter


pages_number = 0

def select_file():
    file_path = filedialog.askopenfilename(
        title='Vyber PDF soubor',
        filetypes=[('PDF soubory', '.pdf')],
    )
    if file_path:
       entry_path.set(file_path)
       try:
            reader = PdfReader(file_path)
            info_label.configure(text=f'Počet stránek: {len(reader.pages)}')

       except Exception as e:
            info_label.configure(text=f'Nelze načíst soubor: {e}')

def split_file():
    file_path = entry_path.get()
    if file_path:
        output_directory = filedialog.askdirectory(title='Vyber složku pro uložení stránek')
        if output_directory:
            try:
                reader = PdfReader(file_path)
                # writer = PdfWriter()
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    output_filename = os.path.join(output_directory, f'{file_name}_{i +1}.pdf')
                    with open(output_filename, "wb") as f:
                        writer.write(f)
                messagebox.showinfo('Hotovo', f'Vytvořeno {len(reader.pages)} souborů ve složce: \n{output_directory}')
            except Exception as e:
                messagebox.showerror('Chyba', f'Rozdělení se nezdařilo: \n{e}')
        else:
            return
    else:
        messagebox.showwarning('Není vybrán soubor', 'Nejprve vyber pdf soubor')
        return

def extract_page():
    file_path = entry_path.get()
    if not file_path:
        messagebox.showwarning('Není vybrán soubor', 'Nejprve vyber pdf soubor')
        return
    try:
        page_number = int(entry_page_number.get())
    except ValueError:
        messagebox.showwarning('Neplatné číslo', 'Zadej platné číslo stránky')
        return

    try:
        reader = PdfReader(file_path)
        if not (1 <= page_number <= len(reader.pages)):
            messagebox.showwarning('Neplatné číslo', f'Zadej číslo stránky mezi 1 a {len(reader.pages)}.')
            return
    except Exception as e:
        messagebox.showerror('Chyba', 'Načtení souboru se nezdařilo')

    output_path = filedialog.asksaveasfilename(
         title='Uložit stránku jako',
         defaultextension='.pdf',
         filetypes=[('PDF soubor', '.pdf')],
         initialfile=f'stranka_{page_number}.pdf',
     )
    if not output_path:
        return

    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])
        with open(output_path, "wb") as f:
            writer.write(f)
    except Exception as e:
        messagebox.showerror('Chyba', f'Uložení stránky se nezdařilo: \n{e}')



root = ctk.CTk()
root.geometry("500x400")
root.title("Pdf Tool")
root.resizable(False, False)

tabview = ctk.CTkTabview(master=root,width=380, height=380)
tabview.pack( fill="both", expand=True, padx=10, pady=10)

tab_split = tabview.add('Rozdělit PDF')
tab_merge = tabview.add('Sloučit PDF')

path_frame = ctk.CTkFrame(master=tab_split)
path_frame.pack( fill='x',  pady = (0, 20))
entry_path = ctk.CTkEntry(path_frame, width=300, font=main_font)
entry_path.grid(row=0, column=0, padx = 5)
select_button = ctk.CTkButton(path_frame, text="Vyber soubor", font=main_font, command=lambda :select_file())
select_button.grid(row=0, column=1)

info_label = ctk.CTkLabel(tab_split, text="Počet stránek: ", font=main_font)
info_label.pack( anchor="w", padx=10)

split_button = ctk.CTkButton(tab_split, text='Rozdělit a uložit do složky', font=main_font, command=lambda :split_file())
split_button.pack( fill='x', padx=10)

page_frame = ctk.CTkFrame(master=tab_split)
page_frame.pack( fill='x',  pady=(20, 0))
select_page_label = ctk.CTkLabel(page_frame, text='Číslo stránky: ', font=main_font)
select_page_label.grid(row=0, column=0, padx=5)
entry_page_number = ctk.CTkEntry(page_frame, font=main_font, width=50, textvariable=tk.StringVar(value='1'))
entry_page_number.grid(row=0, column=1, padx=5)
extract_button = ctk.CTkButton(tab_split,text='Uložit stránku jako...', font=main_font, command=lambda :extract_page())
extract_button.pack( anchor="w", pady=(5, 0), fill="x")









root.mainloop()
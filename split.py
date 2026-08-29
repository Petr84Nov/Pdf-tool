import os
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import pdfplumber


# funkce pro výběr souboru
def select_file(entry_path, info_label):
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

# rozdělení souboru na jednotlivé stránky
def split_file(entry_path):
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

# vybrání pouze jedné stránky
def extract_page(entry_path, entry_page_number):
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
        messagebox.showinfo('Hotovo', 'Stránka úspěšně uložena')
    except Exception as e:
        messagebox.showerror('Chyba', f'Uložení stránky se nezdařilo: \n{e}')

def save_as_text(entry_path):
    file_path = entry_path.get()
    text = ''
    if not file_path:
        messagebox.showwarning('Není vybrán soubor', 'Nejprve vyber pdf soubor')
        return
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + '\n'
    except Exception as e:
        messagebox.showerror('Chyba', 'Uložení souboru se nezdařilo')

    output_path = filedialog.asksaveasfilename(
        title='Uložit soubor jako..',
        filetypes=[('txt soubor', '.txt')],
        defaultextension='.txt',
    )
    if not output_path:
        return

    try:
        with open(output_path, "w") as f:
            f.write(text)
        messagebox.showinfo('Hotovo', 'Soubor úspěšně uložen')
    except Exception as e:
        messagebox.showerror('Chyba', 'Uložení souboru se nezdařilo')

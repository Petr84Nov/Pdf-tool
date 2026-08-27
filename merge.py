import os
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter


def add_files(listbox, file_paths):
    paths = filedialog.askopenfilenames(
        title = "Vyber pdf soubory",
        filetypes = [("pdf", "*.pdf")],
    )
    for path in paths:
        file_paths.append(path)
        listbox.insert("end", os.path.basename(path))

def remove_file(listbox, file_paths):
    selected_files = list(listbox.curselection())
    if selected_files:
        for index in reversed(selected_files):
            listbox.delete(index)
            del file_paths[index]
    else:
        return

# posouvání v listboxu nahoru a dolů
def move(listbox, direction, file_paths):
    selected = list(listbox.curselection())
    if not selected:
        return
    for index in selected if direction < 0 else reversed(selected):
        new_index = index + direction
        if 0 <= new_index < listbox.size():
            file_paths[index], file_paths[new_index] = file_paths[new_index], file_paths[index]
            text = listbox.get(index)
            listbox.delete(index)
            listbox.insert(new_index, text)
            listbox.selection_set(new_index)

def merge_files(listbox, file_paths):
    if listbox.size() < 2:
        messagebox.showwarning("Málo souborů", "Vyber prosím alespoň dva PDF soubory.")
        return

    output_file = filedialog.asksaveasfilename(
        title = "Uložit sloučené PDF jako",
        defaultextension='.pdf',
        filetypes = [("PDF jako", "*.pdf")],
    )
    if not output_file:
        return

    try:
        writer = PdfWriter()
        for path in file_paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
        with (open(output_file, "wb")) as file:
            writer.write(file)
        messagebox.showinfo('Hotovo', f'Soubory byly sloučeny do: \n{output_file}')
    except Exception as e:
        messagebox.showinfo('Chyba', f'Sloučení se nezdařilo\n{e}')


# Exporting Selected DataFrame -------------Author: Yong Javen & Su Qin

from os import name
from tkinter import Message, Widget, filedialog , messagebox , ttk

def export_excel(df, selectedColumn):

    try:
        exported_data = df[selectedColumn].copy()
        exported_data.to_csv('Exported.csv', index=False)
        messagebox.showinfo("Confirmation","Your data has been exported!")
    except:
        messagebox.showinfo("Error","Your data cannot be exported!")
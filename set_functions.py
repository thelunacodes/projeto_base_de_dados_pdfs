import configparser, os, customtkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox


def setRootFolder(window:customtkinter.CTk) -> None:
    """Changes the root folder in the configuration file (settings.ini)
    """
    messagebox.showwarning(title="Atenção!", message="Pasta raiz não encontrada!")

    newRootPath = askdirectory(title="Selecione as pastas contendo os arquivos .pdf")
    window.after(0, lambda:window.wm_state("zoomed")) #Maximize window

    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.set("Database", "root_path", newRootPath)
    
    with open('settings.ini', 'w') as configFile:
        config.write(configFile)
    
    print("[DEBUG] New root file added successfully")
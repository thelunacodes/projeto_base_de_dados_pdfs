import configparser, os, customtkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox

def setConfigValue(section:str, key:str, newValue:str):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.set(section, key, newValue)

    with open('settings.ini', 'w') as configFile:
        config.write(configFile)

def setRootFolder(window:customtkinter.CTk) -> None:
    """Changes the root folder in the configuration file (settings.ini)
    """
    messagebox.showwarning(title="Atenção!", message="Pasta raiz não encontrada!")

    newRootPath = askdirectory(title="Selecione as pastas contendo os arquivos .pdf")
    window.after(0, lambda:window.wm_state("zoomed")) #Maximize window

    setConfigValue("Database", "root_path", newRootPath)
    
    print("[DEBUG] New root file added successfully")



import customtkinter

def openSettingsWindow(window:customtkinter.CTk):
    settingsWindow = customtkinter.CTkToplevel(window)
    settingsWindow.title("Configurações")

    width = 800
    height = 800
    screenwidth = settingsWindow.winfo_screenwidth()
    screenheight = settingsWindow.winfo_screenheight()

    x = int((screenwidth/2)-(width/2))
    y = int((screenheight/2)-(height/2))

    settingsWindow.geometry(f"{width}x{height}+{x}+{y}")
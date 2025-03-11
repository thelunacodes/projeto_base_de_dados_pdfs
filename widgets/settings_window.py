import customtkinter, sqlite3
from get_functions import getConfigValue
from set_functions import setConfigValue
from db_functions import changeRootFolder
from tkinter.filedialog import askdirectory
from tkinter import ttk

def changeTheme(theme:str, themeLabel:customtkinter.CTkLabel):
    customtkinter.set_appearance_mode(theme)
    themeLabel.configure(text=f"Mudar tema (Atual: {"Claro" if theme == "light" else "Escuro"})")

def searchNewRootPath(rootPathEntry:customtkinter.CTkEntry):
    newRootPath = askdirectory(title="Selecione as pastas contendo os arquivos .pdf")
    rootPathEntry.delete(0,"end")
    rootPathEntry.insert(0,newRootPath)

def applyBtn(rootPath:str, conn:sqlite3.Connection, window:customtkinter.CTk, table:ttk.Treeview):
    #Change window theme in the settings file
    setConfigValue("Interface", "window_theme", customtkinter.get_appearance_mode().lower())

    #Change root path in settings file and reload table
    if rootPath != getConfigValue("Database", "root_path"):
        setConfigValue("Database","root_path", rootPath)
        changeRootFolder(conn, window, table, rootPath) #Reload table
        

def okBtn(rootPath:str, conn:sqlite3.Connection, window:customtkinter.CTk, table:ttk.Treeview, settingsWindow:customtkinter.CTkToplevel, settingsIsOpen:customtkinter.BooleanVar):
    #Change window theme in the settings file
    setConfigValue("Interface", "window_theme", customtkinter.get_appearance_mode().lower())
    
    #Change root path in settings file and reload table
    if rootPath != getConfigValue("Database", "root_path"):
        setConfigValue("Database","root_path", rootPath)
        changeRootFolder(conn, window, table, rootPath) #Reload table

    settingsIsOpen.set(False)

    #Change root path in settings file and refresh table
    settingsWindow.destroy()

def cancelBtn(settingsWindow:customtkinter.CTkToplevel, settingsIsOpen:customtkinter.BooleanVar):
    #Return to original theme
    customtkinter.set_appearance_mode(getConfigValue("Interface", "window_theme"))

    settingsIsOpen.set(False)

    settingsWindow.destroy()

def openSettingsWindow(conn: sqlite3.Connection, window:customtkinter.CTk, table:ttk.Treeview, settingsIsOpen:customtkinter.BooleanVar):
    if settingsIsOpen.get() == False:
        settingsIsOpen.set(True)

        settingsWindow = customtkinter.CTkToplevel(window)
        settingsWindow.title("Configurações")
        settingsWindow.attributes("-topmost", True) 

        settingsWindow.protocol("WM_DELETE_WINDOW", lambda:cancelBtn(settingsWindow, settingsIsOpen))

        width = 700
        height = 700
        screenwidth = settingsWindow.winfo_screenwidth()
        screenheight = settingsWindow.winfo_screenheight()

        x = int((screenwidth/2)-(width/2))
        y = int((screenheight/2)-(height/2))

        settingsWindow.geometry(f"{width}x{height}+{x}+{y}")

        settingsHeader = customtkinter.CTkLabel(settingsWindow,
                                                text="Configurações", 
                                                font=("Arial", 16),
                                                )
        settingsHeader.pack(pady=(10,30))

        #Current Window theme Frame
        currTheme = customtkinter.StringVar(value=getConfigValue("Interface", "window_theme"))

        winThemeFrame = customtkinter.CTkFrame(settingsWindow,
                                            fg_color="transparent")
        
        winThemeLabel = customtkinter.CTkLabel(winThemeFrame, 
                                        text=f"Mudar tema (Atual: {"Claro" if currTheme.get().lower() == "light" else "Escuro"})")
        winThemeLabel.grid(column=0,
                        row=0,
                        padx=(0,10))

        winThemeSwitch = customtkinter.CTkSwitch(winThemeFrame,
                                                text="",
                                                onvalue="dark",
                                                offvalue="light",
                                                variable=currTheme,
                                                command=lambda:changeTheme(winThemeSwitch.get(), winThemeLabel))
        winThemeSwitch.grid(column=1,
                            row=0)
        
        winThemeFrame.pack(pady=(0,10),
                           fill="x",
                            padx=50)

        #New Root folder
        rootFolderFrame = customtkinter.CTkFrame(settingsWindow,
                                                fg_color="transparent")

        rootFolderLabel = customtkinter.CTkLabel(rootFolderFrame, 
                                                text="Pasta dos PDFs")
        rootFolderLabel.grid(column=0,
                            row=0)
        
        rootFolderEntry = customtkinter.CTkEntry(rootFolderFrame,
                                                width=400)

        rootFolderEntry.insert(0, getConfigValue("Database", "root_path"))

        rootFolderEntry.grid(column=1,
                            row=0,
                            padx=10,
                            sticky="ew")

        changeRootFolderBtn = customtkinter.CTkButton(rootFolderFrame,
                                                    text="Editar",
                                                    command=lambda: searchNewRootPath(rootFolderEntry))

        changeRootFolderBtn.grid(column=0,
                                row=1,
                                columnspan=2,
                                sticky="ne",
                                pady=(10,0))

        rootFolderFrame.pack(fill="x",
                             padx=50)


        #Buttons on the bottom of the window
        bottomBtnFrame = customtkinter.CTkFrame(settingsWindow,
                                                fg_color="transparent")
        bottomBtnFrame.pack(fill="both",
                            side="bottom", 
                            pady=10,
                            padx=10)

        bottomBtnFrame.columnconfigure(0, weight=1)

        okButton = customtkinter.CTkButton(bottomBtnFrame, 
                                        text="Ok",
                                        command=lambda:okBtn(rootFolderEntry.get(), conn, window, table, settingsWindow, settingsIsOpen))
        okButton.grid(column=0,
                    row=0,
                    sticky="e")
        
        applyButton = customtkinter.CTkButton(bottomBtnFrame, 
                                        text="Aplicar",
                                        command=lambda:applyBtn(rootFolderEntry.get(), conn, window, table ))
        applyButton.grid(column=1,
                    row=0,
                    padx=5,
                    sticky="e")
        
        okButton = customtkinter.CTkButton(bottomBtnFrame, 
                                        text="Cancelar",
                                        command=lambda:cancelBtn(settingsWindow, settingsIsOpen))
        okButton.grid(column=2,
                    row=0,
                    sticky="e")

  

    

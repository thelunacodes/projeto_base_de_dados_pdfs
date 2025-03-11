from connect_db import *
from db_functions import getConfigValue, managePDFDatabase
import customtkinter
from widgets.database_table import getDatabaseTable, reloadTable
from widgets.search_frame import getSearchFrame
from widgets.settings_window import openSettingsWindow

customtkinter.set_appearance_mode(getConfigValue("Interface", "window_theme"))

conn = connectDb() #Active connection with the local database
ROOT_FOLDER = getConfigValue("Database", "root_path") #Get root folder

window = customtkinter.CTk() #Create window
window.title("Base de Dados de PDFs") #Window title
window.after(0, lambda:window.wm_state("zoomed")) #Maximize window

searchValue = customtkinter.StringVar() #Stores the value on the search bar
isDescending = customtkinter.BooleanVar(value=False) #If the entries will be ordered in descending order, or not
displayCategory = customtkinter.StringVar(value="Todas Categorias")

settingsIsOpen = customtkinter.BooleanVar(value=False)


#Database Table
dbTable = getDatabaseTable(conn, window, searchValue, isDescending, displayCategory)

#Search frame
searchFrame = getSearchFrame(conn, dbTable, window, searchValue, isDescending, displayCategory)

searchFrame.pack(pady=(30,0),
              padx=50,
              expand=0,
              fill='x',
              )

dbTable.pack(pady=(30,0),
              padx=50,
              expand=True,
              fill='both',
              )

bottomFrame = customtkinter.CTkFrame(window,
                                     fg_color="transparent")

configButton = customtkinter.CTkButton(bottomFrame,
                             text="Configurações",
                             command=lambda:openSettingsWindow(conn, window, dbTable, settingsIsOpen))
configButton.grid(row=0,
                  column=0,
                  sticky="e")

reloadButton = customtkinter.CTkButton(bottomFrame,
                                        text="Recarregar",
                                        command=lambda:reloadTable(conn, dbTable, searchValue, window, isDescending, displayCategory))
reloadButton.grid(row=0,
                    column=1,
                    padx=(20,0),
                    sticky="e")

def databaseCheckLoop() -> None:
    """Performs a periodic check to verify the database's integrity and update any changes.

    The loop runs indefinitely at 5-second intervals. 
    """
    managePDFDatabase(conn, window, dbTable)
    reloadTable(conn, dbTable, searchValue, window, isDescending, displayCategory)
    window.after(5000, databaseCheckLoop) #Will check again after 5000 ms (5 seconds)

databaseCheckLoop()

bottomFrame.pack(pady=20,
                 padx=50,
                 fill='x',
                 side="right")
window.mainloop()

#End connection with the local database
disconnectDB(conn)



 
 
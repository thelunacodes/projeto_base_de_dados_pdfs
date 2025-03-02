from connect_db import *
from db_functions import *
import customtkinter, os
from widgets.database_table import getDatabaseTable, reloadTable
from widgets.search_frame import getSearchFrame

conn = connectDb() #Active connection with the local database
ROOT_FOLDER = getConfigValue("Database", "root_path") #Get root folder

customtkinter.set_appearance_mode("system")

window = customtkinter.CTk() #Create window
window.title("Base de Dados de PDFs") #Window title
window.after(0, lambda:window.wm_state("zoomed")) #Maximize window

searchValue = customtkinter.StringVar()

#Database Table
dbTable = getDatabaseTable(conn, window, searchValue)

#Search frame
searchFrame = getSearchFrame(conn, dbTable, window, searchValue)

searchFrame.pack(pady=(30,0),
              padx=50,
              expand=0,
              fill='x',
              )

dbTable.pack(pady=(30,0),
              padx=50,
              expand=1,
              fill='both',
              )

reloadButton = customtkinter.CTkButton(window,
                                        text="Recarregar",
                                        command=lambda:reloadTable(conn, dbTable, searchValue))
reloadButton.pack(pady=20,
                   padx=50,
                   side="right")

def databaseCheckLoop() -> None:
    """Performs a periodic check to verify the database's integrity and update any changes.

    The loop runs indefinitely at 5-second intervals. 
    """
    managePDFDatabase(conn)
    reloadTable(conn, dbTable, searchValue)
    window.after(5000, databaseCheckLoop) #Will check again after 5000 ms (5 seconds)

databaseCheckLoop()

window.mainloop()




 
 
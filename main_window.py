import customtkinter
from widgets.database_table import getDatabaseTable, reloadTable
from widgets.search_frame import getSearchFrame
from main import conn
from db_functions import managePDFDatabase

customtkinter.set_appearance_mode("system")

window = customtkinter.CTk() #Create window
window.title("Base de Dados de PDFs") #Window title
window.after(0, lambda:window.wm_state("zoomed")) #Maximize window

#Database Table
db_table = getDatabaseTable(conn, window)

#Search frame
search_frame = getSearchFrame(conn, db_table, window)
search_frame.pack(pady=(30,0),
              padx=50,
              expand=0,
              fill='x',
              )

db_table.pack(pady=(30,0),
              padx=50,
              expand=1,
              fill='both',
              )

reload_button = customtkinter.CTkButton(window,
                                        text="Recarregar",
                                        command=lambda:reloadTable(conn, db_table))
reload_button.pack(pady=20,
                   padx=50,
                   side="right")

def databaseCheckLoop():
    managePDFDatabase(conn)
    window.after(5000, databaseCheckLoop) #Will check again after 5000 ms (5 seconds)

databaseCheckLoop()

window.mainloop()
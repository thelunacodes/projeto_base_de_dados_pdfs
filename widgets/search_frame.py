import customtkinter
from tkinter import *
from tkinter import ttk
from widgets.database_table import categoryFilter, nameFilter, pressEnter
from get_functions import *


def getSearchFrame(conn:sqlite3.Connection, db_table:ttk.Treeview, window=Tk) -> Frame:
    #Seach frame
    searchFrame = customtkinter.CTkFrame(window,
                                         fg_color="transparent"
                                        )
    
    searchFrame.columnconfigure(2, weight=1)

    #Search bar 
    searchBar = customtkinter.CTkEntry(searchFrame,
                                        placeholder_text="Insira o nome do livro...",
                                        width=300
                                        )
    searchBar.grid(row=0, column=0)

    #Search button
    searchButton = customtkinter.CTkButton(searchFrame, 
                                           text="Pesquisar",
                                           command=lambda: nameFilter(conn, db_table, searchBar.get()))
    searchButton.grid(row=0, column=1, padx=(10,0))

    #Category filter
    categorias = getCategories(conn)
    categorias.insert(0,"Todas Categorias")
    categoryOptions = customtkinter.CTkOptionMenu(searchFrame,
                                                  values=categorias,
                                                  command=lambda category:categoryFilter(conn, db_table, category))
    categoryOptions.grid(row=0, column=2, sticky="e")

    

    #Make it so if the user presses "enter", it will also search what is written on the search bar
    searchBar.bind("<Return>", lambda event: pressEnter(event, conn, db_table, searchBar.get()))


    return searchFrame

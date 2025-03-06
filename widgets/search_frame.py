import customtkinter
from tkinter import ttk
from widgets.database_table import categoryFilter, nameFilter, pressEnter
from get_functions import *

def updateCategories(conn:sqlite3.Connection, categoryOptionMenu:customtkinter.CTkOptionMenu) -> None:
    """_summary_

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        categoryOptionMenu (customtkinter.CTkOptionMenu): Option Menu used to select the current category being displayed in the table.  
    """
    currentCategories = categoryOptionMenu.cget("values")
    allCategoriesList = getCategories(conn)

    #Remove old categories
    for oldCategory in currentCategories:
        if oldCategory in allCategoriesList:
            continue
        currentCategories.remove(oldCategory)

    #Add new categories 
    for newCategory in allCategoriesList:
        if newCategory in currentCategories:
            continue
        currentCategories.append(newCategory)

    currentCategories = sorted(currentCategories)
    currentCategories.insert(0,"Todas Categorias")

    categoryOptionMenu.configure(values=currentCategories)

def getSearchFrame(conn:sqlite3.Connection, db_table:ttk.Treeview, window:customtkinter.CTk, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar) -> customtkinter.CTkFrame:
    """Frame containing the search bar, the search button and a dropdown menu containing all the existent categories.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        db_table (ttk.Treeview): Table displaying information extracted from the local database.
        window (customtkinter.CTk): Program window where the Frame will be placed.
        searchValue (customtkinter.StringVar): Value being searched by the user.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        categoryValue (customtkinter.StringVar): Category of the items being displayed on the table.
    Returns:
        customtkinter.CTkFrame: A container widget containing the search bar, the search button and a dropdown menu.
    """

    #Seach frame
    searchFrame = customtkinter.CTkFrame(window,
                                         fg_color="transparent"
                                        )
    
    searchFrame.columnconfigure(2, weight=1)

    #Search bar 
    searchBar = customtkinter.CTkEntry(searchFrame,
                                        placeholder_text="Insira o nome do livro...",
                                        textvariable=searchValue,
                                        width=300
                                        )
    searchBar.grid(row=0, column=0)

    #Search button
    searchButton = customtkinter.CTkButton(searchFrame, 
                                           text="Pesquisar",
                                           command=lambda: nameFilter(conn, db_table, searchBar.get(), searchValue, isDescending, categoryValue))
    searchButton.grid(row=0, column=1, padx=(10,0))

    #Category filter
    categoryList = sorted(getCategories(conn))
    categoryList.insert(0,"Todas Categorias")
    categoryOptions = customtkinter.CTkOptionMenu(searchFrame,
                                                  values=categoryList,
                                                  command=lambda category:categoryFilter(conn, db_table, category, categoryValue, searchValue, isDescending))
    categoryOptions.grid(row=0, column=2, sticky="e")

    #Make it so if the user presses "enter", it will also search what is written on the search bar
    searchBar.bind("<Return>", lambda event: pressEnter(event, conn, db_table, searchBar.get(), searchValue, isDescending, categoryValue))

    def categoryCheckLoop() -> None:
        print("[DEBUG] Updating category list...")
        updateCategories(conn, categoryOptions)
        searchFrame.after(5000, categoryCheckLoop) #Will check again after 5000 ms (5 seconds)

    categoryCheckLoop()

    return searchFrame

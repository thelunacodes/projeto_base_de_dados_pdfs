import customtkinter, os, subprocess
from tkinter import ttk, messagebox
from widgets.table_handler import *
from get_functions import getEntriesByCategory
# from db_functions import managePDFDatabase

def categoryFilter(conn:sqlite3.Connection, table:ttk.Treeview, category:str, categoryValue:customtkinter.StringVar, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, searchBar:customtkinter.CTkEntry) -> None:
    """Retrieves all the entries from a specific category and displays them in the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        category (str): The category of the entries to retrieve from the local database.
        categoryValue (customtkinter.StringVar): StringVar used to track the current category being displayed.
        searchBar (customtkinter.CTkButton): Search bar used by the user to fetch one (or more) entries on the local database.
    """
    
    #Retrieve the current category
    categoryValue.set(category)

    #Change sorting order to ascendent
    isDescending.set(False)

    searchValue.set("")

    #Empty table
    emptyTable(table)

    #Set current category value
    categoryValue.set(category)

    #Get entries
    entryArray = getEntriesByCategory(conn, category) if category != "Todas Categorias" else getDatabaseEntries(conn, isDescending, categoryValue.get(), containing=searchValue.get())

    #Add entries to table
    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], str(getSizeConversion(int(entry[3]))), entry[4] ))

    if category == "Todas Categorias":
        searchBar.delete(0, "end")

def reloadTable(conn:sqlite3.Connection, table:ttk.Treeview, searchVar:customtkinter.StringVar, window:customtkinter.CTk, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar):
    """Adds new items to the table, and removes those that no longer exist.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        searchVar(customtkinter.StringVar): Value being searched by the user.
        window (customtkinter.CTk): Main program window.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        runManageDatabase (bool): If the "managePDFDatabase" function will be executed. Sometimes, it's not necessary.
    """

    print("[DEBUG] Reloading tables...")

    #Get entries
    entryArray = getDatabaseEntries(conn, isDescending, categoryValue.get(), containing=searchVar.get())

    #Get existing IDs from the table
    item_table_ids = [table.item(item, "values")[0] for item in table.get_children()]
    
    #Add new items
    for entry in entryArray:
        if str(entry[0]) in item_table_ids:
            continue
        table.insert("","end",values=(entry[0], entry[1], entry[2], str(getSizeConversion(int(entry[3]))), entry[4] ))

    #Remove items that no longer exist in the local database
    item_db_ids = [str(entry[0]) for entry in entryArray]

    for item in table.get_children():
        if table.item(item, "values")[0] in item_db_ids:
            continue
        table.delete(item)

def openFileByClick(event, conn:sqlite3.Connection, table:ttk.Treeview, searchVar:customtkinter.StringVar, window:customtkinter.CTk) -> None:
    """Opens the .pdf file when clicked in the table.

    Args:
        event (_type_): Event triggered when clicking twice.
        conn (sqlite3.Connection): An active connection to the local database
        table (ttk.Treeview): Table displaying information from the local database.
        searchValue(customtkinter.StringVar): Value being searched by the user.
        window (customtkinter.CTk): Main program window.
    """

    #Retrieve selected item
    selectedItem = list(table.item(table.selection(), "values"))
    
    #Check if the selected item is one of the table items
    if len(selectedItem) == 5:
        itemFilePath = selectedItem[4]

        #Check if file exists
        if os.path.exists(itemFilePath):
            #Open file
            subprocess.Popen([itemFilePath], shell=True)
        else:
            #If file no longer exists, an error message will be displayed and the table will be reloaded
            messagebox.askokcancel(title="Erro!", message="O arquivo não foi encontrado!")
            reloadTable(conn, table, searchVar, window)

def nameFilter(conn:sqlite3.Connection, table:ttk.Treeview, name:str, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar) -> None:
    """Retrieves all the entries containing a specific name/word and displays them in the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        name (str): The name/word being searched in local database.
        searchValue(customtkinter.StringVar): Value being searched by the user.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.

    """

    #Set isDescending value to False
    isDescending.set(False)

    #Set search value
    searchValue.set(name)

    #Empty table
    emptyTable(table)

    #Insert search results into table
    fillTable(conn, table, isDescending, categoryValue, searchValue=name)


def pressEnter(event, conn:sqlite3.Connection, table:ttk.Treeview, name:str, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar) -> None:
    """Retrieves all the entries containing a specific name (or word) by pressing the 'Enter' key, and displays them in the table.

    Args:
        event (_type_): Event triggered when pressing the 'Enter' key.
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        name (str): The name (or word) of the entries to retrieve from the local database.
        searchValue (customtkinter.StringVar): Value being searched by the user.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        categoryValue (customtkinter.StringVar): StringVar used to track the current category being displayed.
    """

    #Set isDescending value to False
    isDescending.set(False)

    #Set search value
    searchValue.set(name)

    #Empty table
    emptyTable(table)

    #Insert search results into table
    fillTable(conn, table, isDescending, categoryValue, searchValue=name)

def getDatabaseTable(conn:sqlite3.Connection, window:customtkinter.CTk, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar) -> ttk.Treeview:
    """Creates and populates a table displaying information from the local database.

    Args:
        conn (sqlite3.Connection): An active connection to the local database.
        window (customtkinter.CTk): Main program window.
        searchValue (customtkinter.StringVar): Value being searched by the user.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        categoryValue (customtkinter.StringVar): Category of the items being displayed on the table.
    Returns:
        ttk.Treeview: Table containing information from the local database.
    """

    db_table = ttk.Treeview(window,
                            columns=("id", "name", "category", "file_size", "file_path"),
                            show="headings",)

    #Set column name
    db_table.heading("id", text="Id", command=lambda:orderByHeader(conn,db_table,"id", searchValue, isDescending, categoryValue))
    db_table.heading("name", text="Nome", command=lambda:orderByHeader(conn,db_table,"name", searchValue, isDescending, categoryValue))
    db_table.heading("category", text="Categoria", command=lambda:orderByHeader(conn,db_table,"category", searchValue, isDescending, categoryValue))
    db_table.heading("file_size", text="Tamanho", command=lambda:orderByHeader(conn,db_table,"file_size", searchValue, isDescending, categoryValue))
    db_table.heading("file_path", text="Caminho", command=lambda:orderByHeader(conn,db_table,"file_path", searchValue, isDescending, categoryValue))

    #Set column size
    db_table.column("id", width=1, anchor="center")  
    db_table.column("name", width=200)  
    db_table.column("category", width=1, anchor="center")  
    db_table.column("file_size", width=1, anchor="center")  
    db_table.column("file_path", width=700)

    #Adds items to the table
    fillTable(conn, db_table, isDescending, categoryValue)

    #If user clicks on one items on the table, the file will be opened
    db_table.bind("<Double-1>", lambda event:openFileByClick(event, conn, db_table, searchValue, window))

    

    return db_table
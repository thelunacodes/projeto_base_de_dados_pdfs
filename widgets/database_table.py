import customtkinter, os, subprocess
from tkinter import *
from tkinter import ttk, messagebox
from get_functions import *
from db_functions import *

def fillTable(conn:sqlite3.Connection, table:ttk.Treeview ,orderBy:str="id", searchValue:str=None) -> None:
    """Insert all entries from the local database into the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        orderBy (str, optional): Criteria by which the data will be organized in the table. Defaults to "id".
        searchValue(str, optional): Value being searched by the user.
    """

    entryArray = getDatabaseEntries(conn, orderBy, searchValue)

    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
    
def emptyTable(table:ttk.Treeview) -> None:
    """Removes all the items from the table.

    Args:
        table (ttk.Treeview): Table containing all the items from the local database.
    """
    for row in table.get_children():
        table.delete(row)

def categoryFilter(conn:sqlite3.Connection, table:ttk.Treeview, category:str) -> None:
    """Retrieves all the entries from a specific category and displays them in the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        category (str): The category of the entries to retrieve from the local database.
    """

    #Empty table
    emptyTable(table)

    #Get entries
    entryArray = getEntriesByCategory(conn, category) if category != "Todas Categorias" else getDatabaseEntries(conn)

    #Add entries to table
    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))

def orderByHeader(conn:sqlite3.Connection, table:ttk.Treeview, headerName:str, searchValue:customtkinter.StringVar):
    """Sorts the items in the table based on which header the user clicked on.

    Args:
        conn (sqlite3.Connection): An active connection to the database.
        table (ttk.Treeview): Table displaying information from the local database.
        headerName (str): Name of the clicked header
        searchValue (customtkinter.StringVar): Value being searched by the user.
    """
    #Empty table
    emptyTable(table)

    #Reinsert items into the array using a sorted list of items
    fillTable(conn, table, headerName,searchValue.get())

def reloadTable(conn:sqlite3.Connection, table:ttk.Treeview, searchVar:customtkinter.StringVar):
    """Adds new items to the table, and removes those that no longer exist.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        searchValue(customtkinter.StringVar): Value being searched by the user.
    """

    #Search new files, check if the root path still exists, and remove items that no longer exist
    managePDFDatabase(conn)

    #Get entries
    entryArray = getDatabaseEntries(conn, containing=searchVar.get())

    #Get existing IDs from the table
    item_table_ids = [table.item(item, "values")[0] for item in table.get_children()]
    
    #Add new items
    for entry in entryArray:
        if str(entry[0]) in item_table_ids:
            continue
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))

    #Remove items that no longer exist in the local database
    item_db_ids = [str(entry[0]) for entry in entryArray]

    for item in table.get_children():
        if table.item(item, "values")[0] in item_db_ids:
            continue
        table.delete(item)

def openFileByClick(event, conn:sqlite3.Connection, table:ttk.Treeview) -> None:
    """Opens the .pdf file when clicked in the table.

    Args:
        event (_type_): Event triggered when clicking twice.
        conn (sqlite3.Connection): An active connection to the local database
        table (ttk.Treeview): Table displaying information from the local database.
    """

    #Retrieve selected item
    selectedItem = list(table.item(table.selection(), "values"))
    
    #Check if the selected item is one of the table items
    if len(selectedItem) == 6:
        itemFilePath = selectedItem[5]

        #Check if file exists
        if os.path.exists(itemFilePath):
            #Open file
            subprocess.Popen([itemFilePath], shell=True)
        else:
            #If file no longer exists, an error message will be displayed and the table will be reloaded
            messagebox.askokcancel(title="Erro!", message="O arquivo não foi encontrado!")
            reloadTable(conn, table)

def nameFilter(conn:sqlite3.Connection, table:ttk.Treeview, name:str, searchValue:customtkinter.StringVar) -> None:
    """Retrieves all the entries containing a specific name/word and displays them in the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        name (str): The name/word being searched in local database.
        searchValue(customtkinter.StringVar): Value being searched by the user.
    """

    #Empty table
    emptyTable(table)

    #Insert search results into table
    fillTable(conn,table,searchValue=name)

    #Set search value
    searchValue.set(name)

def pressEnter(event, conn:sqlite3.Connection, table:ttk.Treeview, name:str, searchValue:customtkinter.StringVar) -> None:
    """Retrieves all the entries containing a specific name (or word) by pressing the 'Enter' key, and displays them in the table.

    Args:
        event (_type_): Event triggered when pressing the 'Enter' key.
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        name (str): The name (or word) of the entries to retrieve from the local database.
        searchValue (customtkinter.StringVar): Value being searched by the user.
    """
    #Set search value
    searchValue.set(name)
    #Empty table
    emptyTable(table)

    #Insert search results into table
    fillTable(conn,table,searchValue=name)

def getDatabaseTable(conn:sqlite3.Connection, window:Tk, searchValue:customtkinter.StringVar) -> ttk.Treeview:
    """Creates and populates a table displaying information from the local database.

    Args:
        conn (sqlite3.Connection): An active connection to the local database.
        window (Tk): Main program window.
        searchValue (customtkinter.StringVar): Value being searched by the user.
    Returns:
        ttk.Treeview: Table containing information from the local database.
    """

    db_table = ttk.Treeview(window,
                            columns=("id", "name", "category", "num_pages", "file_size", "file_path"),
                            show="headings",)
    
    #Set column name
    db_table.heading("id", text="Id", command=lambda:orderByHeader(conn,db_table,"id", searchValue))
    db_table.heading("name", text="Nome", command=lambda:orderByHeader(conn,db_table,"name", searchValue))
    db_table.heading("category", text="Categoria", command=lambda:orderByHeader(conn,db_table,"category", searchValue))
    db_table.heading("num_pages", text="Páginas", command=lambda:orderByHeader(conn,db_table,"num_pages", searchValue))
    db_table.heading("file_size", text="Tamanho", command=lambda:orderByHeader(conn,db_table,"file_size", searchValue))
    db_table.heading("file_path", text="Caminho", command=lambda:orderByHeader(conn,db_table,"file_path", searchValue))

    #Set column size
    db_table.column("id", width=1, anchor="center")  
    db_table.column("name", width=200)  
    db_table.column("category", width=1, anchor="center")  
    db_table.column("num_pages", width=1, anchor="center")  
    db_table.column("file_size", width=1, anchor="center")  
    db_table.column("file_path", width=700)

    #Adds items to the table
    fillTable(conn, db_table)

    #If user clicks on one items on the table, the file will be opened
    db_table.bind("<Double-1>", lambda event:openFileByClick(event, conn, db_table))

    return db_table
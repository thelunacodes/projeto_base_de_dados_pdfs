import sqlite3, customtkinter
from tkinter import ttk
from get_functions import getDatabaseEntries,getSizeConversion

def emptyTable(table:ttk.Treeview) -> None:
    """Removes all the items from the table.

    Args:
        table (ttk.Treeview): Table containing all the items from the local database.
    """
    for row in table.get_children():
        table.delete(row)

def fillTable(conn:sqlite3.Connection, table:ttk.Treeview, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar="Todas Categorias", orderBy:str="id", searchValue:customtkinter.StringVar=None) -> None:
    """Insert all entries from the local database into the table.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        table (ttk.Treeview): Table displaying information from the local database.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        categoryValue (customtkinter.StringVar, optional): Category of the items being displayed on the table.
        orderBy (str, optional): Criteria by which the data will be organized in the table. Defaults to "id".
        searchValue(str, optional): Value being searched by the user.
    """

    entryArray = getDatabaseEntries(conn, isDescending, categoryValue.get(), orderBy, searchValue)

    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], str(getSizeConversion(int(entry[4]))), entry[5]))
    
def orderByHeader(conn:sqlite3.Connection, table:ttk.Treeview, headerName:str, searchValue:customtkinter.StringVar, isDescending:customtkinter.BooleanVar, categoryValue:customtkinter.StringVar):
    """Sorts the items in the table based on which header the user clicked on.

    Args:
        conn (sqlite3.Connection): An active connection to the database.
        table (ttk.Treeview): Table displaying information from the local database.
        headerName (str): Name of the clicked header
        searchValue (customtkinter.StringVar): Value being searched by the user.
        isDescending (customtkinter.BoolVar): If the entries will be ordered in descending order, or not.
        categoryValue (customtkinter.StringVar): Category of the items being displayed on the table.
    """
    #Empty table
    emptyTable(table)

    #Reinsert items into the array using a sorted list of items
    fillTable(conn, table, isDescending, categoryValue, headerName, searchValue.get())

    #Change isDescending value
    isDescending.set(not isDescending.get())
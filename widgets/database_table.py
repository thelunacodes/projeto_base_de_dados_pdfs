import customtkinter
from tkinter import *
from tkinter import ttk
from get_functions import *
from db_functions import *

def fillTable(conn:sqlite3.Connection, table:ttk.Treeview ,orderBy:str="id", category:str=None) -> None:
    entryArray = getDatabaseEntries(conn, orderBy)

    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
        #print(f"Arquivo \"{entry[1]}\" adicionado! ({i+1}/{len(entryArray)})")
    
def emptyTable(table:ttk.Treeview) -> None:
    for row in table.get_children():
        table.delete(row)

def categoryFilter(conn:sqlite3.Connection, table:ttk.Treeview, category:str) -> None:
    #Empty table
    emptyTable(table)

    #Get entries
    entryArray = getEntriesByCategory(conn, category) if category != "Todas Categorias" else getDatabaseEntries(conn)

    #Add entries to table
    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
        #print(f"Arquivo \"{entry[1]}\" adicionado! ({i+1}/{len(entryArray)})")

def reloadTable(conn:sqlite3.Connection, table:ttk.Treeview):
    #Search new files, check if the root path still exists, and remove items that no longer exist
    managePDFDatabase(conn)

    #Get entries
    entryArray = getDatabaseEntries(conn)

    #Get existing IDs from the table
    item_table_ids = [table.item(item, "values")[0] for item in table.get_children()]
    
    #Add new items
    for entry in entryArray:
        if str(entry[0]) in item_table_ids:
            continue
        # print(f"{type(entry[0])} | {type(item_table_ids[0])}")
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
        print(f"Arquivo \"{entry[1]}\" adicionado!")

    #Remove items that no longer exist in the local database
    item_db_ids = [str(entry[0]) for entry in entryArray]

    for item in table.get_children():
        if table.item(item, "values")[0] in item_db_ids:
            continue
        print(f"O item {table.item(item, "values")[1]} não existe mais!")


def nameFilter(conn:sqlite3.Connection, table:ttk.Treeview, name:str) -> None:
    #Empty table
    emptyTable(table)

    #Get entries
    entryArray = getEntriesByName(conn, name)

    #Add entries to table
    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
        #print(f"Arquivo \"{entry[1]}\" adicionado! ({i+1}/{len(entryArray)})")

def pressEnter(event, conn:sqlite3.Connection, table:ttk.Treeview, name:str) -> None:
    #Empty table
    emptyTable(table)

    #Get entries
    entryArray = getEntriesByName(conn, name)

    #Add entries to table
    for i, entry in enumerate(entryArray):
        table.insert("","end",values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5] ))
        #print(f"Arquivo \"{entry[1]}\" adicionado! ({i+1}/{len(entryArray)})")

def getDatabaseTable(conn:sqlite3.Connection, window:Tk) -> ttk.Treeview:
    db_table = ttk.Treeview(window,
                            columns=("id", "name", "category", "num_pages", "file_size", "file_path"),
                            show="headings",)
    
    #Set column name
    db_table.heading("id", text="Id")
    db_table.heading("name", text="Nome")
    db_table.heading("category", text="Categoria")
    db_table.heading("num_pages", text="Páginas")
    db_table.heading("file_size", text="Tamanho")
    db_table.heading("file_path", text="Caminho")

    #Set column size
    db_table.column("id", width=1, anchor="center")  
    db_table.column("name", width=200)  
    db_table.column("category", width=1, anchor="center")  
    db_table.column("num_pages", width=1, anchor="center")  
    db_table.column("file_size", width=1, anchor="center")  
    db_table.column("file_path", width=700)

    fillTable(conn, db_table)

    return db_table
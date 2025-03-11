import sqlite3, traceback, os, configparser, fitz, customtkinter
from spire.pdf.common import *
from spire.pdf import PdfDocument

def getConfigValue(section:str, key:str) -> str:
    """Retrieves a value from the configuration file (settings.ini). 

    Args:
        section (str): The section in the configuration file where the value is.
        key (str): Key of the value being retrieved.

    Returns:
        str: Value associated with a certain key, in a certain section.
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')

    return config.get(section, key)

def getPathArray(conn:sqlite3.Connection) -> list:
    """Retrieves an array with all paths registered in the local database.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.

    Returns:
        list: List of file paths in the database.
    """
    #Get current PDF paths list
    cursor = conn.cursor()
    sql = "SELECT file_path FROM books;"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()

    #Remove items from tuple
    pathArray = [path[0] for path in result]

    return pathArray

def getSizeConversion(bytesValue:int) -> str:    
    kiloValue = bytesValue / 1024
    if kiloValue >= 1024:
        megaValue = bytesValue / (1024 * 1024)
        if megaValue >= 1024:
            gigaValue = bytesValue / (1024 * 1024 * 1024)
            return f"{gigaValue:.1f} GB"
        return f"{megaValue:.1f} MB"
    return f"{kiloValue:.1f} KB"

def getFileInfo(path:str) -> list:
    """Collects information about a specific .pdf file located at a certain file path.

    Args:
        path (str): Absolute path of the .pdf file being analysed.

    Returns:
        list: The .pdf file's name, category, number of pages, and size (in bytes).
    """
    fileName = os.path.basename(path) #name
    
    if os.path.dirname(path) == getConfigValue("Database", "root_path"):
        fileCategory = "-"
    else:
        fileCategory = os.path.basename(os.path.dirname(path)) #category

    try:
        pdf = PdfDocument()
        with open(path, "rb") as pdfFile: 
            pdf.LoadFromFile(path)
            numberOfPages = pdf.Pages.Count # num_pages
    except Exception:
        print(traceback.format_exc())

    fileSize = os.path.getsize(path) #file_size

    return fileName, fileCategory, numberOfPages, fileSize

def getDatabaseEntries(conn:sqlite3.Connection, isDescending:customtkinter.BooleanVar, category:str, orderBy:str="id", containing:str=None) -> list:
    """Retrieves all the entries from the local database.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        isDescending (customtkinter.BooleanVar): If the entries will be ordered in descending order, or not.
        category (str): Category of the items being displayed on the table.
        orderBy (str, optional): Criteria by which the data will be organized in the table. Defaults to "id".

    Returns:
        list: List containing all the entries from the local database.
    """

    if orderBy not in ["id", "name", "category", "num_pages", "file_size", "file_path"]:
        return []
    
    sql = f"SELECT * FROM books {f"WHERE name LIKE '%{containing}%'" if containing != None else ""} {f"{"AND" if containing != None and category != "Todas Categorias" else ""}"} {f"category='{category}'" if category != "Todas Categorias" else ""} ORDER BY {orderBy} {"DESC" if isDescending.get() else "ASC"};"
    print(sql)

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = list(cursor.fetchall())
    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()

    entryList = [list(entry) for entry in result]
    return entryList

def getCategories(conn:sqlite3.Connection) -> list:
    """Retrieves all the distinct categories from the local database. 

    Args:
        conn (sqlite3.Connection): An active connection with the local database.

    Returns:
        list: List containing all the categories registered in the local database.
    """
    sql = f"SELECT DISTINCT category FROM books;"

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = list(cursor.fetchall())
        
    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()

    categoryList = [category[0] for category in result]
    return categoryList

def getEntriesByCategory(conn:sqlite3.Connection, category:str)->list:
    """Retrieves all the entries from a specific category.

    Args:
        conn (sqlite3.Connection): An active connection with the database.
        category (str): The category of the entries to retrieve from the local database.

    Returns:
        list: List containing all the database entries from a specific category.
    """

    sql = f"SELECT * FROM books WHERE category=?"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, (category,))
        result = list(cursor.fetchall())
    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()
    
    entryList = [list(entry) for entry in result]
    return entryList

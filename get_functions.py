import sqlite3, traceback, os, configparser, fitz
from spire.pdf.common import *
from spire.pdf import *

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
            print(f"Pages: {numberOfPages}")
    except Exception:
        print(traceback.format_exc())
        
    fileSize = os.path.getsize(path) #file_size

    return fileName, fileCategory, numberOfPages, fileSize

def getDatabaseEntries(conn:sqlite3.Connection, orderBy:str="id") -> list:
    if orderBy not in ["id", "name", "category", "num_pages", "file_size", "file_path"]:
        return []
    
    sql = f"SELECT * FROM books ORDER BY {orderBy};"

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

def getEntriesByName(conn:sqlite3.Connection, name:str) -> list:
    sql = f"SELECT * FROM books WHERE name LIKE '%{name}%';"

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()
    
    entryList = [list(entry) for entry in result]
    return entryList
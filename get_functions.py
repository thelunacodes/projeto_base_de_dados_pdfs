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
    except Exception:
        print(traceback.format_exc())
        
    fileSize = os.path.getsize(path) #file_size

    return fileName, fileCategory, numberOfPages, fileSize

def getDatabaseEntries(conn:sqlite3.Connection, orderBy:str="id", containing:str=None) -> list:
    """Retrieves all the entries from the local database.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
        orderBy (str, optional): Criteria by which the data will be organized in the table. Defaults to "id".

    Returns:
        list: List containing all the entries from the local database.
    """

    if orderBy not in ["id", "name", "category", "num_pages", "file_size", "file_path"]:
        return []
    
    sql = f"SELECT * FROM books {f"WHERE name LIKE '%{containing}%'" if containing != None else ""} ORDER BY {orderBy};"
    
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

def getId(entryArray:list) -> str:
    """Retrieves the "id" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "id" value.
    """
    return entryArray[0]

def getName(entryArray:list) -> str:
    """Retrieves the "name" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "name" value.
    """

    return entryArray[1]

def getCategory(entryArray:list) -> str:
    """Retrieves the "category" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "category" value.
    """

    return entryArray[2]

def getNumPag(entryArray:list) -> str:
    """Retrieves the "num_pag" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "num_pag" value.
    """

    return entryArray[3]

def getFileSize(entryArray:list) -> str:
    """Retrieves the "file_size" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "file_size" value.
    """

    return entryArray[4]

def getFilePath(entryArray:list) -> str:
    """Retrieves the "num_pag" value from an array containing information of a specific entry of the local database

    Args:
        entryArray (list): Array containing information of a specific entry of the array.

    Returns:
        str: The "num_pag" value.
    """

    return entryArray[5]
import sqlite3, traceback, os
from get_functions import *
from set_functions import *

def addFileToDB(name:str, category:str, numPages:int, fileSize:float, path:str, conn:sqlite3.Connection) -> None:
    """Adds the .pdf file to the local database.

    Args:
        name (str): Name of the file.
        category (str): Category of the file.
        numPages (int): Number of pages in the file.
        fileSize (float): Size of the file (in bytes).
        path (str): Path where the file is located.
        conn (sqlite3.Connection): An active connection with the database
    """

    sql = "INSERT INTO books (name, category, num_pages, file_size, file_path) VALUES (?, ?, ?, ?, ?);"

    cursor = conn.cursor()
    try:
        cursor.execute(sql, (name, category, numPages, fileSize, path))
    except Exception:
        print(traceback.format_exc())
    finally:
        conn.commit()
        cursor.close()

def removeFileFromDB(path:str, conn:sqlite3.Connection) -> None:
    """Removes a .pdf file from the local database.

    Args:
        path (str): Path of the file being removed.
        conn (sqlite3.Connection): Active connection with the local database.
    """
    cursor = conn.cursor()
    sql = f"DELETE FROM books WHERE file_path='{path}';"
    try:
        cursor.execute(sql)
    except Exception:
        print(traceback.format_exc())
    finally:
        conn.commit()
        cursor.close()

def searchNewFiles(path:str, conn:sqlite3.Connection, pathSet:set) -> None:
    """Searches for .pdf files that are not in the local database.

    Args:
        path (str): The path of the directory where the program is searching for .pdf files.
        conn (sqlite3.Connection): An active connection to the local database.
        pathSet (set): Set of paths that are already registered in the database. 
    """
    #The program will go through all the files in the current path
    for file in os.listdir(path):
        #Full path of the current file/directory
        currentPath = os.path.join(path, file)

        #Check if the current path is a .pdf file
        if os.path.isfile(currentPath) and currentPath.endswith(".pdf"): 

            #If the .pdf file is not in the local database, it will be added
            if currentPath not in pathSet: 
                print(f"[DEBUG] New .pdf file found: {file}")
                fileName, fileCategory, numberOfPages, fileSize = getFileInfo(currentPath)
                addFileToDB(fileName, fileCategory, numberOfPages, fileSize, currentPath, conn)
        
        #If the current path is a directory, we'll search within it
        elif os.path.isdir(currentPath):
            searchNewFiles(currentPath, conn, pathSet)

def managePDFDatabase(conn:sqlite3.Connection) -> None:
    """Function responsible for managing the local database. It will do things, such as, checking if the root path is valid, if there's any new files to add to the database or if any files were deleted during the program runtime.

    Args:
        conn (sqlite3.Connection): An active connection with the local database.
    """
    print("[DEBUG] Checking database...")
    
    rootPath = getConfigValue("Database", "root_path")

    #Check if root path exists
    if not os.path.exists(rootPath):
        print("[DEBUG] No root path found!")
        setRootFolder()
        rootPath = getConfigValue("Database", "root_path")

    #Check if all the files registered in the local database still exist
    for p in set(getPathArray(conn)):
        if not os.path.exists(p):
            print(f"[DEBUG] Inexistent .pdf file found and deleted: {os.path.basename(p)}")
            removeFileFromDB(p, conn)
    
    #Search for new files to add to the database
    searchNewFiles(rootPath, conn, set(getPathArray(conn)))

        

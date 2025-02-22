import configparser, os

def setRootFolder() -> None:
    """Changes the root folder in the configuration file (settings.ini)
    """
    
    while True:
        newRootPath = input("Insert new a root path: ")
        if os.path.exists(newRootPath) and os.path.isdir(newRootPath):
            break
        print("[DEBUG] The root path has to be a folder!")

    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.set("Database", "root_path", newRootPath)
    
    with open('settings.ini', 'w') as configFile:
        config.write(configFile)
    
    print("[DEBUG] New root file added successfully")
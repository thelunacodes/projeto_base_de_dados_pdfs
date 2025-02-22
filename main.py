from connect_db import *
from db_functions import *
from get_functions import *
import os

conn = connectDb()
ROOT_FOLDER = getConfigValue("Database", "root_path")

managePDFDatabase(conn)
 
 
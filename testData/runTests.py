# This module tests the different database functions with mock data from
# Mockaroo.com
import time
import json
from pprint import pprint
import sys
sys.path.insert(0, '../app/')
from database import Database

def loadData(name):
    with open(name) as data_file:    
        data = json.load(data_file)
    return data 

def testUserCreation(data, db = None):
    if(not db):
        db = Database()
    for d in data:
        db.createUser(**d)

def testUserDelete(data, db = None):
    if(not db):
        db = Database()
    db = Database()
    pass

def testUserSearchByEmail(data, db = None):
    if(not db):
        db = Database()
    db = Database()
    for d in data:
        user = db.readUserByEmail(d["email"])
        if(not user):
            try:
                raise Exception("Error en la lectura de datos." \
                                "Email no encontrado")
            except Exception as error:
                raise
        
def defaultDataTests(reset = False):
    """
    Runs default tests for the database. Each file of mock data contains
    1000 registers in json format
    """
    userDataPaths = ['USERS_MOCK_DATA'+str(i)+'.json' for i in range(1,6)]
    db = Database(reset)
    startTime = time.time()
    #Tests for user creation
    for i,path in enumerate(userDataPaths):
        print("------ DATASET No." + str(i+1) + " ------")
        
        startPathTime=startLoadData = time.time()
        data = loadData(path)
        print("Tiempo de carga de datos: " + "{:f}".format((time.time()-startLoadData)) + " segundos.")
        
        startCreationTime = time.time()
        testUserCreation(data, db)
        totalCreationTime = time.time()-startCreationTime
        
        startReadingTime = time.time()
        testUserSearchByEmail(data, db)
        totalReadingTime = time.time()-startReadingTime
        
        totalSetTime = time.time()-startPathTime
        
        print("Tiempo de creación: " + "{:f}".format(totalCreationTime) + " segundos.")
        print("Tiempo de lectura: " + "{:f}".format(totalReadingTime) + " segundos.")
        print("Tiempo total de dataset: " + "{:f}".format(totalSetTime) + " segundos.")
        print("--------------------------\n")

defaultDataTests(True)
from subprocess import call
import argparse, sys
from flask import Flask
from flask_cors import CORS
from flask import request
import requests, json, psycopg2
from psycopg2.extras import RealDictCursor
from os import walk

#app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}})
parser=argparse.ArgumentParser()
#pip install Flask
#pip install Requests
#pip install psycopg2
#pip install -U flask-cors
#python3 replica-from-files.py --username "gunter@redcompany.com.br" --password "red321Company" --hostname "192.168.100.236" --database "wm3"
#Send request curl --location --request POST 'http://localhost:8081/postgres/replica/TestsJson' --header 'Content-Type: application/json' --data-raw '[{"data":"daasdasdasd", "test":"asdasdasd"},{"data":"daasdasdasd", "test":"asdasdasd"}]'

listPrimaryKeyNames = {
    "RMW-USUARIO": [
        "id-usuario"
    ],
    "TestsJson": [
        "data"
    ]
}


def getparameters():
    parser.add_argument('--username', help='username', type=str, required=True)
    parser.add_argument('--password', help='password', type=str, required=True)
    parser.add_argument('--hostname', help='hostname', type=str, required=True)
    parser.add_argument('--database', help='database', type=str, required=True)
    
    args=parser.parse_args()
    #print("POSTGRES_USERNAME: " + args.username)
    #print("POSTGRES_PASSWORD: " + args.password)
    #print("POSTGRES_HOSTNAME: " + args.hostname)
    #print("POSTGRES_DATABASE: " + args.database)

#@app.route('/postgres/replica/<tableName>', methods=['POST'])
def replicaDataBaseFromProgresToPostgres():

    #content = request.json
    #content = [{'nome':'daasdasdasd', 'test':'asdasdasd'},{'data':'daasdasdasd', 'test':'asdasdasd'}]
    filenames = next(walk("."), (None, None, []))[2]  # [] if no file
    
    print('Files: ' + str(filenames))
    for filename in filenames:
        if 'table_' in filename:
            f = open(filename, 'r')
            content = json.load(f)
            print(content)
            replicateTable(filename.replace('table_','').replace('.json',''), content)

def replicateTable(tableName, content):
    primarykeyNames = list(listPrimaryKeyNames[tableName])
    print("-------- replicateTable")
    primaryKeyValues = initPrimaryKeyValues(primarykeyNames)
    args=parser.parse_args()

    conn = psycopg2.connect(user="gunter",
                            password=args.password,
                            host=args.hostname,
                            port="5432",
                            database=args.database)
    print(print("-------- connected"))
    
    updated_rows = 0
    created_rows = 0

    # if does not connect so 
    # CREATE ROLE gunter superuser;
    # ALTER ROLE gunter WITH LOGIN;
    print("content: " + str(content))
    for item in content:
        getPrimaryKeyValues(item,primarykeyNames,primaryKeyValues)

        updated_rows += updateElement(item,tableName,conn)

        if(updated_rows < 1):
            created_rows += createElement(item,tableName,conn)
           
    
    print("updated_rows: " + str(updated_rows))
    print("created_rows: " + str(created_rows))

    deleteNonExistsElements(tableName, primaryKeyValues,conn)

    print("--------replicateTable finished")
    return "Table '" + tableName + "' replicated!"

def updateElement(item,tableName,conn):
    cur = conn.cursor()
    updateQuery = makeUpdateQuery(item,tableName)
    print(updateQuery)
    cur.execute(updateQuery)
    conn.commit()
    return cur.rowcount

def createElement(item,tableName,conn):
    cur = conn.cursor()
    insertQuery = makeInsertQuery(item,tableName)
    print(insertQuery)
    cur.execute(insertQuery)
    conn.commit()
    updated_rows = cur.rowcount

def deleteNonExistsElements(tableName,primaryKeyValues,conn):
    cur = conn.cursor()
    primarykeyNames = list(listPrimaryKeyNames[tableName])

    listNonExistElements = selectNonExistElements(tableName,primaryKeyValues,conn)

    print(listNonExistElements)
    for itemData in listNonExistElements:
        deleteQuery = makeDeleteQuery(itemData,tableName)
        print(deleteQuery)
        cur.execute(deleteQuery)
        conn.commit()
        

def selectNonExistElements(tableName,primaryKeyValues,conn):
    cur = conn.cursor(cursor_factory=RealDictCursor)

    selectQuery = makeSelectQueryNonExistElements(tableName,primaryKeyValues)
    print(selectQuery)

    cur.execute(selectQuery)
    conn.commit()
    return cur.fetchall()


def makeInsertQuery(item, tableName):
    fields = item.keys()

    my_field_names = str(list(fields)).replace("[", "(").replace("]", ")").replace("'", '"')
    my_field_values = str([item[field] for field in fields]).replace("[", "(").replace("]", ")")
    
    return "INSERT INTO "+getTableNameForQuery(tableName)+" " + my_field_names +" VALUES " + my_field_values


def makeUpdateQuery(item, tableName):
    fields = item.keys()
    my_field_names = list(listPrimaryKeyNames[tableName])

    update_query = "UPDATE " +getTableNameForQuery(tableName)+ " SET "
    
    update_query += generateStringFieldValue(item, list(fields),",")

    update_query += " WHERE " + generateStringFieldValue(item, my_field_names,"AND")

    return update_query

def makeDeleteQuery(itemData, tableName):
    my_field_names = list(listPrimaryKeyNames[tableName])

    update_query = "DELETE FROM " +getTableNameForQuery(tableName)+ " "    

    update_query += "WHERE " + generateStringFieldValue(transformItem(my_field_names,itemData), my_field_names,"AND")

    return update_query

def transformItem(my_field_names,itemData):
    item = {}
    for fieldName in my_field_names:
        item[fieldName] = itemData[fieldName]

    return item

def generateStringFieldValue(item, my_field_names,concat):
    print(my_field_names)

    fieldValue = '"'+ my_field_names[0] +'" = \'' + item[my_field_names[0]] + "' "
    my_field_names.pop(0)
    for field in my_field_names:
        fieldValue += concat+' "'+ field +'" = \'' + item[field] + "' "
    
    return fieldValue

def makeSelectQueryNonExistElements(tableName,primaryKeyValues):
    my_field_names = list(listPrimaryKeyNames[tableName])

    selectQuery = "SELECT "+ str(my_field_names).replace('[','').replace(']','').replace('\'','"')
    selectQuery += " FROM " + getTableNameForQuery(tableName) + " "
    
    selectQuery += "WHERE " + generateStringFieldValueForQueryNonExistElements(primaryKeyValues, my_field_names)

    return selectQuery

def generateStringFieldValueForQueryNonExistElements(primaryKeyValues, my_field_names):
    print(my_field_names)

    fieldValue = '"'+ my_field_names[0] +'" NOT IN ' + str(primaryKeyValues[my_field_names[0]]).replace('[','(').replace(']',')')
    my_field_names.pop(0)
    for field in my_field_names:
        fieldValue += ' AND "'+ field +'" NOT IN ' + str(primaryKeyValues[field]).replace('[','(').replace(']',')')
    
    return fieldValue

def getPrimaryKeyValues(item, primaryKeyList, primaryKeyValues):
    for primaryKey in  primaryKeyList:
        primaryKeyValues[primaryKey].append(item[primaryKey])


def initPrimaryKeyValues(primaryKeyList):
    primaryKeyValues = {}
    for primaryKey in primaryKeyList:
        #setattr(primaryKeyValues.a, param, [])
        primaryKeyValues[primaryKey] = []

    return primaryKeyValues

def getTableNameForQuery(tableName):
    return 'pub."'+tableName+'"'

if __name__ == '__main__':
    print("INITIALIZING . . . ")
    getparameters()
    replicaDataBaseFromProgresToPostgres()


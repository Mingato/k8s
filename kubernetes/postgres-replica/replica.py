from subprocess import call
import argparse, sys
from flask import Flask
from flask_cors import CORS
from flask import request
import requests, json, psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
parser=argparse.ArgumentParser()
#pip install Flask
#pip install Requests
#pip install psycopg2
#pip install -U flask-cors
#python3 replica.py --username "gunter@redcompany.com.br" --password "kisphp" --hostname "192.168.100.236" --database "wm3"
#Send request curl --location --request POST 'http://localhost:8081/postgres/replica/TestsJson' --header 'Content-Type: application/json' --data-raw '[{"data":"daasdasdasd", "test":"asdasdasd"},{"data":"daasdasdasd", "test":"asdasdasd"}]'

listPrimaryKeyNames = {
    "rwm_usuario": [
        "id_usuario"
    ],
    "rwm_grp": [
        "cod_grp"
    ],
    "rwm_circulo": [
        "cod_circulo"
    ],
    "rwm_grp_rel": [
        "cod_circulo",
        "cod_grp",
        "cod_grp_rel"
    ],
    "rwm_circulo_grp": [
        "cod_circulo",
        "cod_grp",
        "cod_pai",
        "seq",
        "seq_pai"
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

@app.route('/postgres/replica', methods=['POST'])
def replicaDataBaseFromProgresToPostgres():

    content = request.json
    #content = [{'nome':'daasdasdasd', 'test':'asdasdasd'},{'data':'daasdasdasd', 'test':'asdasdasd'}]
    
    #print(content["RWM_TABLES"].keys())
    for tableName in content["RWM_TABLES"].keys():
        print("------------- replicando: " + tableName)
        replicateTable(tableName, content["RWM_TABLES"][tableName])
    
    return "DataBase successfuly replicated!"

def replicateTable(tableName, content):
    primarykeyNames = list(listPrimaryKeyNames[tableName])
    primaryKeyValues = initPrimaryKeyValues(primarykeyNames)
    args=parser.parse_args()

    conn = psycopg2.connect(user="gunter",
                            password=args.password,
                            host=args.hostname,
                            port="5432",
                            database=args.database)
    
    updated_rows = 0
    created_rows = 0

    # if does not connect so 
    # CREATE ROLE gunter superuser;
    # ALTER ROLE gunter WITH LOGIN;
    print("Content size: " + str(len(content)))
    for item in content:
        getPrimaryKeyValues(item,primarykeyNames,primaryKeyValues)

        updated_row = updateElement(item,tableName,conn)
        if(updated_row < 1):
            created_rows += createElement(item,tableName,conn)

        updated_rows += updated_row

    deleted_rows = deleteNonExistsElements(tableName, primaryKeyValues,conn)

    print("------ results")
    print("updated_rows: " + str(updated_rows))
    print("created_rows: " + str(created_rows))
    print("deleted_rows: " + str(deleted_rows))
    print("--------------------------------------------------------")
    return "Table '" + tableName + "' replicated!"

def updateElement(item,tableName,conn):
    cur = conn.cursor()
    updateQuery = makeUpdateQuery(item,tableName)
    #print(updateQuery)
    cur.execute(updateQuery)
    conn.commit()
    return cur.rowcount

def createElement(item,tableName,conn):
    cur = conn.cursor()
    insertQuery = makeInsertQuery(item,tableName)
    #print(insertQuery)
    cur.execute(insertQuery)
    conn.commit()
    return cur.rowcount

def deleteNonExistsElements(tableName,primaryKeyValues,conn):
    deleted_rows = 0
    cur = conn.cursor()
    primarykeyNames = list(listPrimaryKeyNames[tableName])

    listNonExistElements = selectNonExistElements(tableName,primaryKeyValues,conn)

    #print(listNonExistElements)
    for itemData in listNonExistElements:
        deleteQuery = makeDeleteQuery(itemData,tableName)
        #print(deleteQuery)
        cur.execute(deleteQuery)
        deleted_rows += cur.rowcount
        conn.commit()
    
    return deleted_rows

def selectNonExistElements(tableName,primaryKeyValues,conn):
    cur = conn.cursor(cursor_factory=RealDictCursor)

    selectQuery = makeSelectQueryNonExistElements(tableName,primaryKeyValues)
    #print(selectQuery)

    cur.execute(selectQuery)
    conn.commit()
    return cur.fetchall()


def makeInsertQuery(item, tableName):
    fields = item.keys()

    my_field_names = str(list(fields)).replace("[", "(").replace("]", ")").replace("'", '"')
    my_field_values = str([item[field] for field in fields]).replace("[", "(").replace("]", ")").replace("None", "NULL")
    
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
    #print(my_field_names)

    fieldValue = '"'+ my_field_names[0] +'" = ' + getValueAccordingToType(item[my_field_names[0]]) + " "
    my_field_names.pop(0)
    for field in my_field_names:
        fieldValue += concat+' "'+ field +'" = ' + getValueAccordingToType(item[field]) + " "
    
    return fieldValue

def getValueAccordingToType(value):
    if isinstance(value, str):
        return "\'" + value + "\'"
    elif value is None:
        return "NULL"
    else:
        return str(value)


def makeSelectQueryNonExistElements(tableName,primaryKeyValues):
    my_field_names = list(listPrimaryKeyNames[tableName])

    selectQuery = "SELECT "+ str(my_field_names).replace('[','').replace(']','').replace('\'','"')
    selectQuery += " FROM " + getTableNameForQuery(tableName) + " "
    
    selectQuery += "WHERE " + generateStringFieldValueForQueryNonExistElements(primaryKeyValues, my_field_names)

    return selectQuery

def generateStringFieldValueForQueryNonExistElements(primaryKeyValues, my_field_names):
    #print(my_field_names)

    fieldValue = '"'+ my_field_names[0] +'" NOT IN ' + str(primaryKeyValues[my_field_names[0]]).replace('[','(').replace(']',')')
    my_field_names.pop(0)
    for field in my_field_names:
        fieldValue += ' AND "'+ field +'" NOT IN ' + str(primaryKeyValues[field]).replace('[','(').replace(']',')')
    
    return fieldValue

def getPrimaryKeyValues(item, primaryKeyList, primaryKeyValues):
    for primaryKey in primaryKeyList:
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

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True,
            host="0.0.0.0",
            port=8081,
            threaded=True)



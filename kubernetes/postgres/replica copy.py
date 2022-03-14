from subprocess import call
import argparse, sys
from flask import Flask
from flask_cors import CORS
from flask import request
import requests, json, psycopg2  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
parser=argparse.ArgumentParser()
#pip install Flask
#pip install Requests
#pip install psycopg2
#pip install -U flask-cors
#python3 replica.py --username "gunter@redcompany.com.br" --password "kisphp" --hostname "192.168.100.236" --database "wm3"
#Send request curl --location --request POST 'http://192.168.100.236:8080/upload-version/news-service/0.0.7'

def getparameters():
    parser.add_argument('--username', help='username', type=str, required=True)
    parser.add_argument('--password', help='password', type=str, required=True)
    parser.add_argument('--hostname', help='hostname', type=str, required=True)
    parser.add_argument('--database', help='database', type=str, required=True)
    
    args=parser.parse_args()
    print("POSTGRES_USERNAME: " + args.username)
    print("POSTGRES_PASSWORD: " + args.password)
    print("POSTGRES_HOSTNAME: " + args.hostname)
    print("POSTGRES_DATABASE: " + args.database)

@app.route('/postgres/replica/<tablename>', methods=['POST'])
def uploadApplicationVersion(tablename):
    print(request)
    tablename = 'pub."'+tablename+'"'

    #content = request.json
    content = [{'data':'daasdasdasd', 'test':'asdasdasd'},{'data':'daasdasdasd', 'test':'asdasdasd'}]
    print(makeQuery(content[0], tablename))
    #my_field_values = str([content[0][field] for field in content[0].keys()]).replace("[", "(").replace("]", ")")
    #my_field_names = str(list(content[0].keys())).replace("[", "(").replace("]", ")")
    #print(my_field_names))
    #print(my_field_values)
    #print("INSERT INTO "+tablename+" " + my_field_names +" VALUES " + my_field_values)

    return replicateTable(tablename, content)

def replicateTable(tablename, content):
    print("--------replicateTable")
    
    args=parser.parse_args()
    
    try:
        conn = psycopg2.connect(user=args.username,
                                password=args.password,
                                host=args.hostname,
                                port="5432",
                                database=args.database)
        print(content)
        for item in content:
            query = makeQuery(item)
            print(query)
            conn.cursor().execute(query)
            conn.commit()

        
    except:
        print("I am unable to connect to the database")
        return "I am unable to connect to the database"


    return "Table '" + tablename + "' replicated!"
    print("--------replicateTable finished")

def makeQuery(item, tablename):
    fields = item.keys()

    my_field_names = str(list(fields)).replace("[", "(").replace("]", ")").replace("'", '"')
    my_field_values = str([item[field] for field in fields]).replace("[", "(").replace("]", ")")
    
    insert_query = makeInsertQuery(tablename,my_field_names,my_field_values)
    update_query = makeUpdateQuery(list(fields), item)

    

    return insert_query+ " " + update_query

def makeInsertQuery(tablename,my_field_names,my_field_values):
    insert_query = "INSERT INTO "+tablename+" " + my_field_names +" VALUES " + my_field_values

def makeUpdateQuery(my_field_names, item):
    update_query = "ON CONFLICT DO UPDATE SET "

    my_field_names[0]
    update_query += '"'+ my_field_names[0] +'" = \'' + item[my_field_names[0]] + "'"
    my_field_names.pop(0)
    for field in my_field_names:
        update_query += ', "'+ field +'" = \'' + item[field] + "'"

    return update_query

if __name__ == '__main__':
    print("INITIALIZING . . . ")
    getparameters()

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True,
            host="0.0.0.0",
            port=8081,
            threaded=True)
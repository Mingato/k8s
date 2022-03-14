from subprocess import call
import argparse, sys
from flask import Flask
from flask_cors import CORS
#from flask import request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
parser=argparse.ArgumentParser()
#pip install Flask
#pip install -U flask-cors
#python3 deployer.py --username "Gunter" --password "b1i2t3" --urlRepository "http://192.168.100.12:8081"
#Send request curl --location --request POST 'http://192.168.100.236:8080/upload-version/news-service/0.0.7'

def getparameters():
    parser.add_argument('--username', help='username', type=str, required=True)
    parser.add_argument('--password', help='password', type=str, required=True)
    parser.add_argument('--urlRepository', help='urlRepository', type=str, required=True)
    
    args=parser.parse_args()
    print("GIT_USERNAME: " + args.username)
    print("GIT_PASSWORD: " + args.password)
    print("URL_REPOSITORY: " + args.urlRepository)

@app.route('/upload-version/<aplicationName>/<version>', methods=['POST'])
def uploadApplicationVersion(aplicationName,version):
    print("POST /upload-version/"+aplicationName+"/"+version)

    createDockerImage(aplicationName, version)

    downloadRepo()
    changeDeploymentImageVersion(aplicationName, version)
    commitFile()

    return aplicationName +" version changed!"


def createDockerImage(aplicationName, version):
    print("\n---------------------------- createDockerImage ----------------------------")
    args=parser.parse_args()

    imageName = 'wm3/' +aplicationName+":"+version

    command = 'docker build ./apps/' + aplicationName + ' -t ' + imageName + ' --build-arg VERSION=' + version + ' --build-arg URL_REPOSITORY="' + args.urlRepository + '"'
    print(command)
    call("eval $(minikube docker-env)", shell=True)
    call(command, shell=True)
    print("\n---------------------------- createDockerImage finished ----------------------------")

#### download file from git
def downloadRepo():
    print("\n---------------------------- Downloading repo ----------------------------")
    args=parser.parse_args()

    fileUrl = 'https://'+args.username+':'+args.password+'@git.webmodule.com.br/scm/wmser/docker.git'
    #call("rm docker", shell=True)
    commandClone = "git clone "+fileUrl
    print(commandClone)
    call(commandClone, shell=True)
    #call("git revert master", shell=True)

    call("git -C docker pull", shell=True)
    print("\n---------------------------- Repo Downloaded  ----------------------------")


####Change file version
def changeDeploymentImageVersion(aplicationName, version):
    print("\n---------------------------- changing file version ----------------------------")
    import yaml

    
    fileName = "docker/kubernetes/apps/"+aplicationName+"/deployment.yaml"#service
    imageName = 'wm3/' +aplicationName+":"+version
    print("File: " + fileName)
    print("New Image version: " + imageName)

    with open(fileName, "r") as yaml_in:
        yaml_list = list(yaml.safe_load_all(yaml_in))

        for yaml_object in yaml_list:
            print(yaml_object)
            if(yaml_object is not None):
                print(yaml_object["kind"])

                if yaml_object["kind"] == "Deployment":
                    #print(deploymentYaml)
                    print("Current IMAGE: " + str(yaml_object['spec']['template']['spec']['containers'][0]['image']))
                    yaml_object['spec']['template']['spec']['containers'][0]['image'] = imageName
                    print("New IMAGE VERSION: " + imageName)

        with open(fileName, 'w') as outfile:
            yaml.dump_all(yaml_list, outfile,default_flow_style=False,sort_keys=False)
    
    print("\n---------------------------- file version changed ----------------------------")

#### write file on git
def commitFile():
    print("\n---------------------------- Commit file ----------------------------")

    gitCommand_Add = "git -C docker add --all"
    gitCommand_Commit = 'git -C docker commit -m "Changing version"'
    gitCommand_Push = "git -C docker push"

    print(gitCommand_Add)
    call(gitCommand_Add, shell=True)

    print(gitCommand_Commit)
    call(gitCommand_Commit, shell=True)

    print(gitCommand_Push)
    call(gitCommand_Push, shell=True)

    print("\n---------------------------- file commited ----------------------------")

if __name__ == '__main__':
    print("INITIALIZING . . . ")
    getparameters()

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True,
            host="0.0.0.0",
            port=8080,
            threaded=True)
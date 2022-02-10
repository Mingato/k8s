from subprocess import call
import argparse, sys
from flask import Flask
from flask_cors import CORS
#from flask import request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

print("initializing . . .")

@app.route('/<aplicationName>/<version>', methods=['POST'])
def hello(aplicationName,version):
    
    print("POST /"+aplicationName+"/"+version)

    #downloadRepo(args.username, args.password, args.projectName)

    #changeDockerFileVersion()

    #createDockerImage()

    #changeFileVersion(aplicationName, version)
    #commitFile()

    return 'Hello, World!'
    
print("initialized")

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", port=8080)
    


#### download file from git
def downloadRepo(username, password, projectName):
    print("\n . . . Downloading repo . . . ")

    #fileUrl = 'https://'+username+':'+password+'@bitbucket.org/guntermingato/'+projectName+'.git'
    fileUrl = 'https://'+username+':'+password+'@git.webmodule.com.br/scm/wmser/docker.git'
    #call("rm docker", shell=True)
    commandClone = "git clone "+fileUrl
    print(commandClone)
    print("---------------")
    call(commandClone, shell=True)
    #call("git revert master", shell=True)

    call("git -C "+projectName+" pull", shell=True)



####Change file version
def changeFileVersion(projectName, version):
    print("\n . . . changing file version . . . ")
    #pip install pyyaml
    import yaml

    fileName = "docker/kubernetes/apps/"+projectName+"/deployment.yaml"#service
    print("File: " + fileName)

    with open(fileName, "r") as yaml_in:
        yaml_list = list(yaml.safe_load_all(yaml_in))

        for yaml_object in yaml_list:
            print(yaml_object["kind"])

            if yaml_object["kind"] == "Deployment":
                #print(deploymentYaml)
                print("Current version: " + str(yaml_object['spec']['template']['metadata']['labels']['version']))
                yaml_object['spec']['template']['metadata']['labels']['version'] = version
                print("New appVersion: " + version)

        with open(fileName, 'w') as outfile:
            yaml.dump_all(yaml_list, outfile,default_flow_style=False)

#### write file on git
def commitFile():
    print("\n . . . Commit file . . . ")

    project = "docker"

    gitCommand_Add = "git -C "+project+" add *"
    gitCommand_Commit = 'git -C '+project+' commit -m "Changing version"'
    gitCommand_Push = "git -C "+project+" push"

    print(gitCommand_Add)
    call(gitCommand_Add, shell=True)

    print(gitCommand_Commit)
    call(gitCommand_Commit, shell=True)

    print(gitCommand_Push)
    call(gitCommand_Push, shell=True)

#if __name__ == '__main__':

    #print("INITIALIZING . . . ")
    #parser=argparse.ArgumentParser()

    #parser.add_argument('--username', help='username', type=str, required=True)
    #parser.add_argument('--password', help='password', type=str, required=True)
    #parser.add_argument('--projectName', help='projectName', type=str, required=True)
    #parser.add_argument('--projectVersion', help='projectVersion', type=str, required=True)

    #args=parser.parse_args()

    #downloadRepo(args.username, args.password, args.projectName)
    #changeFileVersion(args.projectName, args.projectVersion)
    #commitFile()

#python deploy-service-dev.py --username "guntermingato" --password "senhaboa1515" --projectName "auth-pipe" --projectVersion "2.0"
#python deploy-service-dev.py --username "Gunter" --password "b1i2t3" --projectName "auth" --projectVersion "2.0"
#python deploy-service-dev.py --username $USERNAME_K8S_REPOSITPRY --password $PASSWORD_K8S_REPOSITPRY --projectName $BITBUCKET_REPO_FULL_NAME --projectVersion $BITBUCKET_BUILD_NUMBER

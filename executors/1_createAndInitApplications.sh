#!/bin/bash
echo "STARTING WM3 . . . \n"

#É preciso que esteja instalado:
#   docker
#   kubectl

#download all projeject
#git clone https://Gunter:b1i2t3@git.webmodule.com.br/scm/wmser/docker.git


#init minikube
echo "----------------------- Create MINIKUNE ----------------------------- "
minikube start --memory=34096 --cpus=4 --embed-certs
minikube -p minikube docker-env
eval $(minikube docker-env)
ufw allow 8000:8100/tcp


#init istio
echo "------------------------ Init Istio ----------------------------- "
cd ../istio-1.13.2
export PATH=$PWD/bin:$PATH
istioctl install --set profile=default -y
kubectl label namespace default istio-injection=enabled
minikube addons enable ingress

#init tsl config
echo "---------------------- TLS ssh config ---------------------------- "
cd ../kubernetes/gateway
kubectl create -n istio-system secret tls istio-ingressgateway-certs --key webmodule-key.pem --cert webmodule-crt.pem

# init argocd
echo "------------------------ Init ArgoCD ----------------------------- "
cd ../argocd
kubectl create namespace argocd
kubectl apply -n argocd -f instalation
kubectl apply -f apps

#create application images
echo "------------------ Create application images ---------------------- "
cd ../../deployer
python3 initApplications.py --username "Gunter" --password "b1i2t3" --urlRepository "http://192.168.100.12:8081"


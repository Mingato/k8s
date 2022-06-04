#!/bin/bash
echo "STARTING WM3 . . . \n"

#É preciso que esteja instalado:
#   docker
#   kubectl

#download all projeject
#git clone https://Gunter:b1i2t3@git.webmodule.com.br/scm/wmser/docker.git


#init minikube
echo "----------------------- Create MINIKUNE ----------------------------- "
minikube start --memory=34096 --cpus=4 --vm-driver=xhyve
minikube -p minikube docker-env
eval $(minikube docker-env)
sudo ufw allow 8000:8100/tcp
sudo ufw allow out 8000:8100/tcp
sudo ufw allow 5432/tcp
sudo ufw allow out 5432/tcp
sudo ufw enable

minikube addons enable metrics-server
#minikube addons enable dashboard

#monitoring
kubectl create namespace monitoring
helm install --generate-name stable/prometheus-operator --namespace monitoring --set prometheus.prometheusSpec.serviceMonitorNamespaceSelector.any=true


#init istio
echo "------------------------ Init Istio ----------------------------- "
cd ../istio-1.13.2
export PATH=$PWD/bin:$PATH
istioctl install --set profile=default -y
#istioctl operator init --watchedNamespaces=istio-system,default
kubectl label namespace default istio-injection=enabled
minikube addons enable ingress
#kubectl aaply -f ./samples/addons/prometheus.yaml
#kubectl aaply -f ./samples/addons/kiali.yaml

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

# init prometheus e grafana
echo "------------------------ Init ArgoCD ----------------------------- "
cd ../monitoring
kubectl create -f manifests/setup
kubectl create -f manifests/

#create application images
echo "------------------ Create application images ---------------------- "
cd ../../deployer
python3 initApplications.py --username "Gunter" --password "b1i2t3" --urlRepository "http://192.168.100.12:8081"


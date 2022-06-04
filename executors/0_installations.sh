#sudo hostnamectl set-hostname master-node
sudo apt-get update -y

# install docker
sudo apt-get install docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
sudo chmod 666 /var/run/docker.sock

# install kubectl
sudo apt update
sudo apt -y install curl apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install kubectl
sudo apt-mark hold kubectl

#sudo swapoff -a  
#sudo sed -i '/ swap / s/^/#/' /etc/fstab


#install minikube
wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo cp minikube-linux-amd64 /usr/local/bin/minikube
sudo chmod +x /usr/local/bin/minikube

#install python
sudo apt install python3-pip
pip install flask
pip install flask_cors

# resolvconfig
sudo apt install resolvconf 
sudo systemctl enable --now resolvconf.service

#helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh
helm version

helm repo add stable https://charts.helm.sh/stable
helm repo update
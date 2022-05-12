
sudo apt-get update

# install docker
sudo apt-get install docker.io
sudo systemctl enable docker
sudo systemctl start docker

# install kubectl
#sudo apt-get install kubeadm kubelet kubectl
#sudo apt-mark hold kubeadm kubelet kubectl
sudo apt-get install kubectl
sudo apt-mark hold kubectl

sudo swapoff -a  
sudo sed -i '/ swap / s/^/#/' /etc/fstab
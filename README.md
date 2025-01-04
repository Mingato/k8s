
# Kubernetes Setup Guide
This guide provides step-by-step instructions for setting up Docker, Kubernetes, Minikube, Istio, ArgoCD, and other tools on Ubuntu.


## Prerequisites

1. **Install Docker and Kubectl**:
   ```bash
   sudo swapoff -a
   sudo curl -fsSL https://get.docker.com | bash
   curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   sudo apt-get update
   sudo apt-get install kubelet kubectl kubeadm -y
   ```

---

## Kubernetes Installation

1. **Set Hostname**:
   ```bash
   sudo hostnamectl set-hostname master-node
   sudo hostnamectl set-hostname worker01
   ```

2. **Initialize Kubernetes Cluster**:
   ```bash
   sudo kubeadm init --pod-network-cidr=10.244.0.0/16
   # Or specify advertise address
   sudo kubeadm init --apiserver-advertise-address=$(hostname -i) --pod-network-cidr=10.244.0.0/16
   ```

3. **Setup kubeconfig**:
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

---

## Minikube Installation

For systems with less than 32GB RAM, use Minikube:

1. **Start Minikube**:
   ```bash
   mkdir -p $HOME/minikube/src/data
   minikube start --memory=16096 --mount --mount-string $HOME/minikube/src/data:/data
   eval $(minikube -p minikube docker-env)
   sudo ufw allow 30000:60000/tcp
   ```

2. **Mount with Daemon**:
   ```bash
   sudo apt update
   sudo apt install daemon
   daemon minikube mount $HOME/minikube/src/data:/data
   ```

---

## Istio Installation

1. **Download and Install Istio**:
   ```bash
   curl -L https://istio.io/downloadIstio | sh -
   cd istio-1.11.3
   export PATH=$PWD/bin:$PATH
   istioctl install --set profile=default -y
   ```

2. **Enable Sidecar Injection**:
   ```bash
   kubectl label namespace default istio-injection=enabled
   kubectl get ns default --show-labels
   ```

---

## ArgoCD Installation

1. **Install ArgoCD**:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. **Access ArgoCD**:
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   ```

3. **Expose Service**:
   ```bash
   kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer", "externalIPs":["192.168.100.236"]}}'
   ```

---

## NFS Server Setup

1. **Install and Configure NFS**:
   ```bash
   sudo apt update
   sudo apt install nfs-kernel-server
   sudo mkdir -p /var/nfs/k8s
   sudo chmod -R 777 /var/nfs
   sudo chown nobody:nogroup /var/nfs/k8s
   ```

2. **Export Directory**:
   ```bash
   echo "/var/nfs/k8s *(rw,sync,no_subtree_check,insecure,no_root_squash)" | sudo tee -a /etc/exports
   sudo exportfs -rav
   sudo systemctl restart nfs-kernel-server
   ```

---

## Troubleshooting

1. **Images Not Found in Minikube**:
   ```bash
   eval $(minikube docker-env)
   docker build -t <image-name> .
   kubectl set imagePullPolicy Never
   ```

2. **Firewall Issues**:
   ```bash
   sudo ufw allow 8080:8100/tcp
   sudo ufw allow 30000:60000/tcp
   ```

3. **Accessing Services Across Namespaces**:
   ```bash
   <service-name>.<namespace>.svc.cluster.local
   ```

---

## Helm Installation

1. **Install Helm**:
   ```bash
   brew install helm
   ```

2. **Configure Helm in Kubernetes**:
   ```bash
   kubectl -n kube-system create serviceaccount tilter
   kubectl create clusterrolebinding tilter --clusterrole cluster-admin --serviceaccount=kube-system:tilter
   helm repo update
   helm install <chart-name>
   ```

---

For more detailed information, refer to the [official documentation](https://kubernetes.io/docs/home/).
```

Feel free to customize the content or add more details as needed.

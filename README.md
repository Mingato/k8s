# Kubernetes Project Setup Guide

This repository contains a comprehensive Kubernetes setup with Docker applications, Istio service mesh, ArgoCD for GitOps, and automated deployment tools. The project includes microservices architecture with monitoring, authentication, and various application services.

## 📁 Project Structure

```
k8s/
├── kubernetes/           # Kubernetes manifests and configurations
│   ├── apps/            # Application deployments
│   ├── argocd/          # ArgoCD configurations
│   ├── authentication/   # Auth service configurations
│   ├── configs/         # General configurations
│   ├── dashboards/      # Monitoring dashboards
│   ├── elasticsearch/   # Elasticsearch setup
│   ├── gateway/         # API Gateway configurations
│   ├── kiali/          # Istio Kiali dashboards
│   ├── monitoring/      # Prometheus/Grafana setup
│   ├── mongodb/         # MongoDB configurations
│   ├── nginx/           # Nginx configurations
│   ├── pgadmin/         # PostgreSQL admin
│   ├── postgres/        # PostgreSQL configurations
│   ├── postgres-replica/ # PostgreSQL replica
│   └── volumes/         # Persistent volume configurations
├── docker-apps/         # Docker application Dockerfiles
├── deployer/            # Deployment automation scripts
├── executors/           # Execution scripts
├── istio-1.11.3/       # Istio installation files
├── istio-1.13.2/       # Istio installation files
├── docker-compose.yaml  # Local development setup
├── deploy-service-dev.py # Automated deployment script
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Ubuntu 20.04+ (recommended)
- At least 8GB RAM (16GB+ recommended)
- Docker installed
- Git installed

### 1. Install Docker and Kubernetes Tools

```bash
# Disable swap
sudo swapoff -a

# Install Docker
sudo curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# Install kubectl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubectl kubeadm
```

### 2. Choose Your Kubernetes Setup

#### Option A: Full Kubernetes Cluster (32GB+ RAM)

```bash
# Set hostname for master node
sudo hostnamectl set-hostname master-node

# Initialize cluster
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=$(hostname -i)

# Setup kubeconfig
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### Option B: Minikube (Recommended for development, <32GB RAM)

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube with custom configuration
mkdir -p $HOME/minikube/src/data
minikube start --memory=16096 --mount --mount-string $HOME/minikube/src/data:/data
eval $(minikube -p minikube docker-env)

# Configure firewall
sudo ufw allow 30000:60000/tcp
sudo ufw allow 8080:8100/tcp

# Optional: Mount with daemon for persistent mounting
sudo apt update && sudo apt install -y daemon
daemon minikube mount $HOME/minikube/src/data:/data
```

## 🔧 Service Mesh Setup

### Install Istio

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.11.3
export PATH=$PWD/bin:$PATH

# Install Istio with default profile
istioctl install --set profile=default -y

# Enable sidecar injection for default namespace
kubectl label namespace default istio-injection=enabled
kubectl get ns default --show-labels

# Enable Minikube addons (if using Minikube)
minikube addons enable ingress
```

### Verify Istio Installation

```bash
# Check Istio components
kubectl get pods -n istio-system

# Check sidecar injection
kubectl get ns default --show-labels
```

## 🚀 GitOps with ArgoCD

### Install ArgoCD

```bash
# Create ArgoCD namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
```

### Access ArgoCD

```bash
# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Expose ArgoCD service (replace with your IP)
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer", "externalIPs":["YOUR_IP_ADDRESS"]}}'

# Or use port-forward for local access
kubectl port-forward --address=0.0.0.0 svc/argocd-server -n argocd 8080:443
```

**Default credentials:**
- Username: `admin`
- Password: (use the command above to get it)

## 🐳 Docker Applications

This project includes several microservices:

- **auth**: Authentication service
- **notification**: Notification service  
- **storage**: File storage service
- **news**: News/content service
- **chat**: Real-time chat service
- **socket**: WebSocket service
- **demo**: Demo application

### Local Development with Docker Compose

```bash
# Start all services locally
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Build Individual Services

```bash
# Build a specific service
docker build -f docker-apps/auth.Dockerfile -t wm3/auth-service ./docker-apps/

# Build all services
for service in auth notification storage news chat socket demo; do
    docker build -f docker-apps/${service}.Dockerfile -t wm3/${service}-service ./docker-apps/
done
```

## 🤖 Automated Deployment

### Using the Deployment Script

The `deploy-service-dev.py` script automates the deployment process:

```bash
# Deploy a service with new version
python deploy-service-dev.py \
    --username "your-username" \
    --password "your-password" \
    --projectName "auth" \
    --projectVersion "2.0"
```

### Manual Deployment Process

1. **Update version in deployment YAML**
2. **Commit changes to Git repository**
3. **ArgoCD automatically detects changes and deploys**

## 📊 Monitoring and Observability

### Available Dashboards

- **Kiali**: Istio service mesh visualization
- **Grafana**: Metrics and monitoring
- **ArgoCD**: Application deployment status
- **pgAdmin**: PostgreSQL administration

### Access Dashboards

```bash
# Kiali (Istio)
kubectl port-forward svc/kiali 20001:20001 -n istio-system

# Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# pgAdmin
kubectl port-forward svc/pgadmin 5050:80 -n postgres
```

## 🗄️ Database Setup

### PostgreSQL

```bash
# Apply PostgreSQL configurations
kubectl apply -f kubernetes/postgres/
kubectl apply -f kubernetes/pgadmin/
```

### MongoDB

```bash
# Apply MongoDB configurations
kubectl apply -f kubernetes/mongodb/
```

### Elasticsearch

```bash
# Apply Elasticsearch configurations
kubectl apply -f kubernetes/elasticsearch/
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Images Not Found in Minikube

```bash
# Build images in Minikube's Docker environment
eval $(minikube docker-env)
docker build -t <image-name> .

# Set image pull policy to Never for local images
kubectl set image deployment/<deployment-name> <container-name>=<image-name> --image-pull-policy=Never
```

#### 2. Firewall Issues

```bash
# Allow required ports
sudo ufw allow 8080:8100/tcp
sudo ufw allow 30000:60000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

#### 3. Service Communication Issues

```bash
# Check service endpoints
kubectl get endpoints

# Test service connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup <service-name>.<namespace>.svc.cluster.local
```

#### 4. Istio Issues

```bash
# Check Istio components
kubectl get pods -n istio-system

# Verify sidecar injection
kubectl describe pod <pod-name> | grep -A 10 "Containers:"

# Uninstall Istio if needed
istioctl x uninstall --purge
```

#### 5. ArgoCD Issues

```bash
# Check ArgoCD pods
kubectl get pods -n argocd

# View ArgoCD logs
kubectl logs -n argocd deployment/argocd-server

# Reset ArgoCD admin password
kubectl -n argocd patch secret argocd-secret \
  -p '{"stringData": {"admin.password": "$2a$10$rRyBsGSHK6.uc8fntPxVIuLVHmAh7o54W1aR9lQmBUvUTvczq1zW."}}'
```

### Useful Commands

```bash
# Check cluster status
kubectl cluster-info

# View all resources
kubectl get all --all-namespaces

# Check node status
kubectl get nodes

# View events
kubectl get events --sort-by='.lastTimestamp'

# Access Minikube dashboard
minikube dashboard
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Istio Documentation](https://istio.io/latest/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

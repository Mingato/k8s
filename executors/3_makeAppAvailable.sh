#!/bin/bash

kubectl port-forward svc/istio-ingressgateway --address=0.0.0.0 -n istio-system 8081:443
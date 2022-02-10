Monitor the operator logs:
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator

disponibilizar o kibana:
kubectl port-forward service/quickstart-kb-http 5601
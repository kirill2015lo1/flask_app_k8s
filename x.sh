docker build -t tsurankirill/webapp:latest . && docker push tsurankirill/webapp:latest
kubectl delete -f flask.yaml
kubectl apply -f flask.yaml

docker build -t tsurankirill/webapp:latest . && docker push tsurankirill/webapp:latest
docker rmi $(docker images -qa)
kubectl delete -f flask.yaml 
kubectl apply -f flask.yaml

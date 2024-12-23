docker build -t tsurankirill/webapp:latest . && docker push tsurankirill/webapp:latest
kubectl apply -f flask.yaml

Перед развертыванием на baremetal нужно чтобы в кластере был установлен rook: `https://github.com/kirill2015lo1/devops/blob/main/install_rook(ceph).md` и 
metallb: `https://github.com/kirill2015lo1/devops/blob/main/install_metallb.md`

Чтобы запустить веб приложение, выполнить:
```
kubectl apply -f flask.yaml
```
При изменении Какого либа файла, чтобы вручную не удалять старые поды не пушить в dockerhub есть скрипт с названием x.sh, 
при надобности изменить репозиторий для пуша в скрипте, и заголиниться через docker login:


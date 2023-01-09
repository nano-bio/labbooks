## Create dump on old machine

```shell
cd /var/opt/labbooks/ &&
  source ../venv-labbooks/bin/activate &&
  python3 manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    -e contenttypes \
    -e auth.Permission \
    -e admin \
    -e sessions \
    -e labinventory.temperature \
    -o db-dump-for-transfer.json.gz
```

## Download dump

```shell
scp root@138.232.74.41:/var/opt/labbooks/db-dump-for-transfer.json.gz .
```

## Copy Dump to django service

```shell
docker compose cp db-dump-for-transfer.json.gz django:/src/.
```

## Import Dump in django container

```shell
docker compose exec django python3 manage.py loaddata db-dump-for-transfer.json
```

## Run on dev for dev machine

```shell
cd ~/gh-projects/labbooks/src &&
  scp root@138.232.74.41:/var/opt/labbooks/db-dump-for-transfer.json.gz . &&
  rm -f db.sqlite3 &&
  python3 manage.py migrate --settings=labbooks.settings_local &&
  echo "start loaddata" &&
  python3 manage.py loaddata --settings=labbooks.settings_local db-dump-for-transfer.json &&
  echo "finish loaddata"

```

## Copy to vServer

```shell
scp db-dump-for-transfer.json.gz \
  c7441211@c744-labbooks.uibk.ac.at:/srv/labbooks/.
```

## Run on dev for new machine

```shell
scp \
  root@138.232.74.41:/var/opt/labbooks/db-dump-for-transfer.json.gz \
  c7441211@c744-labbooks.uibk.ac.at:/srv/labbooks/.
```

## Run on new machine

```shell
#    python3 manage.py migrate && \
#    echo "start loaddata" && \
#    python3 manage.py loaddata db-dump-for-transfer.json && \
#    echo "finish loaddata"
```

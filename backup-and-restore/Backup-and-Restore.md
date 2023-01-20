# Backup and Restore

This document explains how the backup scripts are implemented and how to restore these backups.

Please check last line in `/etc/aliases`!

## Backup

There are three types of data:

- **Code / application**

  Code is saved in this GitHub-Repo.
  The application can always be recovered by cloning this repo on the server (`/srv/labbooks/` is
  used).

- **Media Files**

  All files, like tof.h5, image.png, data.csv, evaluation.zip are stored
  directly in the netshare managed bei ZID uibk.

  We do not backup this, because they do (and they are good!)

- **Database**

  Here, data like measurement datetime, deflector voltage or paths to
  the media files are stored. this is stored in a persistent docker volume
  named `postgres-data` stored in `/var/lib/docker/volumes/labbooks_postgres-data`.

  This, WE have to backup.

### Backup Scripts

Add the following line to `/etc/crontab`:

```shell
MAILTO=labbooks # see /etc/aliases
42 1 * * * root /srv/labbooks/backup-and-restore/backup-daily.sh >> /var/log/backup-labbooks.log
42 2 7 * * root /srv/labbooks/backup-and-restore/backup-monthly.sh >> /var/log/backup-labbooks.log

```

## Restore

### Useful commands

```shell
# Copy files from server to current folder:
scp root@138.232.74.41:/var/opt/labbooks/db-dump-for-transfer.json.gz .

# Copy Dump to django service
docker compose cp db-dump-for-transfer.json.gz django:/src/.

# Run command in a docker service: django load database
docker compose exec django python3 manage.py loaddata db-dump-for-transfer.json

```
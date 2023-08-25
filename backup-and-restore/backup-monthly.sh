#!/bin/bash

cd /srv/labbooks &&
  docker compose exec django python3 manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    -e contenttypes \
    -e auth.Permission \
    -e admin \
    -e sessions \
    -e labinventory.temperature \
    -o "db-dump-$(date +%Y-%m-%d).json.gz" &&
  docker compose cp \
    "django:/src/db-dump-$(date +%Y-%m-%d).json.gz" \
    /media/netshare/Backups/c744-labbooks/
